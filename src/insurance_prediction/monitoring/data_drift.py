import os
from evidently.metrics import DatasetDriftMetric
from evidently.base_metric import InputData, ColumnMapping
from evidently.runner.loader import DataLoader, DataOptions
from evidently.calculations.data_drift import get_drift_for_columns
from evidently.options import DataDriftOptions
from evidently.utils.data_operations import process_columns

from collections import deque
from typing import Any, Callable, Dict, MutableMapping, MutableSequence, Sequence

import pandas as pd
from prometheus_client import Gauge
from insurance_prediction.model.domain.insurance import Prediction, RiskPredictionInput

from insurance_prediction.monitoring import collector_registry

reference_path: str = os.getenv('REFERENCE_PATH')
window_size: int = int(os.getenv('METRICS_WINDOW_SIZE', '1500'))


reference_dataset = DataLoader().load(
   filename=reference_path,
   data_options = DataOptions(date_column=None, separator=';'),
)
reference_dataset = reference_dataset.drop(['risk', 'group', 'group_name'], axis='columns')

column_mapping = ColumnMapping(
    categorical_features=['training', 'emergency_braking'],
    numerical_features=['age', 'braking_distance', 'power', 'miles'],
    prediction=None,
    target=None,
)
columns = column_mapping.categorical_features + column_mapping.numerical_features
drift_share = 0.5

window: MutableSequence[RiskPredictionInput] = deque(maxlen=int(window_size))
gauges: MutableMapping[str, Gauge] = dict()

number_of_columns_gauge = Gauge('number_of_columns', '', registry=collector_registry)
number_of_drifted_columns_gauge = Gauge('number_of_drifted_columns', '', registry=collector_registry)
share_of_drifted_columns_gauge = Gauge('share_of_drifted_columns', '', registry=collector_registry)
dataset_drift_gauge = Gauge('dataset_drift', '', registry=collector_registry)
drift_score_by_columns_gauge = Gauge('drift_score_by_columns', '', ['feature'], registry=collector_registry)

requests_in_windows_gauge = Gauge('requests_in_windows', '', registry=collector_registry)

def _to_dataframe(current_data: Sequence[RiskPredictionInput]) -> pd.DataFrame:
    def _to_dict(risk_input: RiskPredictionInput) -> Dict[str, Any]:
        return {
            'training': int(risk_input.driver.training),
            'emergency_braking': int(risk_input.vehicle.emergency_braking),
            'age': risk_input.driver.age,
            'braking_distance': risk_input.vehicle.braking_distance,
            'power': risk_input.vehicle.power,
            'miles': risk_input.driver.miles
        }

    current_data = list(map(_to_dict, current_data))
    return pd.DataFrame.from_records(current_data)


def risk_prediction(fun: Callable[[RiskPredictionInput], Prediction]) -> Callable[[RiskPredictionInput], Prediction]:
    def _wrapper(prediction_input: RiskPredictionInput) -> Prediction:
        prediction = fun(prediction_input)
        window.append(prediction_input)
        requests_in_windows_gauge.set(len(window))
        if len(window) >= window_size:
            input_data = InputData(
                reference_data=reference_dataset.copy(),
                current_data=_to_dataframe(window),
                column_mapping=column_mapping,
                current_additional_features=None,
                data_definition=None,
                reference_additional_features=None
            )
            window.clear()

            dataset_columns = process_columns(input_data.reference_data, input_data.column_mapping)
            result = get_drift_for_columns(
                current_data=input_data.current_data,
                reference_data=input_data.reference_data,
                data_drift_options=DataDriftOptions(),
                drift_share_threshold=drift_share,
                dataset_columns=dataset_columns,
                columns=column_mapping.categorical_features + column_mapping.numerical_features,
            )

            number_of_columns_gauge.set(result.number_of_columns)
            number_of_drifted_columns_gauge.set(result.number_of_drifted_columns)
            share_of_drifted_columns_gauge.set(result.share_of_drifted_columns)
            dataset_drift_gauge.set(result.dataset_drift)

            for column in columns:
                drift = result.drift_by_columns[column]
                drift_score_by_columns_gauge.labels(feature = column).set(drift.drift_score,)

        return prediction
    return _wrapper
