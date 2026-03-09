"""
This file is to show how to load a saved model and explanation regarding what to choose when you loading model.
"""

import pickle
from pathlib import Path

import joblib

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR.parent / "models"

# fallback: create if it doesn't exist
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def load_model():
    """
    # -------------------------------------
    # Load the model using different methods
    # -------------------------------------

    - Pickle is Python’s native object serialization.
    - Joblib is more efficient than pickle for saving large objects (Joblib is built specifically for NumPy-heavy objects.)
    """
    # Method 1: Using pickle
    with open(MODEL_DIR / "model.pkl", "rb") as f:
        pkl_model = pickle.load(f)

    # Method 2: Using joblib
    jolib_model = joblib.load(MODEL_DIR / "model.joblib")

    # Method 3: Using joblib with compression
    jolib_compressed_model = joblib.load(MODEL_DIR / "model_compressed.joblib")

    # Make predictions
    print(f"Pickle model predictions: \n{pkl_model.predict([[1], [2], [3], [4], [5]])}")
    print(
        f"Joblib model predictions: \n{jolib_model.predict([[1], [2], [3], [4], [5]])}"
    )
    print(
        f"Joblib compressed model predictions: \n{jolib_compressed_model.predict([[1], [2], [3], [4], [5]])}"
    )


if __name__ == "__main__":
    load_model()
