# Delta for ML Spam Classifier

## ADDED Requirements

### Requirement: SMS Spam Classification Baseline
The system SHALL provide a reproducible baseline model for SMS spam classification using a linear SVM.

#### Scenario: Baseline training and evaluation
- GIVEN the dataset is available at `dataset/sms_spam_no_header.csv` (downloaded from the referenced GitHub URL)
- AND a fixed random seed is used with a stratified train/test split
- AND text is vectorized using TF‑IDF
- WHEN the training script is executed
- THEN the system SHALL train a baseline linear SVM model
- AND output accuracy, precision, recall, and F1 score on the test set
- AND save a confusion matrix image to `artifacts/`
- AND persist the trained model and vectorizer as files in `artifacts/`

#### Scenario: Baseline quality threshold
- WHEN evaluating on the held‑out test set
- THEN accuracy SHOULD be at least 0.95 (target)
- AND actual results SHALL be documented in a metrics JSON file

### Requirement: Reproducibility
The training MUST be reproducible across runs on the same machine.

#### Scenario: Deterministic seed and versions
- GIVEN a fixed random seed and pinned library versions in `requirements.txt`
- WHEN re‑running the training
- THEN results SHOULD be within negligible variance of prior runs
- AND environment setup steps SHALL be documented for Windows PowerShell

## MODIFIED Requirements
- None

## REMOVED Requirements
- None
