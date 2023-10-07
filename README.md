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

# Installation

You can choose between two ways of installation. You can either install
* locally: requires Docker and Poetry (or at least pip)
* using the cloud: requires accounts for Google Colab and Gitpod

_Please have the installation ready and checked before the workshop. Should you run into problems, please create an issue in this repository._ 

_Should you really have issues, don't panic: we only need one working installation per team, so you can share and installation and work together with a colleague._

## Instalation in the Cloud

Recommended for most users. 

### Prerequisites
- Recent version of a modern browser (like Chrome)
- Google Account (for Colab)
- Gitpod Account

### Part I: Start monitoring servers using Gitpod

Click the button below to start a new development environment:

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/DJCordhose/mlops-drift)

The standard virtual machine might struggle a bit, but should still be able to run our setup. If you can use the more powerful setup.

You might have to wait for a bit until docker has started all containers. Once ports are displayed in the lower right corner, the application has started. Click on the ports to open the overview view. Opening the application running on port 8080 should show the swagger interface on top of its API.

__Note:__ This _should_ work in Github Codespaces (https://github.com/features/codespaces) just fine, but this has not been tested so far.

### Part II: Run Notebooks using Colab
* Developing drift metrics: https://colab.research.google.com/github/djcordhose/mlops-drift/blob/main/notebooks/drift.ipynb
* Analysis: https://colab.research.google.com/github/djcordhose/mlops-drift/blob/main/notebooks/analysis.ipynb
* Re-Train: https://colab.research.google.com/github/djcordhose/mlops-drift/blob/main/notebooks/train.ipynb


## Local Installation

Only recommended when you have experience with Docker and Python build tools and know what you are doing.

### Prerequisites
- Linux, Mac or Windows installation with WSL2 (important)
- curl
- Working Docker 2 installation 
- recent Python 3 installation

### Part I: Start monitoring servers using docker

```
docker compose up
```

Check the following services:
* ML Service should be reachable 
  * Swagger API: http://localhost:8080
  * Metrics: http://localhost:8080/metrics/
* Prometheus scrape target `insurance_prediction_service` should be in `UP` state: http://localhost:9090/targets
* Grafana Dashboard should show mostly empty, but without warnings: http://localhost:3000/d/U54hsxv7k/evidently-data-drift-dashboard?orgId=1&refresh=5s
  * login: admin/admin, you can skip the dialogue asking you to change the password

### Part II: local notebook installation

1. create an environment for the project using your favorite environment manager
   * using the `venv` it would look like this
     * `python3 -m venv .venv` and 
     * `source .venv/bin/activate`
1. pip install poetry
1. poetry install
1. Start your preferred notebook server
   * you can just as well use what is built into your IDE, VSC works just fine
   * if you do not have one, just do: `jupyter notebook`
1. Run notebooks using your notebook server
   * Developing drift metrics: notebooks/drift.ipynb
   * Analysis: notebooks/analysis.ipynb
   * Re-Train: notebooks/train.ipynb