# Fraud Backend Prediction

This project can run fraud predictions with `predict.py` using the saved XGBoost model at:

```text
ML/xgboost_model.pkl
```

## Python dependencies

Install the Python packages needed by the model before running predictions:

```bash
pip install xgboost pandas scikit-learn
```

If the model was trained with a specific Python or XGBoost version, use that same version to avoid pickle compatibility issues.

## Running `predict.py`

`predict.py` accepts transaction data as JSON from stdin, a JSON string argument, or a JSON file path.

### From stdin

```bash
echo "{\"amount\": 100, \"merchant\": 42}" | python predict.py
```

### From a JSON argument

```bash
python predict.py "{\"amount\": 100, \"merchant\": 42}"
```

### From a JSON file

```bash
python predict.py transaction.json
```

For multiple transactions, pass an array of objects:

```json
[
  { "amount": 100, "merchant": 42 },
  { "amount": 250, "merchant": 12 }
]
```

The script prints JSON like:

```json
{
  "predictions": [0],
  "probabilities": [[0.91, 0.09]]
}
```

## Using it from `GET_DATA.js`

`Backend/src/GET_DATA.js` currently receives `req.body`. Send that object to `predict.py` through stdin from Node:

```js
import { spawn } from "node:child_process";

const python = spawn("python", ["../predict.py"]);
python.stdin.write(JSON.stringify(req.body));
python.stdin.end();
```

Collect stdout from the Python process and return it as the API response. Make sure Express has JSON parsing enabled with `app.use(express.json())`.

## Input fields

The JSON keys must match the feature names used when `xgboost_model.pkl` was trained. If the model stores feature names, `predict.py` will validate missing fields and order the data correctly. If it does not, the input JSON key order must match the training feature order.
