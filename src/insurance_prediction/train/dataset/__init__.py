from dataclasses import dataclass
import tensorflow as tf

@dataclass
class Dataset:
    num_features: int
    train: tf.data.Dataset
    test: tf.data.Dataset
