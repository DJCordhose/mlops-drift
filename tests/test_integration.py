from fastapi.testclient import TestClient

from insurance_prediction.app.application.dto import *
from insurance_prediction.app.main import app
from insurance_prediction.model import InsurancePredictor
from insurance_prediction.app.usecase import insurance
from insurance_prediction.monitoring.data_drift import window_size

client = TestClient(app)

window_size = 1

class _MockPredictor(InsurancePredictor):
    def can_predict(self, prediction_input: RiskPredictionInput) -> bool:
        return True

    def predict(self, prediction_input: RiskPredictionInput) -> Prediction:
        self.prediction_input = prediction_input
        return Prediction(
            prediction=Risk.LOW,
            probabilities = None,
            predictor_type=PredictorType.MODEL
        )


def test_prediction():
    # arrange
    mock_model = _MockPredictor()
    insurance.insurance_model = mock_model

    prediction_input = RiskPredictionInputDto(
        driver = DriverInformationDto(
            age=35,
            training=True,
            miles=45.9
        ),
        vehicle = VehicleInformationDto(
            braking_distance=45.,
            power=90.,
            emergency_braking=False            
        )
    )

    # then
    response = client.post('/predict', content=prediction_input.json())

    # assert
    assert response.status_code == 200
    assert mock_model.prediction_input == prediction_input.to_domain()


def test_metrics():
    # arrange
    mock_model = _MockPredictor()
    insurance.insurance_model = mock_model

    prediction_input = RiskPredictionInputDto(
        driver = DriverInformationDto(
            age=35,
            training=True,
            miles=45.9
        ),
        vehicle = VehicleInformationDto(
            braking_distance=45.,
            power=90.,
            emergency_braking=False            
        )
    )

    # then
    client.post('/predict', content=prediction_input.json())
    response = client.get('/metrics')

    # assert
    assert response.status_code == 200
    assert len(response.text) > 0

