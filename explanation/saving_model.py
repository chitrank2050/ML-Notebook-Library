"""
This file is to show how to save a model and explanation regarding what to choose when you saving model.
I am just going to build a simple linear regression model and save it using different methods.

# -------------------------------------
# What production systems actually use?
# -------------------------------------

->>> Winner for traditional ML → Joblib

- Traditional ML models: joblib (because these models contain large NumPy arrays.)
  Example:
  •	linear regression
  •	random forest
  •	gradient boosting
- Deep learning / LLM models: pytorch, tensorflow, huggingface (Use framework formats instead)
  Why?
  •	hardware optimized
  •	GPU compatible
  •	safer
  •	framework supported

# -------------------------------------
# What LLM infrastructure uses?
# -------------------------------------

Modern LLM stacks use formats like:
- Safetensors
- GGUF
- ONNX
- TensorRT

|-------------------|---------------------------------|
| Format            | Why                             |
|-------------------|---------------------------------|
| safetensors       | secure, fast loading            |
| ONNX              | cross-platform inference        |
| GGUF              | optimized for local inference   |
| TensorRT          | optimized for NVIDIA GPUs       |
|-------------------|---------------------------------|

Serious ML infrastructure prefers:
- ONNX
- TorchScript
- SavedModel
- safetensors

Because they support:
- GPU
- distributed inference
- language-independent serving

|----------------------|----------------------|
| Model Type.          | Format               |
|----------------------|----------------------|
| scikit-learn         | joblib               |
| PyTorch              | .pth                 |
| TensorFlow           | SavedModel           |
| LLM                  | safetensors / gguf   |
| cross-platform       | onnx                 |
|----------------------|----------------------|

"""

import pickle
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR.parent / "models"

# fallback: create if it doesn't exist
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def train_model():
    """
    Train a simple linear regression model
    - Generate some sample data
    - Split the data into training and testing sets
    - Train a simple linear regression model
    - Make predictions on the test set
    - Evaluate the model
    - Plot the results
    - Save the model

    We need to train model on training data and evaluate it on test data.
    """
    # Generate some sample data
    np.random.seed(42)
    X = 2 * np.random.rand(100, 1)
    y = 4 + 3 * X + np.random.randn(100, 1)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train a simple linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = model.predict(X_test)

    # Evaluate the model
    print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
    print("R2 Score:", r2_score(y_test, y_pred))

    # Plot the results
    plt.scatter(X_test, y_test, color="black")
    plt.plot(X_test, y_pred, color="blue", linewidth=3)
    plt.xlabel("X")
    plt.ylabel("y")
    plt.title("Linear Regression")
    plt.show()

    # Save the model
    save_model(model)


def save_model(model: LinearRegression):
    """
    # -------------------------------------
    # Save the model using different methods
    # -------------------------------------

    We have pickle and joblib as popular options to save models
    - Pickle is Python’s native object serialization.
    - Joblib is more efficient than pickle for saving large objects (Joblib is built specifically for NumPy-heavy objects.)
    """

    # Method 1: Using pickle
    with open(MODEL_DIR / "model.pkl", "wb") as f:
        pickle.dump(model, f)

    # Method 2: Using joblib
    joblib.dump(model, MODEL_DIR / "model.joblib")

    # Method 3: Using joblib with compression
    joblib.dump(model, MODEL_DIR / "model_compressed.joblib", compress=3)

    # Method 4: Using joblib with different compression levels
    joblib.dump(model, MODEL_DIR / "model_compressed_0.joblib", compress=0)
    joblib.dump(model, MODEL_DIR / "model_compressed_1.joblib", compress=1)
    joblib.dump(model, MODEL_DIR / "model_compressed_2.joblib", compress=2)
    joblib.dump(model, MODEL_DIR / "model_compressed_3.joblib", compress=3)
    joblib.dump(model, MODEL_DIR / "model_compressed_4.joblib", compress=4)
    joblib.dump(model, MODEL_DIR / "model_compressed_5.joblib", compress=5)
    joblib.dump(model, MODEL_DIR / "model_compressed_6.joblib", compress=6)
    joblib.dump(model, MODEL_DIR / "model_compressed_7.joblib", compress=7)
    joblib.dump(model, MODEL_DIR / "model_compressed_8.joblib", compress=8)
    joblib.dump(model, MODEL_DIR / "model_compressed_9.joblib", compress=9)


if __name__ == "__main__":
    train_model()
