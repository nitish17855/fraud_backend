import argparse
import json
import pickle
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
DEFAULT_MODEL_PATH = ROOT_DIR / "ML" / "xgboost_model.pkl"


def read_payload(raw_input):
    if raw_input:
        possible_path = Path(raw_input)
        if possible_path.exists():
            return json.loads(possible_path.read_text(encoding="utf-8"))
        return json.loads(raw_input)

    stdin_data = sys.stdin.read().strip()
    if not stdin_data:
        raise ValueError("No input data provided. Pass JSON by stdin, argument, or file path.")
    return json.loads(stdin_data)


def normalize_records(payload):
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict):
        records = [payload]
    else:
        raise ValueError("Input must be a JSON object or an array of JSON objects.")

    if not all(isinstance(record, dict) for record in records):
        raise ValueError("Every prediction record must be a JSON object.")

    return records


def load_model(model_path):
    with model_path.open("rb") as model_file:
        return pickle.load(model_file)

# Hard Disk
#       │
#       │ xgboost_model.pkl
#       ▼
# model_path
#       │
#       │ open("rb")
#       ▼
# model_file
#       │
#       │ pickle.load()
#       ▼
# Trained XGBoost model object
#       │
#       ▼
# model.predict(...)

def build_dataframe(records, model):
    try:
        import pandas as pd
    except ImportError as exc:
        raise RuntimeError("pandas is required to prepare model input. Install it with pip.") from exc

    frame = pd.DataFrame(records)
    feature_names = getattr(model, "feature_names_in_", None)

    if feature_names is not None:
        missing = [feature for feature in feature_names
                    if feature not in frame.columns]
        if missing:
            raise ValueError(f"Missing required feature(s): {', '.join(missing)}")
        frame = frame[list(feature_names)]

    return frame

# Node

# ↓

# JSON

# ↓

# json.loads()

# ↓

# Dictionary

# ↓

# normalize_records()

# ↓

# List of Dictionaries

# ↓

# pd.DataFrame()

# ↓

# DataFrame

# ↓

# Reorder Columns

# ↓

# model.predict(DataFrame)


def predict(records, model_path):
    model = load_model(model_path)
    data = build_dataframe(records, model)

    predictions = model.predict(data)
    result = {"predictions": predictions.tolist()}

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(data)
        result["probabilities"] = probabilities.tolist()

    return result


def main():
    parser = argparse.ArgumentParser(description="Run fraud prediction with xgboost_model.pkl.")
    parser.add_argument(
        "input",
        nargs="?",
        help="Transaction JSON, path to a JSON file, or omit to read JSON from stdin.",
    )
    parser.add_argument(
        "--model",
        default=str(DEFAULT_MODEL_PATH),
        help="Path to xgboost_model.pkl.",
    )
    args = parser.parse_args()

    try:
        records = normalize_records(read_payload(args.input))
        model_path = Path(args.model)
        output = predict(records, model_path)
        print(json.dumps(output))
    except Exception as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

# Node
# │
# │ spawn("python", ["predict.py"])
# ▼
# Python starts
# │
# ▼
# if __name__ == "__main__"
# │
# ▼
# main()
# │
# ├── parse command-line arguments
# ├── read JSON from stdin
# ├── normalize records
# ├── build model path
# ├── load model
# ├── build DataFrame
# ├── predict
# ├── convert result to JSON
# ├── print JSON to stdout
# └── exit with code 0

#             │
#             ▼
# Node reads stdout
#             │
#             ▼
# JSON.parse(...)
#             │
#             ▼
# Send response to frontend