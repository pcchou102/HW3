import json
import os
import subprocess
from pathlib import Path

import joblib
import numpy as np
import streamlit as st

ART_DIR = Path("artifacts")
MODEL_PATH = ART_DIR / "model.joblib"
VEC_PATH = ART_DIR / "vectorizer.joblib"
METRICS_PATH = ART_DIR / "metrics.json"
CM_IMG_PATH = ART_DIR / "confusion_matrix.png"
DATASET_PATH = Path("dataset/sms_spam_no_header.csv")

# Auto-train on Streamlit Cloud if artifacts missing
def ensure_artifacts():
    if MODEL_PATH.exists() and VEC_PATH.exists():
        return
    st.info("Artifacts not found. Downloading dataset and training model (one-time setup)...")
    
    # Download dataset
    if not DATASET_PATH.exists():
        DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
        import urllib.request
        url = "https://raw.githubusercontent.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Cybersecurity/master/Chapter03/datasets/sms_spam_no_header.csv"
        urllib.request.urlretrieve(url, str(DATASET_PATH))
    
    # Train model
    subprocess.run(
        ["python", "train.py", "--data", str(DATASET_PATH), "--out", str(ART_DIR), "--seed", "42"],
        check=True
    )
    st.success("Training complete!")
    st.rerun()

ensure_artifacts()

st.set_page_config(page_title="SMS Spam Classifier", page_icon="📬", layout="wide")
st.title("📬 SMS Spam Classifier (Baseline: LinearSVC + TF‑IDF)")

# Sidebar: metrics overview
with st.sidebar:
    st.header("Run Status & Metrics")
    if METRICS_PATH.exists():
        try:
            metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
            st.metric("Accuracy", f"{metrics.get('accuracy', 0):.4f}")
            st.write("Seed:", metrics.get("seed"))
            st.write("Test size:", metrics.get("test_size"))
        except Exception as e:
            st.warning(f"Failed to read metrics.json: {e}")
    else:
        st.info("metrics.json not found. Run training first.")

    if CM_IMG_PATH.exists():
        st.image(str(CM_IMG_PATH), caption="Confusion Matrix", use_container_width=True)
    else:
        st.info("confusion_matrix.png not found.")

# Load model/vectorizer
@st.cache_resource(show_spinner=False)
def load_artifacts():
    if not MODEL_PATH.exists() or not VEC_PATH.exists():
        return None, None
    try:
        clf = joblib.load(MODEL_PATH)
        vec = joblib.load(VEC_PATH)
        return clf, vec
    except Exception as e:
        st.error(f"Failed to load artifacts: {e}")
        return None, None

clf, vec = load_artifacts()

if clf is None or vec is None:
    st.error("Artifacts not found. Please run training to create 'artifacts/model.joblib' and 'artifacts/vectorizer.joblib'.")
    st.stop()

colL, colR = st.columns([3, 2])

with colL:
    st.subheader("Try it out")
    default_text = "Congratulations! You've won a free ticket. Reply WIN to claim."
    text = st.text_area("Enter an SMS message:", value=default_text, height=120)

    if st.button("Classify"):
        if not text.strip():
            st.warning("Please enter some text.")
        else:
            X = vec.transform([text])
            pred = clf.predict(X)[0]
            # LinearSVC has decision_function but no predict_proba
            margin = None
            try:
                margin = clf.decision_function(X)
                if np.ndim(margin) > 1:
                    # For binary, decision_function returns shape (n_samples,)
                    margin = margin[0]
                else:
                    margin = float(margin)
            except Exception:
                pass

            label = "spam" if int(pred) == 1 else "ham"
            st.success(f"Prediction: {label}")
            if margin is not None:
                st.caption(f"Decision margin: {margin:.3f} (positive ⇒ spam)")

with colR:
    st.subheader("How this works")
    st.markdown(
        """
        - Vectorization: TF‑IDF (unigrams/bigrams)
        - Model: LinearSVC (linear SVM)
        - Trained on: `dataset/sms_spam_no_header.csv`
        - Artifacts saved under: `artifacts/`
        """
    )
    st.markdown(
        """
        Tips:
        - If artifacts are missing, run the training script.
        - This baseline does not output probabilities; we show the SVM decision margin.
        """
    )
