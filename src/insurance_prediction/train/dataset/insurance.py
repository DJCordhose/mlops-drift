from pathlib import Path

import pandas as pd
import tensorflow as tf

from insurance_prediction.train.dataset import Dataset

def load_dataset(train_csv_path: Path, test_csv_path: Path) -> Dataset:
    train_df = pd.read_csv(train_csv_path, sep=';')
    test_df = pd.read_csv(test_csv_path, sep=';')
    return Dataset(
        num_features=len(train_df.columns) - len(['risk','group','group_name']),
        train=_load_dataset_from_df(train_df),
        test=_load_dataset_from_df(test_df)
    )

def _load_dataset_from_df(df: pd.DataFrame) -> tf.data.Dataset:
    features = df.drop(['risk', 'group', 'group_name'], axis='columns').values
    label = df.pop('group')

    feature_dataset = tf.data.Dataset.from_tensor_slices(features)
    label_dataset = tf.data.Dataset.from_tensor_slices(label)

    return tf.data.Dataset.zip((feature_dataset, label_dataset))
