import torch
import random
import requests
import json
import pandas as pd
import numpy as np

from pytorch_lightning.callbacks import Callback, EarlyStopping
from sklearn.preprocessing import MaxAbsScaler

from darts.models import TFTModel
from darts.dataprocessing.transformers import Scaler
from darts.metrics import smape
from darts.utils.likelihood_models import GaussianLikelihood
from darts.utils.timeseries_generation import datetime_attribute_timeseries
from darts import TimeSeries

from loss_logger import LossLogger


# declaring some constants
NR_DAYS = 90
DAY_DURATION = 24  # hour frequency
WINDOW = 7 * DAY_DURATION  # 7 days
HORIZON = 1 * DAY_DURATION  # 1 day
EPOCHS = 60
IP_ADDRESS = '192.168.18.12'

def pipeline():
    #get all ev charger id
    id_chargers = get_id_chargers()

    for id_charger in id_chargers:
        # get data
        data = get_data(id_charger['id'])

        # split training and val dataset
        train = data[:-HORIZON]

        # Scale so that the largest value is 1.
        # This way of scaling perserves the sMAPE
        scaler = Scaler(scaler=MaxAbsScaler())
        train_transformed = scaler.fit_transform(train)

        # generate future covariates
        cov = datetime_attribute_timeseries(data, attribute="month", one_hot=False)
        cov = cov.stack(datetime_attribute_timeseries(data, attribute="day", one_hot=False))
        cov = cov.astype(np.float32)

        # transform covariates (note: we fit the transformer on train split and can then transform the entire covariates series)
        scaler_covs = Scaler(scaler=MaxAbsScaler())
        cov_train = cov[: -HORIZON]
        scaler_covs.fit(cov_train)
        covariates_transformed = scaler_covs.transform(cov)

        # create model
        model = TFTModel.load('electricity_model.pt')

        # train model
        model.fit(train_transformed, verbose=True, future_covariates=covariates_transformed, epochs=EPOCHS)

        # predict
        prediction = model.predict(series = train_transformed, n=HORIZON, future_covariates=covariates_transformed)

        # reverse transform
        reversed_pred = scaler.inverse_transform(prediction)
        pred_arr = reversed_pred.pd_dataframe().to_numpy().flatten()
        pred_arr = [round(x, 2) for x in pred_arr]
        print(pred_arr)

        # save data in db
        data = {
            "id": id_charger['id'],
            "rate_predicted": json.dumps(pred_arr)
        }
        headers = {'Content-Type':"application/json"}
        response = requests.post("http://{}:5000/api/update_charger".format(IP_ADDRESS), data=json.dumps(data), headers=headers)           
        print(response.text)


def get_id_chargers():
    req = requests.get("http://{}:5000/api/get_all_charger_ids".format(IP_ADDRESS), headers={'Content-Type':"application/json"})
    data = json.loads(req.content)
    return data['data']



def get_data(id_charger):
    print("manipulating data...")

    req = requests.get("http://{}:5000/api/get_all_past_charger_rates".format(IP_ADDRESS), params={'id_charger': id_charger}, headers={'Content-Type':"application/json"})
    data = json.loads(req.content)
    
    length = len(data['data'])

    df = pd.DataFrame(data['data'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    #     df  =df.resample('H', on='timestamp', closed='right').mean()
    if(length > NR_DAYS * DAY_DURATION):
        df = df.tail(NR_DAYS * DAY_DURATION)

    t_series = TimeSeries.from_dataframe(df, time_col = 'timestamp' , value_cols ='rate')
    t_series.astype(np.float32)

    
    print(t_series)
    print("data manipulation done!")
    return t_series


pipeline()




