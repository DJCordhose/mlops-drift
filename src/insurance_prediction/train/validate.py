import argparse
import os
from pathlib import Path
from typing import Union

import numpy as np
import tensorflow as tf

from insurance_prediction.train.dataset.insurance import \
    load_dataset
from insurance_prediction.train.evaluation import evaluate


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Validation Script'
    )
    parser.add_argument(
        '--dataset',
        type=str,
        metavar='DIRECTORY',
        required=True,
        help='Path to the dataset directory'
    )
    parser.add_argument(
        '--model',
        type=str,
        required=True,
        help='Path to the trained model'
    )

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    tf.config.set_visible_devices([], 'GPU')

    args = parser.parse_args()

    dataset_path = Path(args.dataset)
    model_path = Path(args.model)

    dataset = load_dataset(
        train_csv_path = dataset_path / 'train.csv.gz',
        test_csv_path = dataset_path / 'test.csv.gz'
    )
    model: Union[None, tf.keras.Model] = tf.keras.models.load_model(model_path)
    if model is None:
        raise ValueError(f"Failed to load model from file {model_path}")

    # Basic metrics
    print('Checking basic metrics')

    train_evaluation = evaluate(model, dataset.train)
    test_evaluation = evaluate(model, dataset.test)

    train_metric = train_evaluation.accuracy
    test_metric = test_evaluation.accuracy

    print(
        f'Model train / test accuracy: {train_metric} / {test_metric}')

    assert train_metric > .85
    print(f'Model train accuracy of {train_metric} exceeds 85%')
    assert test_metric > .85
    print(f'Model test accuracy of {test_metric} exceeds 85%')
    assert abs(train_metric - test_metric) < .05
    print(
        f'Accuracy spread of {abs(train_metric - test_metric)} is below 5% (checking or overfitting here)')

    # Output distributions
    print('Checking output distribution')

    X = dataset.train.concatenate(dataset.test).map(lambda x, y: x)
    y_pred = model.predict(X, verbose=0).argmax(axis=1)
    _, counts = np.unique(y_pred, return_counts=True)

    # Equal distribution around classes expected
    tolerance = 0.20
    expected_count = len(X) / 3
    lower_bound = int(expected_count * (1 - tolerance))
    upper_bound = int(expected_count * (1 + tolerance))
    print(f'Counts should be within {lower_bound}-{upper_bound}')
                  
    for count in counts:
        print(count)
        assert count in range(lower_bound, upper_bound)
    print(f'Counts {counts} are within {tolerance} of {expected_count}')

    # Certainty distribution
    min = .4
    mean = 0.7
    max = 0.99
    print(f'Checking certainty distribution of outputs is within expected bounds min: {min}, mean: {mean}, max: {max}')
    y_pred_probas = model.predict(X, verbose=0).max(axis=1)
    print(
        f'Min: {y_pred_probas.min()}, mean: {y_pred_probas.mean()}, max: {y_pred_probas.max()}')
    assert y_pred_probas.min() > min
    assert y_pred_probas.mean() > mean
    assert y_pred_probas.max() > max
