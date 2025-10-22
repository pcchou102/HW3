import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
import matplotlib.pyplot as plt
import seaborn as sns

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
    
    with st.spinner("🚀 First-time setup: Downloading dataset and training model (this may take 1-2 minutes)..."):
        try:
            # Download dataset
            if not DATASET_PATH.exists():
                DATASET_PATH.parent.mkdir(parents=True, exist_ok=True)
                import urllib.request
                url = "https://raw.githubusercontent.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Cybersecurity/master/Chapter03/datasets/sms_spam_no_header.csv"
                urllib.request.urlretrieve(url, str(DATASET_PATH))
                st.success("✅ Dataset downloaded")
            
            # Train inline (avoid subprocess issues)
            ART_DIR.mkdir(parents=True, exist_ok=True)
            
            # Load data
            df = pd.read_csv(DATASET_PATH, header=None, names=["label", "text"], encoding="utf-8")
            df = df.dropna(subset=["label", "text"])
            df["text"] = df["text"].astype(str).str.strip()
            df = df[df["text"].str.len() > 0]
            
            # Map labels
            label_map = {"ham": 0, "spam": 1}
            y = df["label"].str.strip().str.lower().map(label_map).values
            X_text = df["text"].values
            
            # Split
            X_train, X_test, y_train, y_test = train_test_split(
                X_text, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Vectorize
            vectorizer = TfidfVectorizer(
                lowercase=True, analyzer="word", ngram_range=(1, 2),
                max_features=50000, min_df=2, stop_words="english"
            )
            X_train_vec = vectorizer.fit_transform(X_train)
            X_test_vec = vectorizer.transform(X_test)
            
            # Train
            clf = LinearSVC(random_state=42)
            clf.fit(X_train_vec, y_train)
            
            # Evaluate
            y_pred = clf.predict(X_test_vec)
            acc = accuracy_score(y_test, y_pred)
            precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average="weighted", zero_division=0)
            cm = confusion_matrix(y_test, y_pred)
            
            # Save artifacts
            metrics = {
                "accuracy": acc,
                "precision_weighted": precision,
                "recall_weighted": recall,
                "f1_weighted": f1,
                "seed": 42,
                "test_size": 0.2,
            }
            with open(METRICS_PATH, "w", encoding="utf-8") as f:
                json.dump(metrics, f, indent=2)
            
            # Save confusion matrix plot
            fig, ax = plt.subplots(figsize=(4, 3))
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                        xticklabels=["ham", "spam"], yticklabels=["ham", "spam"], ax=ax)
            ax.set_xlabel("Predicted")
            ax.set_ylabel("True")
            plt.tight_layout()
            plt.savefig(CM_IMG_PATH)
            plt.close()
            
            # Save model & vectorizer
            joblib.dump(clf, MODEL_PATH)
            joblib.dump(vectorizer, VEC_PATH)
            
            st.success(f"✅ Training complete! Accuracy: {acc:.4f}")
            st.balloons()
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Training failed: {e}")
            st.stop()

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
