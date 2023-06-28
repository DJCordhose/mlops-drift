import argparse
from pathlib import Path
from time import sleep

import pandas as pd

from insurance_prediction.app.application.dto import DriverInformationDto, RiskPredictionInputDto, VehicleInformationDto

from httpx import Client as HttpClient

def main():
    parser = argparse.ArgumentParser(
        description="Drift-Simulation Script"
    )

    parser.add_argument(
        "--dataset",
        type=str,
        metavar='DIRECTORY',
        required=True,
        help="Path to the dataset folder"
    )

    parser.add_argument(
        "--base_url",
        type=str,
        metavar='DIRECTORY',
        help="Path to the dataset folder",
        default="http://localhost:8000/"
    )

    parser.add_argument(
        "--timeout",
        type=int,
        help="Timeout between each batch in seconds",
        default=0
    )

    args = parser.parse_args()
    timeout = int(args.timeout)

    dataset_path = Path(args.dataset)

    with HttpClient(base_url=args.base_url) as http_client:
        months = dataset_path.glob('monthly/*.csv.gz')
        months = sorted(months, key=lambda path: int(path.name[len('month-'):-len('.csv.gz')]))

        for month in months:
            df = pd.read_csv(month, delimiter=';')
            print(month)
            for _, row in df.iterrows():
                prediction_input = RiskPredictionInputDto(
                    driver=DriverInformationDto(
                        age=int(row['age']),
                        training=bool(row['training']),
                        miles=float(row['miles'])
                    ),
                    vehicle=VehicleInformationDto(
                        emergency_braking=bool(row['emergency_braking']),
                        power=float(row['power']),
                        braking_distance=float(row['braking_distance'])
                    )
                )
                
                http_client.post('/predict/mock', content=prediction_input.json())
            sleep(timeout)