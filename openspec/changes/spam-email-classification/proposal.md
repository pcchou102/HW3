# Change Proposal: SMS Spam Email Classification (Baseline)

## Summary
Build a baseline SMS spam classifier. The overall goal is spam email/SMS classification using machine learning (eventual Logistic Regression), but Phase 1 will deliver a simple, reproducible baseline using a Support Vector Machine (SVM) on the public dataset:

- Dataset: https://github.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Cybersecurity/blob/master/Chapter03/datasets/sms_spam_no_header.csv

This change establishes the data pipeline, training/evaluation script, and baseline metrics. Later phases (kept empty for now) will iterate with Logistic Regression and other improvements.

## Motivation
- Create a reliable baseline to prove end‑to‑end flow: load data → preprocess → train → evaluate → persist artifacts.
- Provide a yardstick for future models (e.g., Logistic Regression) and feature engineering.

## Scope (Phase 1 Baseline)
- Language: Python (assumption) with scikit‑learn for classic ML. If we need Node.js, we can adapt later, but Python is chosen for faster iteration and richer ML libs.
- Model: Linear SVM (e.g., LinearSVC) as the initial baseline.
- Input: csv with two columns (commonly label,text). We’ll confirm the columns when downloading.
- Steps: load dataset → clean → split (train/test, fixed seed) → vectorize (e.g., TF‑IDF) → train → evaluate.
- Outputs:
  - Metrics: accuracy, precision, recall, F1 (test set)
  - Confusion matrix
  - Trained model artifact (e.g., model.pkl) and vectorizer if needed
  - Minimal CLI entry (e.g., `python train.py --data path --out outdir`)
- Reproducibility: fixed random seed, requirements.txt, brief README.

## Out of Scope (for this change)
- Production deployment, API, or UI
- Hyperparameter tuning beyond a minimal default
- Dataset labeling changes, augmentation, or deduplication
- Advanced feature engineering

## Data Source & Licensing
- Source: PacktPublishing repo (educational sample). We’ll download raw file content from GitHub and cache under `dataset/` or `data/`.
- If the remote link structure changes, we fallback to a local copy placed under version control (small file) or note manual download instructions.

## Acceptance Criteria (Phase 1)
- `train.py` trains a baseline SVM on the dataset and prints metrics for the test split.
- Outputs include accuracy, precision, recall, F1 and a confusion matrix.
- A serialized model artifact and instructions to reproduce are present.
- Baseline quality target: accuracy ≥ 0.95 on the test split (indicative; adjust if dataset realities differ, but aim for a strong baseline).

## Risks & Considerations
- CSV encoding or column naming mismatch (e.g., headerless CSV). We’ll add robust parsing and a schema check.
- Imbalanced classes: we’ll report class distribution; consider class_weight='balanced' if needed.
- Reproducibility on Windows paths/encodings.

## Phases
### Phase 1 (this change): Baseline SVM
- Deliver full training/eval pipeline and artifacts as above.

### Phase 2+: Logistic Regression & Iterations
- Placeholder for future changes (kept empty now per request).

## Alternatives Considered
- Starting directly with Logistic Regression. We picked SVM first to establish a quick high‑performing baseline; we’ll compare in Phase 2.

## Success Metrics
- Reproducible run finishes within minutes on a typical laptop.
- Metrics reported and archived in `artifacts/` or `outputs/` with a simple README.
