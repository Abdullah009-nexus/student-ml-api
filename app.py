from pathlib import Path

from flask import Flask, jsonify, request

app = Flask(__name__)

APPLICATION_NAME = "student-ml-api"
VERSION = Path(__file__).with_name("VERSION").read_text(encoding="utf-8").strip()


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "healthy",
            "application": APPLICATION_NAME,
            "version": VERSION,
        }
    )


@app.post("/predict")
def predict():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict) or "value" not in payload:
        return jsonify({"error": "Missing required field: value"}), 400

    try:
        value = float(payload["value"])
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid value: must be numeric"}), 400

    return jsonify(
        {
            "input": value,
            "prediction": value * 2,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
