# MLOps: Monitoring and Managing Drift

As soon as your machine learning model goes into production everything changes. 
You now will need to constantly monitor the performance of your model, evaluate whether it is still sufficient and react accordingly.
This, however, can be a challenge when you have no reliable ground truth to recalibrate its performance. 
Typically, you will need to fall back to a surrogate metric that you can measure and that is correlated with the performance of your model.
What those metrics can be and how you track and monitor them is the topic of this workshop.

This workshop consists of two parts:
- Part I: Simulate production on an existing machine learning model and detecting drift
  - an OpenAPI machine learning service will be provided
  - we will use Evidently, Prometheus and Grafana to monitor and detect the drift
- Part II: Interpreting and Analyzing Drift and what to do about it
  - when you have detected drift, you will need to interpret what happened and decide what to do about it
  - among the steps you can take is to retrain your model with new data
  - we might also have to consider to rethink the model architecture or the data we are using

Our objective is to ensure that you are equipped with the essential knowledge and practical tools to proficiently manage
your machine learning models in a real-world production environment.

## Start using Gitpod

Click the button below to start a new development environment:

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/DJCordhose/mlops-drift)

## Local Installation

Please have the installation ready and checked before the workshop. Should you run into problems, 
please create an issue in this repository.

### Prerequisites
- Linux, Mac oder Windows installation with WSL2 (important)
- curl
- Working Docker installation 
- Recent version of a modern browser (like Chrome)
- Google Account (for Colab)

### Part I: local installation using docker

_we only need one working installation per team, so if it really does not work on your machine, you can share with a colleague_

```
docker compose up
```

Check the following services:
* ML Service should be reachable 
  * Swagger API: http://localhost:8080
  * Metrics: http://localhost:8080/metrics/
* Prometheus scrape target `insurance_prediction_service` should be in `UP` state: http://localhost:9090/targets
* Grafana Dashboard should show mostly empty, but without warnings: http://localhost:3000/d/U54hsxv7k/evidently-data-drift-dashboard?orgId=1&refresh=5s

### Part II: cloud installation using Colab or local installation, both work fine

_this should work for every participant_

## Credits

This repository is based on https://github.com/openknowledge/mlops-m3/tree/main/insurance-prediction

