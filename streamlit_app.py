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

# Sidebar: 優化版側邊欄
with st.sidebar:
    st.markdown("### 🎯 About This App")
    st.markdown("""
    This demo uses a **Linear SVM** model trained on 5,574 SMS messages 
    to classify text as **spam** or **ham** (legitimate).
    """)
    
    st.markdown("---")
    
    # Model Performance (可摺疊)
    with st.expander("📊 Model Performance", expanded=False):
        if METRICS_PATH.exists():
            try:
                metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Accuracy", f"{metrics.get('accuracy', 0):.3f}")
                    st.metric("Precision", f"{metrics.get('precision_weighted', 0):.3f}")
                with col2:
                    st.metric("Recall", f"{metrics.get('recall_weighted', 0):.3f}")
                    st.metric("F1 Score", f"{metrics.get('f1_weighted', 0):.3f}")
                
                st.caption(f"🔢 Seed: {metrics.get('seed')} | Test size: {metrics.get('test_size')}")
            except Exception as e:
                st.warning(f"Failed to load metrics: {e}")
        else:
            st.info("Metrics not available. Training in progress...")
    
    # Confusion Matrix (可摺疊)
    with st.expander("🔍 Confusion Matrix", expanded=False):
        if CM_IMG_PATH.exists():
            st.image(str(CM_IMG_PATH), use_container_width=True)
            st.caption("Visual breakdown of model predictions")
        else:
            st.info("Confusion matrix will appear after training.")
    
    # Dataset Info (可摺疊)
    with st.expander("📁 Dataset Info", expanded=False):
        st.markdown("""
        **Source**: [PacktPublishing](https://github.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Cybersecurity)
        
        **Total Messages**: 5,574  
        **Split**: 80% train / 20% test  
        **Classes**: Ham (legitimate) & Spam
        
        The dataset contains real-world SMS messages 
        labeled for spam detection research.
        """)
    
    # Quick Stats (固定顯示)
    st.markdown("---")
    st.markdown("### 📈 Quick Stats")
    stat_col1, stat_col2 = st.columns(2)
    with stat_col1:
        st.metric("Model", "LinearSVC")
        st.metric("Features", "TF-IDF")
    with stat_col2:
        st.metric("Train Time", "~2 min")
        st.metric("Status", "✅ Ready")
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.85em;'>
    Built with Streamlit 🎈<br/>
    <a href='https://github.com/pcchou102/HW3' target='_blank'>View on GitHub</a>
    </div>
    """, unsafe_allow_html=True)

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

# 預設範例
HAM_EXAMPLES = [
    "Can we reschedule our meeting to tomorrow at 3pm?",
    "Lunch at 12? I'm thinking pizza.",
    "Hey! How was your weekend? Let's catch up soon.",
    "Thanks for your help yesterday. Really appreciate it!",
    "Don't forget to bring the documents for tomorrow's presentation.",
    "Are you free for coffee this afternoon?",
]

SPAM_EXAMPLES = [
    "Congratulations! You've won a FREE ticket to Bahamas. Reply WIN to claim now!",
    "URGENT! Your bank account has been suspended. Click here to verify immediately.",
    "You have been selected for a $5000 loan. No credit check required. Call now!",
    "FREE iPhone 15! You are the lucky winner. Click this link to claim your prize.",
    "Your package delivery failed. Pay $2.99 fee to reschedule: http://fake-link.com",
    "WINNER! You won $1,000,000 in our lottery. Send your details to claim.",
]

# Initialize session state
if "input_text" not in st.session_state:
    st.session_state["input_text"] = HAM_EXAMPLES[0]

with colL:
    st.subheader("🔍 Try it out")
    
    # 範例按鈕區 - 改為 3 個大按鈕
    st.markdown("**Quick Examples:**")
    col_ham, col_spam, col_random = st.columns(3)
    
    with col_ham:
        if st.button("✅ Generate HAM", use_container_width=True, type="secondary"):
            import random
            st.session_state["input_text"] = random.choice(HAM_EXAMPLES)
            st.rerun()
    
    with col_spam:
        if st.button("🚫 Generate SPAM", use_container_width=True, type="secondary"):
            import random
            st.session_state["input_text"] = random.choice(SPAM_EXAMPLES)
            st.rerun()
    
    with col_random:
        if st.button("🎲 Random", use_container_width=True, type="secondary"):
            import random
            all_examples = HAM_EXAMPLES + SPAM_EXAMPLES
            st.session_state["input_text"] = random.choice(all_examples)
            st.rerun()
    
    st.markdown("---")
    
    # 文字輸入區 - 直接使用 session_state 作為 value
    text = st.text_area(
        "Enter an SMS message:", 
        value=st.session_state["input_text"], 
        height=120,
        help="Type your own message or use the buttons above to generate examples"
    )
    
    # 當使用者手動編輯時，更新 session_state
    if text != st.session_state["input_text"]:
        st.session_state["input_text"] = text

    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        classify_btn = st.button("🚀 Classify", type="primary", use_container_width=True)
    with col_btn2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state["input_text"] = ""
            st.rerun()

    if classify_btn:
        if not text.strip():
            st.warning("⚠️ Please enter some text.")
        else:
            with st.spinner("Analyzing..."):
                X = vec.transform([text])
                pred = clf.predict(X)[0]
                
                # Get decision margin
                margin = None
                try:
                    margin = clf.decision_function(X)
                    if np.ndim(margin) > 1:
                        margin = margin[0]
                    else:
                        margin = float(margin)
                except Exception:
                    pass

                label = "SPAM" if int(pred) == 1 else "HAM"
                is_spam = (label == "SPAM")
                
                # 美化結果展示
                st.markdown("---")
                st.markdown("### 📊 Classification Result")
                
                # 大標題結果
                result_col1, result_col2 = st.columns([2, 3])
                
                with result_col1:
                    if is_spam:
                        st.error("### 🚫 SPAM")
                        st.markdown("**This message is likely spam.**")
                    else:
                        st.success("### ✅ HAM (Legitimate)")
                        st.markdown("**This message appears to be legitimate.**")
                
                with result_col2:
                    # 信心度指示器
                    if margin is not None:
                        confidence = min(abs(margin) / 2.0, 1.0) * 100  # 簡化的信心度
                        st.metric(
                            label="Confidence",
                            value=f"{confidence:.1f}%",
                            delta=f"Margin: {margin:.3f}"
                        )
                        
                        # 視覺化信心度條
                        if is_spam:
                            color = "#ff4b4b" if confidence > 70 else "#ffa500"
                        else:
                            color = "#00cc00" if confidence > 70 else "#ffa500"
                        
                        st.markdown(
                            f"""
                            <div style="background-color: #f0f2f6; border-radius: 10px; padding: 10px; margin-top: 10px;">
                                <div style="background-color: {color}; width: {confidence}%; height: 20px; border-radius: 5px; transition: width 0.5s;"></div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                
                # 詳細解釋
                with st.expander("ℹ️ How does this work?"):
                    st.markdown(f"""
                    - **Model**: Linear SVM (Support Vector Machine)
                    - **Decision Margin**: `{margin:.4f}` (positive = spam, negative = ham)
                    - **Feature Extraction**: TF-IDF with unigrams + bigrams
                    - **Training Accuracy**: ~98.4% on test set
                    
                    The decision margin represents how far the message is from the decision boundary. 
                    Larger absolute values indicate higher confidence.
                    """)

with colR:
    st.subheader("📖 How this works")
    st.markdown(
        """
        ### Model Architecture
        - **Vectorization**: TF‑IDF (unigrams/bigrams)
        - **Algorithm**: LinearSVC (linear SVM)
        - **Training Data**: 5,574 SMS messages
        - **Accuracy**: ~98.4%
        
        ### Quick Guide
        1. Click a quick example or type your own message
        2. Press **Classify** to analyze
        3. View the prediction with confidence score
        
        ### Tips
        - Spam messages often contain: prizes, urgent actions, suspicious links
        - Ham messages are normal conversations
        - Confidence based on decision boundary distance
        """
    )
