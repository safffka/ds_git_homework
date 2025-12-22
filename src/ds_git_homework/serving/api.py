from __future__ import annotations
import os
from typing import Any
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from ds_git_homework.serving.model_loader import (
    get_best_run_id,
    load_model_from_s3,
    resolve_model_ref,
)

app = FastAPI(title="ds_git_homework model serving")

MODEL: Any | None = None
FEATURES = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare"]


class PredictRequest(BaseModel):
    Pclass: int
    Sex: str  # "male"/"female"
    Age: float
    SibSp: int
    Parch: int
    Fare: float


class PredictResponse(BaseModel):
    prediction: int


@app.on_event("startup")
def startup_load_model() -> None:
    global MODEL

    experiment_name = os.environ.get("SERVE_EXPERIMENT", "titanic_tree")
    metric_name = os.environ.get("SERVE_METRIC", "accuracy")

    run_id = os.environ.get("SERVE_RUN_ID")
    if not run_id:
        run_id = get_best_run_id(experiment_name, metric_name)

    model_ref = resolve_model_ref(
        experiment_name=experiment_name,
        run_id=run_id,
    )

    MODEL = load_model_from_s3(model_ref)


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest) -> PredictResponse:
    if MODEL is None:
        raise RuntimeError("Model is not loaded")

    sex_num = 0 if req.Sex == "male" else 1
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
