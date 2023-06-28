# Prepared scripts and image for showing the data-drift example

The data-drift example can be run manually using `sh curl-drift.sh BASE_URL`. The BASE_URL should not contain a trailing slash!

```sh
# For localhost:
sh curl-drift.sh http://localhost:8000
# To manually run it to the cluster
sh curl-drift.sh http://localhost:30080
```

Additionally we also prepared a docker image. This is needed to run this as a k8s job later. It is prepared to be accessible at `ghcr.io/habecker/insurance-prediction-drift-demo`