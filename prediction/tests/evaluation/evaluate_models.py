import pickle
import warnings

warnings.filterwarnings("ignore")

import time
import glob
import torch
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import product
from pytorch_lightning.callbacks import Callback, EarlyStopping
import pytorch_lightning as pl
from sklearn.preprocessing import MaxAbsScaler
from darts.models import *
from darts.dataprocessing.transformers import Scaler
from darts.utils.timeseries_generation import datetime_attribute_timeseries
from darts.metrics import *
from darts.utils.likelihood_models import GaussianLikelihood
from darts import TimeSeries, concatenate
from pytorch_lightning.callbacks import EarlyStopping
from datetime import timedelta

NR_DAYS = 90
DAY_DURATION = 24
DAY_PREDICT = 1     # Number of days we want to predict ahead
OUTPUT_CHUNK = DAY_PREDICT * DAY_DURATION   # predict n day ahead as test
LAGS = 7 * DAY_DURATION

torch.set_float32_matmul_precision("medium")

def evaluate_pipeline():
    #load data
    series_pricing, covariates_demand = load_electricity_data(selected_type = 'Hourly')
    train_pricing, val_pricing, train_pricing_transformed, val_pricing_transformed, series_pricing_transformed = transform_target(series_pricing)
    cov_demand_train, cov_demand_val, covariates_demand_transformed = transform_covariate(covariates_demand)
    
    #test on several library models available
    lr_smapes, lr_time = eval_global_model(train_pricing, val_pricing, LinearRegressionModel, lags=LAGS, output_chunk_length=OUTPUT_CHUNK)
    lgbm_smapes, lgbm_time = eval_global_model(train_pricing, val_pricing, LightGBMModel, lags=LAGS, output_chunk_length=OUTPUT_CHUNK, objective="mape")
    rf_smapes, rf_time = eval_global_model(train_pricing, val_pricing, RandomForest, lags=LAGS, output_chunk_length=OUTPUT_CHUNK)
    # create year, month and integer index covariate series
    cov_date = datetime_attribute_timeseries(series_pricing, attribute="month", one_hot=False)
    cov_date = cov_date.stack(
        datetime_attribute_timeseries(series_pricing, attribute="day", one_hot=False)
    )
    cov_date = cov_date.stack(covariates_demand_transformed)
    cov_date = cov_date.astype(np.float32)
    # transform covariates (note: we fit the transformer on train split and can then transform the entire covariates series)
    scaler_covs = Scaler(scaler=MaxAbsScaler())
    cov_train, cov_val = cov_date.split_after(get_cut_off_time(cov_date))
    scaler_covs.fit(cov_train)
    covariates_transformed = scaler_covs.transform(cov_date)
    
    #build tft model build_tft_with_opt_weights() / build_tft_def_weights()
    tft_model = build_tft_with_opt_weights()
    print(tft_model._model_params)
    tft_model.fit(train_pricing_transformed, future_covariates=covariates_transformed, epochs=180)
    
    start_time = time.time()
    # get predictions
    tft_preds = tft_model.predict(series=train_pricing_transformed, n=DAY_DURATION, future_covariates=covariates_transformed)

    tft_elapsed_time = time.time() - start_time
    tft_smapes = eval_forecasts(tft_preds, train_pricing_transformed, val_pricing_transformed, tft_elapsed_time)
    
    smapes_2 = {
        "Linear Regression": lr_smapes,
        "LGBM": lgbm_smapes,
        "Random Forest": rf_smapes,
        "TFT": tft_smapes,
        }
    elapsed_times_2 = {
        "Linear Regression": lr_time,
        "LGBM": lgbm_time,
        "Random Forest": rf_time,
        "TFT": tft_elapsed_time,
        }
    
    # plot models for analysis
    plot_models(elapsed_times_2, smapes_2)


# using default weights
def build_tft_def_weights():
    tft_model = TFTModel(
        input_chunk_length=LAGS,
        output_chunk_length=OUTPUT_CHUNK
    )
    return tft_model


def build_tft_with_opt_weights():
    tft_model = TFTModel.load("./electricity_model.pt")
    tft_model._model_params['input_chunk_length'] = LAGS
    tft_model._model_params['output_chunk_length'] = OUTPUT_CHUNK
    
    tft_model._model_params['batch_size'] = 128
    tft_model._model_params['optimizer_kwargs']={'lr':0.000001}
    return tft_model

