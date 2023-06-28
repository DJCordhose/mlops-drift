
from dataclasses import dataclass
from enum import auto, Enum
from typing import Any, Dict, Optional

@dataclass
class DriverInformation:
    training: bool
    age: int
    miles: float

@dataclass
class VehicleInformation:
    emergency_braking: bool
    braking_distance: float
    power: float

@dataclass
class RiskPredictionInput:
    driver: DriverInformation
    vehicle: VehicleInformation

class PredictorType(Enum):
    MODEL = auto()
    RULES = auto()

class Risk(Enum):
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()

    @classmethod
    def of(cls, value: int):
        return [Risk.HIGH, Risk.MEDIUM, Risk.LOW][value]

@dataclass
class Prediction:
    prediction: Risk
    probabilities: Optional[Dict[Risk, float]]
    predictor_type: PredictorType
