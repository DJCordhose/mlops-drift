import uvicorn

from fastapi import FastAPI
from insurance_prediction.app.application.router import router as prediction_router
from insurance_prediction.monitoring import metrics_app


app = FastAPI(docs_url='/')
app.include_router(prediction_router)
app.mount('/metrics', metrics_app)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
