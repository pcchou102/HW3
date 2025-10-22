# SMS Spam Classification (Baseline)

This project provides a reproducible baseline for SMS spam classification using a linear SVM with TF‑IDF features. It is meant to establish an end‑to‑end pipeline for future iterations (e.g., Logistic Regression in Phase 2).

## Dataset
- Source: PacktPublishing — sms_spam_no_header.csv
- Raw URL:
  https://raw.githubusercontent.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Cybersecurity/master/Chapter03/datasets/sms_spam_no_header.csv
- Expected local path: `dataset/sms_spam_no_header.csv`

## Quickstart (Windows PowerShell)

```powershell
# 1) Create and activate a virtual environment
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 3) Download dataset (or place it under dataset/)
New-Item -ItemType Directory -Path dataset -Force | Out-Null
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Cybersecurity/master/Chapter03/datasets/sms_spam_no_header.csv" -OutFile "dataset/sms_spam_no_header.csv"

# 4) Train baseline model
python train.py --data dataset/sms_spam_no_header.csv --out artifacts --seed 42

# 5) (Optional) Run smoke test
python test_smoke.py --artifacts artifacts
```

Artifacts include:
- `artifacts/model.joblib` — trained LinearSVC
- `artifacts/vectorizer.joblib` — fitted TF‑IDF vectorizer
- `artifacts/metrics.json` — accuracy/precision/recall/F1 and report
- `artifacts/confusion_matrix.png` — confusion matrix visualization

## Launch the Streamlit App

```powershell
# Ensure dependencies are installed and artifacts exist
pip install -r requirements.txt

# Run the Streamlit UI (opens a local web app)
streamlit run streamlit_app.py
```

You can input an SMS message and see the predicted label (ham/spam). The sidebar shows accuracy and the confusion matrix from your last training run.

## Notes
- If the dataset schema changes, update the loader in `train.py` accordingly.
- You can enable class balancing with `--balanced`.
- For reproducibility, keep the random seed and dependency versions stable.
