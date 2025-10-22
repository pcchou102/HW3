## 1. Environment Setup
- [x] 1.1 Create a Python 3.10+ virtual environment (e.g., venv)
- [x] 1.2 Add `requirements.txt` with: scikit-learn, pandas, numpy, scipy, scikit-learn-intelex (optional), matplotlib, seaborn (optional), joblib
- [x] 1.3 Verify installation on Windows PowerShell and document steps in a mini README (see `README.md`)

## 2. Data Acquisition & Preparation
- [x] 2.1 Download the dataset to `dataset/sms_spam_no_header.csv` (raw file from GitHub)
- [x] 2.2 Validate schema (label,text) and handle headerless format
- [x] 2.3 Basic cleaning: trim whitespace, drop empty text rows, normalize newlines
- [x] 2.4 Train/test split (e.g., 80/20) with fixed random seed and stratification

## 3. Feature Engineering
- [x] 3.1 Text vectorization with TF‑IDF (unigrams/bigrams baseline)
- [x] 3.2 Persist the fitted vectorizer (e.g., joblib dump)

## 4. Modeling (Baseline)
- [x] 4.1 Train a Linear SVM (e.g., `LinearSVC`) on the training set
- [x] 4.2 Evaluate on test set: accuracy, precision, recall, F1 (macro/weighted)
- [x] 4.3 Generate and save confusion matrix plot to `artifacts/`
- [x] 4.4 Serialize the model (e.g., `artifacts/model.joblib`) and vectorizer (`artifacts/vectorizer.joblib`)

## 5. CLI & Reproducibility
- [x] 5.1 Provide `train.py` with arguments: `--data`, `--out`, `--seed`
- [x] 5.2 Print metrics to console and save JSON report to `artifacts/metrics.json`
- [x] 5.3 Add a minimal `README.md` under project root describing how to run

## 6. Quality Gates
- [x] 6.1 Target: Accuracy ≥ 0.95 on test split; document actual results (achieved: Accuracy ≈ 0.984; see `artifacts/metrics.json`)
- [x] 6.2 Add a tiny smoke test script that loads the saved model and predicts on 3–5 sample texts (`test_smoke.py`)

## 7. Phase 2+ Placeholders (keep empty for now)
- [ ] 7.1 Logistic Regression implementation and comparison (TBD)
- [ ] 7.2 Hyperparameter tuning and/or feature improvements (TBD)
- [ ] 7.3 Packaging or service interface (TBD)
