from __future__ import annotations

import os
from typing import Any

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ds_git_homework.serving.model_loader import (
    get_best_run_id,
    load_model_from_s3,
    resolve_model_ref,
)

# ---------------------------------------------------------------------
# App
# ---------------------------------------------------------------------

app = FastAPI(title="ds_git_homework model serving")

MODEL: Any | None = None
FEATURES = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare"]

# ---------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------


class PredictRequest(BaseModel):
    Pclass: int
    Sex: str  # "male" / "female"
    Age: float
    SibSp: int
    Parch: int
    Fare: float


class PredictResponse(BaseModel):
    prediction: int


class HealthResponse(BaseModel):
    status: str


# ---------------------------------------------------------------------
# Startup
# ---------------------------------------------------------------------


@app.on_event("startup")
def startup_load_model() -> None:
    global MODEL

    experiment_name = os.environ.get("SERVE_EXPERIMENT", "titanic_tree")
    metric_name = os.environ.get("SERVE_METRIC", "accuracy")
    os.environ.get("S3_BUCKET", "datasets")
    os.environ.get("MODEL_S3_PREFIX", "models")

    run_id = os.environ.get("SERVE_RUN_ID")
    if run_id is None:
        run_id = get_best_run_id(experiment_name, metric_name)

    model_ref = resolve_model_ref(
        experiment_name=experiment_name,
        run_id=run_id
    )

    MODEL = load_model_from_s3(model_ref)


# ---------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest) -> PredictResponse:
    if MODEL is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")

    sex_num = 0 if req.Sex.lower() == "male" else 1

    row = {
        "Pclass": req.Pclass,
        "Sex": float(sex_num),
        "Age": req.Age,
        "SibSp": req.SibSp,
        "Parch": req.Parch,
        "Fare": req.Fare,
    }

    X = pd.DataFrame([row], columns=FEATURES)
    pred = int(MODEL.predict(X)[0])

    return PredictResponse(prediction=pred)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok" if MODEL is not None else "model_not_loaded"
    )
