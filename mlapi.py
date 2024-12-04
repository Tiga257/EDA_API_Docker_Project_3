"""
Sepsis Prediction API

This API provides a simple interface for predicting sepsis using various machine learning models.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
import numpy as np
import pandas as pd
from typing import Dict
import joblib
import uvicorn



app = FastAPI(
    title = "SEPSIS PREDICTION API",
    description= "Predict sepsis using various machine learning models"
)

MODEL_PATHS = {"Logistic_Regression": "models/logistic_regression_model.pkl", 
              "Random_Forest": "models/random_forest_model.pkl", "KNN": 
              "models/k-nearest_neighbors_model.pkl"
}

# load the models

models = {}
for model, path in MODEL_PATHS.items():
    try:
        models [model] = joblib.load(path)
    except Exception as e: 
        raise RuntimeError(f"Failed to load model '{models}' from '{path}'. Error: {e}")
    
@app.get("/")
async def st_endpoint():
    return{"message": "Welcome to Sepsis Prediction App"}


@app.post("/predict")
async def predictor(model: str, file:UploadFile = File(...)):
    """
    This accepts a model
    
    Successfully loads a file

    Eventually returns a json with prediction for each row

    """
# load the csv file
    try: 
        df = pd.read_csv(file.file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading the file:{e}")   

# verify required features
    required_features = models[model].n_features_in_
    if len(df.columns) != required_features:
        raise HTTPException(ststus_code=400, detail=f"the model expect{required_features} but file has {len(df.columns).columns}")
    
# convert to array   
    features = df.values

# select the model  
    selected_model = models[model]
# make predictions
    predictions = selected_model.predict(df)

# show response
    results = {
        "model_used": model,
        "predictions": predictions.tolist() 
    }

    return results