# Credit Card Fraud Detection (ML Integration)

## Overview

This project contains the Machine Learning component of a **Credit Card Fraud Detection System**. The model is trained on a PCA-transformed credit card fraud dataset and is designed to integrate seamlessly with a Node.js backend for real-time fraud prediction.

The repository focuses on **model inference**, allowing a backend service to send transaction data to a Python process and receive fraud predictions in JSON format.

---

## Features

* Trained on a PCA-transformed Credit Card Fraud dataset.
* Loads a pre-trained model (`.pkl`) for inference.
* Accepts transaction data in JSON format.
* Supports single and batch predictions.
* Validates required input features before prediction.
* Returns predictions in JSON format.
* Optionally returns prediction probabilities when supported by the model.
* Designed for seamless integration with a Node.js backend using child processes (`spawn`).

---

## Project Structure

```text
.
├── predict.py          # Prediction entry point
├── model.pkl           # Trained ML model
├── requirements.txt    # Python dependencies
└── README.md
```

---

## Workflow

```text
Backend (Node.js)
        │
        │ JSON Transaction
        ▼
Python (predict.py)
        │
        ├── Read Input
        ├── Validate Features
        ├── Convert to DataFrame
        ├── Load Trained Model
        ├── Generate Prediction
        ▼
JSON Response
```

---

## Input

The prediction script expects transaction data in JSON format with the same feature set used during model training.

Example:

```json
{
  "Time": 100,
  "V1": -1.23,
  "V2": 0.45,
  "...": "...",
  "Amount": 250.75
}
```

---

## Output

Example response:

```json
{
  "predictions": [0],
  "probabilities": [
    [0.998, 0.002]
  ]
}
```

Where:

* `0` → Legitimate Transaction
* `1` → Fraudulent Transaction

---

## Backend Integration

The Python script is designed to be executed from a backend service.

Typical flow:

1. Backend starts the Python process.
2. Transaction data is sent through **stdin**.
3. The model performs inference.
4. Prediction results are written to **stdout** as JSON.
5. Backend parses the response and returns it to the client.

---

## Dataset

The model is trained on a **PCA-transformed Credit Card Fraud Detection dataset**, where sensitive transaction features have been anonymized using Principal Component Analysis (PCA). The dataset contains highly imbalanced classes, making it suitable for real-world fraud detection experiments.

---

## Requirements

* Python 3.10+
* pandas
* numpy
* scikit-learn
* xgboost
* joblib (if applicable)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Purpose

This repository demonstrates the Machine Learning inference layer of a real-time fraud detection pipeline. It is intended to be used alongside a backend application that handles API requests and communicates with the Python prediction service.
