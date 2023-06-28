from enum import auto
from typing import Dict, Optional

from pydantic import BaseModel
from strenum import StrEnum

from insurance_prediction.model.domain.insurance import (DriverInformation,
                                                         Prediction,
                                                         PredictorType, Risk,
                                                         RiskPredictionInput,
                                                         VehicleInformation)

class PredictorTypeDto(StrEnum):
    MODEL = auto()
    RULES = auto()

    @classmethod
    def from_domain(cls, obj: PredictorType) -> 'PredictorTypeDto':
        return PredictorTypeDto[obj.name]

class RiskDto(StrEnum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()

    @classmethod
    def from_domain(cls, obj: Risk) -> 'RiskDto':
        return RiskDto[obj.name]

class PredictionDto(BaseModel):
    prediction: RiskDto
    probabilities: Optional[Dict[RiskDto, float]]
    predictor_type: PredictorTypeDto

    @classmethod
    def from_domain(cls, obj: Prediction) -> 'PredictionDto':
        return PredictionDto(
            prediction=RiskDto.from_domain(obj.prediction),
            probabilities={RiskDto.from_domain(risk): p for risk, p in obj.probabilities.items()} if obj.probabilities is not None else None,
            predictor_type=PredictorTypeDto.from_domain(obj.predictor_type)
        )

class DriverInformationDto(BaseModel):
    training: bool
    age: int
    miles: float

    def to_domain(self) -> DriverInformation:
        return DriverInformation(
            training=self.training,
            age=self.age,
            miles=self.miles
        )

class VehicleInformationDto(BaseModel):
    emergency_braking: bool
    braking_distance: float
    power: float

    def to_domain(self) -> VehicleInformation:
        return VehicleInformation(
            emergency_braking=self.emergency_braking,
            braking_distance=self.braking_distance,
            power=self.power
        )

class RiskPredictionInputDto(BaseModel):
    driver: DriverInformationDto
    vehicle: VehicleInformationDto

    def to_domain(self) -> RiskPredictionInput:
        return RiskPredictionInput(
            driver=self.driver.to_domain(),
            vehicle=self.vehicle.to_domain()
        )
