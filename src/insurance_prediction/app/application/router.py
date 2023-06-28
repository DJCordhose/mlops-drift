from fastapi import APIRouter

from insurance_prediction.app.application.dto import PredictionDto, RiskPredictionInputDto
from insurance_prediction.app.usecase.insurance import predict_risk, predict_mock

router = APIRouter(
    prefix='/predict'
)

@router.post(path='/', response_model=PredictionDto)
async def post_predict_risk(prediction_input: RiskPredictionInputDto) -> PredictionDto:
    prediction = predict_risk(prediction_input.to_domain())
    return PredictionDto.from_domain(prediction)

@router.post(path='/mock', response_model=None, include_in_schema=False)
async def post_predict_mock(prediction_input: RiskPredictionInputDto) -> PredictionDto:
    predict_mock(prediction_input.to_domain())
