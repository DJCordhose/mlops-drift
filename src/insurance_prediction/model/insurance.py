import logging
import os
from typing import Optional
import tensorflow as tf

from insurance_prediction.model import InsurancePredictor, InfeasiblePredictionError
from insurance_prediction.model.domain.insurance import Prediction, PredictorType, Risk, RiskPredictionInput

class _InsuranceModel(InsurancePredictor):
    logger = logging.getLogger('insurance_model')

    def __init__(self, model_path: str,
                 min_probability_threshold = .5,
                 age_range = range(10, 150),
                 power_range = range(50, 250)) -> None:
        super().__init__()
        self.age_range = age_range
        self.power_range = power_range
        self.min_probability_threshold = min_probability_threshold

        self.model = tf.keras.models.load_model(model_path)

    def can_predict(self, prediction_input: RiskPredictionInput) -> bool:
        in_range = prediction_input.driver.age in self.age_range and int(prediction_input.vehicle.power) in self.power_range
        if not in_range:
            _InsuranceModel.logger.warning('Input out of range for ML model - falling back to baseline model')
        return in_range

    def predict(self, prediction_input: RiskPredictionInput) -> Prediction:
        if not self.can_predict(prediction_input):
            raise InfeasiblePredictionError(f'Prediction input {prediction_input} is \
                out of range age_range={self.age_range}, power_range={self.power_range}.')

        model_input = [
            [int(prediction_input.driver.training),
             prediction_input.driver.age,
             int(prediction_input.vehicle.emergency_braking),
             prediction_input.vehicle.braking_distance,
             prediction_input.vehicle.power,
             prediction_input.driver.miles]
        ]
        result = self.model.predict(model_input, verbose=0)[0]

        if result.max() < self.min_probability_threshold:
            _InsuranceModel.logger.warning('ML model confidence %.2f too low - falling back to baseline model', result.max())
            raise InfeasiblePredictionError(f'Result of model is not confident enough, as it is below {self.min_probability_threshold}')

        return Prediction(
            prediction=Risk.of(result.argmax()),
            probabilities={Risk.of(i): p for i, p in enumerate(result)},
            predictor_type=PredictorType.MODEL
        )

def load_model(model_path: str = os.getenv('MODEL_PATH')) -> InsurancePredictor:
    if model_path is None:
        return None

    return _InsuranceModel(
        model_path = model_path
    )
