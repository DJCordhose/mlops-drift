from dataclasses import dataclass

import tensorflow as tf


@dataclass
class Evaluation:
    loss: float
    accuracy: float

def evaluate(model: tf.keras.Model, dataset: tf.data.Dataset, batch_size: int = 32) -> Evaluation:
    loss, metric = model.evaluate(dataset.batch(batch_size), verbose=0)
    return Evaluation(loss, metric)