def load_electricity_data(selected_type):
    # Make data
    # Create list to store all file names with half-hourly records
    li =[]
    for name in glob.glob('./data/*.csv'):
        df = pd.read_csv(name, index_col=None, header=0, parse_dates=["DATE"])
        li.append(df)
    # merge all records
    ds = pd.concat(li, axis=0, ignore_index=True).drop([ "INFORMATION TYPE", "LCP ($/MWh)", "TCL (MW)", "TCL(MW)" , "SOLAR(MW)"], axis='columns')

    len(ds. index) 
    interval = 30

    # Because we want hourly records, we manipulate data to get the average price/hour 
    rows_to_drop = [] # list to store all records to be dropped
    print("Manipulating data...")
    for i in range(len(ds. index)):
            # convert string to datetime object
        d = ds.at[i, "DATE"]
        result = d + timedelta(minutes=interval*(i%48))
        ds.at[i, "DATE"] = result
        
        if(selected_type == "Hourly"):
            if i%2==0:
                ds.at[i, "USEP ($/MWh)"] = (ds.at[i, "USEP ($/MWh)"] + ds.at[i+1, "USEP ($/MWh)"])/2    # get the average price/hour 
                ds.at[i,"DEMAND (MW)"] = (ds.at[i, "DEMAND (MW)"] + ds.at[i+1, "DEMAND (MW)"])/2    # get the average demand
            else:
                rows_to_drop.append(int(i))
        elif(selected_type == "Daily"):
            p_accumulator = 0
            d_accumulator = 0
            if i %48==0:
                for k in range(48):
                    p_accumulator = p_accumulator + ds.at[i+k, "USEP ($/MWh)"]
                    d_accumulator = d_accumulator + ds.at[i+k, "DEMAND (MW)"]
                    if k == 47:
                        ds.at[i+k, "USEP ($/MWh)"] = p_accumulator/48
                        ds.at[i+k, "DEMAND (MW)"]= d_accumulator/48
                    else:
                        rows_to_drop.append(int(i+k))

    ds = ds.drop(rows_to_drop)   # drop all even records
    ds = ds.reset_index(drop=True)
        
    series = TimeSeries.from_dataframe(ds, time_col = 'DATE' , value_cols =['USEP ($/MWh)', 'DEMAND (MW)']) # convert to timeseries
    converted_series = []
    for col in ["USEP ($/MWh)", "DEMAND (MW)"]:
        converted_series.append(
            series[col]
        )
    converted_series = concatenate(converted_series, axis=1)
    
    series_pricing = converted_series["USEP ($/MWh)"].astype(np.float32)
    covariates_demand = converted_series["DEMAND (MW)"].astype(np.float32)
    
    return series_pricing, covariates_demand

def transform_target(target_series):
    
    training_cutoff = get_cut_off_time(target_series)

    # use electricity pricing as target, create train and validation sets and transform data
    transformer_pricing = Scaler(scaler=MaxAbsScaler())
    train_pricing, val_pricing = target_series.split_before(training_cutoff)

    train_pricing_transformed = transformer_pricing.fit_transform(train_pricing)
    val_pricing_transformed = transformer_pricing.transform(val_pricing)
    series_pricing_transformed = transformer_pricing.transform(target_series)
    
    return train_pricing, val_pricing, train_pricing_transformed, val_pricing_transformed, series_pricing_transformed
    
    
def transform_covariate(cov_series):
    training_cutoff = get_cut_off_time(cov_series)
    
    # use electricity demand as past covariates and transform data
    cov_demand_train, cov_demand_val = cov_series.split_before(training_cutoff)
    transformer_demand = Scaler(scaler=MaxAbsScaler())
    transformer_demand.fit(cov_demand_train)
    covariates_demand_transformed = transformer_demand.transform(cov_series)
    
    return cov_demand_train, cov_demand_val, covariates_demand_transformed


def get_cut_off_time(series):
    print(f"length to predict: {OUTPUT_CHUNK}")
    # define train/validation cutoff time
    training_cutoff_pricing = series.time_index[-OUTPUT_CHUNK]
    print(f'training cutoff: {training_cutoff_pricing}')
    return training_cutoff_pricing


def eval_global_model(train_series, test_series, model_cls, **kwargs):
    start_time = time.time()
    model = model_cls(**kwargs)
    model.fit(train_series)
    preds = model.predict(n=OUTPUT_CHUNK, series=train_series)

    elapsed_time = time.time() - start_time

    smapes = eval_forecasts(preds, train_series, test_series, elapsed_time)
    return smapes, elapsed_time

def eval_local_model(
    train_series, test_series, model_cls, **kwargs):
    start_time = time.time()
    model = model_cls(**kwargs)
    model.fit(train_series)
    pred = model.predict(n=OUTPUT_CHUNK)

    elapsed_time = time.time() - start_time

    smapes = eval_forecasts(pred, train_series, test_series, elapsed_time)
    return smapes, elapsed_time

def eval_forecasts(
    pred_series,train_series, test_series, time):

    print("computing sMAPEs...")
    smapes = smape(test_series, pred_series)
    fig = plt.figure(figsize=(15, 5))
    train_series[-7 * DAY_DURATION :].plot()
    test_series.plot(label="actual")
    pred_series.plot(label="forecast")
    plt.title("sMAPE: {}".format(smapes))
    fig.savefig("models/{}, {}.png".format(smapes, time))
    plt.show()
    plt.close()
    return smapes

def plot_models(method_to_elapsed_times, method_to_smapes):
    shapes = ["o", "s", "*"]
    colors = ["tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple"]
    styles = list(product(shapes, colors))

    plt.figure(figsize=(6, 6))
    for i, method in enumerate(method_to_elapsed_times.keys()):
        t = method_to_elapsed_times[method]
        s = styles[i]
        plt.semilogx(
            [t],
            [np.median(method_to_smapes[method])],
            s[0],
            color=s[1],
            label=method,
            markersize=13,
        )
    plt.xlabel("elapsed time [s]")
    plt.ylabel("median sMAPE over all series")
    plt.legend(bbox_to_anchor=(0.7, 1.0), frameon=True)
    plt.savefig("models/models1.png")
    



class LossLogger(Callback):
    def __init__(self):
        self.train_loss = []
        self.val_loss = []

        # will automatically be called at the end of each epoch
    def on_train_epoch_end(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule") -> None:
        self.train_loss.append(float(trainer.callback_metrics["train_loss"]))
            # will automatically be called at the end of each epoch
    def on_validation_epoch_end(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule") -> None:
        if not trainer.sanity_checking:
            self.val_loss.append(float(trainer.callback_metrics["val_loss"]))
   
evaluate_pipeline()

