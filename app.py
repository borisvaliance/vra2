import os
import math
import random
from typing import Dict, Any

# --- UI ---
import streamlit as st

# --- Optional backend ---
from flask import Flask, jsonify, request

# =========================================
# CONFIG
# =========================================
RUN_MODE = os.getenv("RUN_MODE", "streamlit")   # "streamlit" (default) or "flask"
PORT = int(os.getenv("PORT", "5000"))           # Flask port (local only)
API_BASE_URL = os.getenv("API_BASE_URL")        # e.g., "https://your-api.example.com"
TIMEOUT_SECS = 30

# =========================================
# SIMPLE PREDICTORS (placeholder logic)
# Replace with real model loads and inference
# =========================================
def _sigmoid(x: float) -> float:
    return 1 / (1 + math.exp(-x))

def predict_cause(features: Dict[str, Any]) -> Dict[str, Any]:
    # Dummy scoring: deterministic-ish using simple hashing
    score = (hash(str(features)) % 100) / 100
    classes = ["Electrical", "Cooking", "Arson", "Wildfire", "Unknown"]
    pred = classes[int(score * len(classes)) % len(classes)]
    conf = 0.6 + 0.4 * _sigmoid(score * 3 - 1.5)
    return {"prediction": pred, "confidence": round(conf, 3)}

def predict_loss_severity(features: Dict[str, Any]) -> Dict[str, Any]:
    base = (hash("loss"+str(features)) % 100) / 100
    buckets = ["Low", "Moderate", "High", "Severe", "Catastrophic"]
    pred = buckets[int(base * len(buckets)) % len(buckets)]
    conf = 0.55 + 0.45 * _sigmoid(base * 4 - 2)
    return {"prediction": pred, "confidence": round(conf, 3)}

def predict_response_risk(features: Dict[str, Any]) -> Dict[str, Any]:
    base = (hash("resp"+str(features)) % 100) / 100
    pred = "Elevated" if base > 0.5 else "Normal"
    conf = 0.5 + 0.5 * _sigmoid((base - 0.5) * 6)
    return {"prediction": pred, "confidence": round(conf, 3)}

# =========================================
# FLASK BACKEND (runs only when RUN_MODE=flask)
# =========================================
flask_app = Flask(__name__)

@flask_app.route("/predict/cause", methods=["POST"])
def route_cause():
    data = request.get_json(force=True) or {}
    return jsonify(predict_cause(data))

@flask_app.route("/predict/loss_severity", methods=["POST"])
def route_loss():
    data = request.get_json(force=True) or {}
    return jsonify(predict_loss_severity(data))

@flask_app.route("/predict/response_risk", methods=["POST"])
def route_resp():
    data = request.get_json(force=True) or {}
    return jsonify(predict_response_risk(data))

# =========================================
# STREAMLIT FRONTEND (default)
# =========================================
def run_streamlit():
    import requests

    st.set_page_config(page_title="NFIRS AI Analytics", layout="wide")
    st.title("🔥 NFIRS AI Analytics")

    with st.sidebar:
        st.header("Inputs")
        incident_type = st.selectbox("Incident Type", ["Fire", "Rescue", "Hazmat", "Medical"])
        structure_type = st.selectbox("Structure Type", ["Residential", "Commercial", "Industrial", "Wildland"])
        occupancy = st.selectbox("Occupancy", ["Single-family", "Multi-family", "Warehouse", "Office", "Open space"])
        weather_severity = st.slider("Weather Severity (0–10)", 0, 10, 4)
        alarm_hour = st.slider("Alarm Hour (0–23)", 0, 23, 15)
        units_responding = st.number_input("Units Responding", min_value=1, max_value=50, value=3, step=1)
        sqft = st.number_input("Structure Sq Ft", min_value=0, max_value=100000, value=1800, step=100)
        st.divider()
        st.caption("Tip: set API_BASE_URL in Secrets to call your deployed API.")

    features = {
        "incident_type": incident_type,
        "structure_type": structure_type,
        "occupancy": occupancy,
        "weather_severity": int(weather_severity),
        "alarm_hour": int(alarm_hour),
        "units_responding": int(units_responding),
        "structure_sqft": int(sqft),
    }

    tabs = st.tabs(["Cause", "Loss Severity", "Response Risk"])

    def call_or_local(endpoint: str, payload: dict, fallback_fn):
        """If API_BASE_URL is set, call it; else run local function."""
        if API_BASE_URL:
            try:
                url = f"{API_BASE_URL.rstrip('/')}{endpoint}"
                r = requests.post
