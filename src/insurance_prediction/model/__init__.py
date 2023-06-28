from abc import abstractmethod

from insurance_prediction.model.domain.insurance import Prediction, RiskPredictionInput

class InfeasiblePredictionError(Exception):
    ...

class InsurancePredictor:
    @abstractmethod
    def can_predict(self, prediction_input: RiskPredictionInput) -> bool:
        """ Checks if the given predictor can predict tine given input.

        Args:
            prediction_input (RiskPredictionInput): The input for the risk prediction, 
                                                    contains information about the client
                                                    and his vehicle.

        Returns:
            Boolean: if the predictor is compatible with the given input data.
        """
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def predict(self, prediction_input: RiskPredictionInput) -> Prediction:
        """ Predicts the risk for a possible insurance client based on some risk related features.

        Args:
            prediction_input (RiskPredictionInput): The input for the risk prediction, 
                                                    contains information about the client
                                                    and his vehicle.

        Returns:
            Prediction: The result of the prediction
        
        Raises:
            InfeasiblePredictionError: In case the input is out of range for the given model or it's
                                       not feasible to predict based on it.
        """
        raise NotImplementedError("Not implemented")
