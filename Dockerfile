FROM ghcr.io/habecker/tensorflow_poetry:py3.10.11-tf2.12.0-slim AS base
COPY ./ /insurance_prediction
WORKDIR /insurance_prediction
RUN poetry install
RUN REFERENCE_PATH=./datasets/insurance_prediction/reference.csv.gz pytest -q
RUN pylint --fail-under=9 ./src ./tests

FROM base AS build
RUN poetry build
RUN poetry export -f requirements.txt --output ./requirements.txt

FROM base AS training
COPY ./datasets/insurance_prediction/reference.csv.gz /
RUN poetry run train --dataset ./datasets/insurance_prediction/ --model /model.h5
RUN poetry run validate --dataset ./datasets/insurance_prediction/ --model /model.h5

FROM ghcr.io/habecker/tensorflow_poetry:py3.10.11-tf2.12.0-slim
EXPOSE 80
ENV MODEL_PATH=/model.h5
ENV REFERENCE_PATH=/reference.csv.gz

COPY --from=build /insurance_prediction/dist/insurance_prediction_app-*.whl /
COPY --from=build /insurance_prediction/requirements.txt /

COPY --from=training /model.h5 /
COPY ./datasets/insurance_prediction/reference.csv.gz /

# Until https://github.com/python-poetry/poetry/issues/2778 is resolved:
RUN pip install -r requirements.txt
RUN pip install insurance_prediction_app-*.whl --no-deps

ENTRYPOINT [ "uvicorn", "insurance_prediction.app.main:app", "--host", "0.0.0.0", "--port", "80"]
