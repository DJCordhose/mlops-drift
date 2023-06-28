from insurance_prediction.model import InfeasiblePredictionError
from insurance_prediction.model.domain.insurance import Prediction, RiskPredictionInput
from insurance_prediction.model.insurance import load_model as load_insurance_model
from insurance_prediction.model.rule_based import load_model as load_rule_based_model
import insurance_prediction.monitoring.data_drift as data_drift

insurance_model = load_insurance_model()
rule_based_model = load_rule_based_model()

@data_drift.risk_prediction
def predict_risk(prediction_input: RiskPredictionInput) -> Prediction:
    try:
        if insurance_model.can_predict(prediction_input):
            return insurance_model.predict(prediction_input)
        else:
            return rule_based_model.predict(prediction_input)
    except InfeasiblePredictionError:
        return rule_based_model.predict(prediction_input)

@data_drift.risk_prediction
def predict_mock(_: RiskPredictionInput) -> None:
    """ Mocks the prediction by just receiving the input.
        This is used only for the monitoring show-case where
        we don't want to predict every single input element.
    """
