import warnings

warnings.filterwarnings("ignore")

import pickle
import wandb
import numpy as np
import pytorch_lightning as pl
import matplotlib.pyplot as plt

from pytorch_lightning.callbacks import Callback, EarlyStopping
from sklearn.preprocessing import MaxAbsScaler
from darts.models import *
from darts.dataprocessing.transformers import Scaler
from darts.utils.timeseries_generation import datetime_attribute_timeseries
from darts.metrics import *
from darts import TimeSeries
from pytorch_lightning.callbacks import EarlyStopping

# callback function to load train_loss and val_loss in wandb for analysis
class LossLogger(Callback):
    def __init__(self):
        self.train_loss = []
        self.val_loss = []

        # will automatically be called at the end of each epoch
    def on_train_epoch_end(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule") -> None:
        self.train_loss.append(float(trainer.callback_metrics["train_loss"]))
        wandb.log({"train_loss": float(trainer.callback_metrics["train_loss"])})
            # will automatically be called at the end of each epoch
    def on_validation_epoch_end(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule") -> None:
        if not trainer.sanity_checking:
            self.val_loss.append(float(trainer.callback_metrics["val_loss"]))
            wandb.log({"val_loss": float(trainer.callback_metrics["val_loss"])})
   
    # throughout training we'll monitor the validation loss for early stopping to prevent overfitting
early_stopper = EarlyStopping("val_loss", min_delta=0.001, patience=3, verbose=True)
loss_logger = LossLogger()



NR_DAYS = 90
DAY_DURATION = 24
DAY_PREDICT = 1     # Number of days we want to predict ahead
OUTPUT_CHUNK = DAY_PREDICT * DAY_DURATION   #predict n day ahead as test
WINDOW = 7 * DAY_DURATION
num_samples = 200

new_dataset = []
counter1 = 0
with open('electric_dataset.pickle', 'rb') as data:
    dataset = pickle.load(data)    
for s in dataset:
    df = s.pd_dataframe()
    df = df.reset_index()
    df = df.tail(NR_DAYS * DAY_DURATION)
    t_series = TimeSeries.from_dataframe(df, time_col = 'date' , value_cols ='power_usage')
    t_series.astype(np.float32)
    new_dataset.append(t_series)


print(new_dataset)

new_dataset = new_dataset

train = [s[: -(1 * OUTPUT_CHUNK)] for s in new_dataset]
val = [s[-(1 * OUTPUT_CHUNK) : ] for s in new_dataset]
# Scale so that the largest value is 1.
# This way of scaling perserves the sMAPE
scaler = Scaler(scaler=MaxAbsScaler())
train_transformed = scaler.fit_transform(train)
val_transformed = scaler.transform(val)



def eval_model(preds, name, train_set=train, val_set=val):
    smapes = smape(preds, val_set)
    print("{} sMAPE: {:.2f} +- {:.2f}".format(name, np.mean(smapes), np.std(smapes)))
    
    fig = plt.figure(figsize=(15, 5))
    train_set[-7 * DAY_DURATION :].plot()
    val_set.plot(label="actual")
    preds.plot(label="forecast")
    plt.title("MAPE: {:.2f}".format(mape(val_set, preds)))
    fig.savefig('electricity_test.png')
    # wandb.log({'Chart' : wandb.Image(fig), 'smape' : np.mean(smapes) , "smape +-":np.std(smapes)})
    
    
def eval_model(preds, name, train_set, val_set):
    smapes = smape(preds, val_set)
    print("{} sMAPE: {:.2f} +- {:.2f}".format(name, np.mean(smapes), np.std(smapes)))

    for i in preds:
        plt.figure(figsize=(15, 5))
        train_set[i][-7 * DAY_DURATION :].plot()
        val_set[i].plot(label="actual")
        preds[i].plot(label="forecast")

# generate future covariates
covs = []
for s in new_dataset:
    cov = datetime_attribute_timeseries(t_series, attribute="month", one_hot=False)
    cov = cov.stack(datetime_attribute_timeseries(t_series, attribute="day", one_hot=False))
    cov = cov.astype(np.float32)
    # transform covariates (note: we fit the transformer on train split and can then transform the entire covariates series)
    scaler_covs = Scaler(scaler=MaxAbsScaler())
    cov_train = cov[: -OUTPUT_CHUNK]
    scaler_covs.fit(cov_train)
    covariates_transformed = scaler_covs.transform(cov)
    covs.append(covariates_transformed)





my_model = TFTModel(
    input_chunk_length=WINDOW,
    output_chunk_length=OUTPUT_CHUNK,
    hidden_size=32,
    lstm_layers=1,
    batch_size=256,
    n_epochs=60,
    dropout=0.1,
    add_encoders={"cyclic": {"future": ["month", "day"]}},
    add_relative_index=False,
    optimizer_kwargs={"lr": 1e-4},
    random_state=42,
)

# fit the model with past covariates
my_model.fit(
    train_transformed, verbose=True
)
model_val_set = scaler.transform(
        t_series[-((2 * my_model._model_params['output_chunk_length']) + my_model._model_params['input_chunk_length']) : -my_model._model_params['output_chunk_length']]
    ) # target series must have at least input_chunk_length + output_chunk_length time steps
model_val_cov = covariates_transformed[-((2 * my_model._model_params['output_chunk_length']) + my_model._model_params['input_chunk_length'] ) : -my_model._model_params['output_chunk_length']]

with wandb.init(project="Electricity Prices", config = None):
    config = wandb.config
    my_model._model_params['batch_size'] = config.batch_size
    my_model._model_params['optimizer_kwargs']={'lr':config.learning_rate}
    my_model.fit(series =train_transformed, verbose=True,  future_covariates=covariates_transformed, epochs = config.epochs, val_future_covariates = model_val_cov, val_series =model_val_set )

preds = my_model.predict(series=train, n=OUTPUT_CHUNK , num_samples=num_samples, future_covariates=covariates_transformed)
eval_model(preds, "wandb TFT model",  train_set=train_transformed, val_set=val_transformed)


