from pytorch_lightning.callbacks import Callback
import pytorch_lightning as pl

class LossLogger(Callback):
    def __init__(self):
        self.train_loss = []

        # will automatically be called at the end of each epoch
    def on_train_epoch_end(self, trainer: "pl.Trainer", pl_module: "pl.LightningModule") -> None:
        self.train_loss.append(float(trainer.callback_metrics["train_loss"]))
            # will automatically be called at the end of each epoch
