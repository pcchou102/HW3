import argparse
import json
import os
from pathlib import Path
from typing import Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
import matplotlib.pyplot as plt
import seaborn as sns


def ensure_out_dir(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)


def read_dataset(path: Path) -> pd.DataFrame:
    # Try headerless first
    try:
        df = pd.read_csv(path, header=None, names=["label", "text"], encoding="utf-8")
    except Exception:
        # Fallback to autodetect
        df = pd.read_csv(path, encoding="utf-8")
    # Normalize columns
    cols = [c.strip().lower() for c in df.columns]
    df.columns = cols
    if "label" not in df.columns or "text" not in df.columns:
        # Try infer if there are exactly two columns
        if len(df.columns) == 2:
            df.columns = ["label", "text"]
        else:
            raise ValueError(
                f"Expected columns ['label','text'] in {path}, got: {df.columns.tolist()}"
            )
    # Drop NA and empty
    df = df.dropna(subset=["label", "text"]).copy()
    df["text"] = df["text"].astype(str).str.strip()
    df = df[df["text"].str.len() > 0]
    return df


def map_labels(labels: pd.Series) -> Tuple[np.ndarray, dict]:
    # Standard dataset uses 'ham' / 'spam'. Handle common variants.
    label_map = {}
    l = labels.astype(str).str.strip().str.lower()
    unique = sorted(l.unique())
    if set(unique).issubset({"ham", "spam"}):
        label_map = {"ham": 0, "spam": 1}
        y = l.map(label_map).values
    elif set(unique).issubset({"0", "1"}):
        label_map = {"0": 0, "1": 1}
        y = l.map(label_map).values
    else:
        # Fallback: make the most frequent class 0 and the other 1
        counts = l.value_counts()
        classes = list(counts.index[:2])
        label_map = {classes[0]: 0, classes[1]: 1}
        y = l.map(label_map).values
    return y, label_map


def plot_confusion(cm: np.ndarray, out_path: Path, class_names=("ham", "spam")) -> None:
    plt.figure(figsize=(4, 3))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False,
                xticklabels=class_names, yticklabels=class_names)
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description="Train baseline SMS spam classifier (LinearSVC)")
    parser.add_argument("--data", type=str, default="dataset/sms_spam_no_header.csv",
                        help="Path to CSV with columns: label,text")
    parser.add_argument("--out", type=str, default="artifacts", help="Output directory for artifacts")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--test-size", type=float, default=0.2, help="Test split size")
    parser.add_argument("--balanced", action="store_true", help="Use class_weight='balanced' for LinearSVC")

    args = parser.parse_args()

    data_path = Path(args.data)
    out_dir = Path(args.out)
    ensure_out_dir(out_dir)

    print(f"Loading dataset from: {data_path}")
    df = read_dataset(data_path)
    print(f"Dataset rows after cleaning: {len(df)}")

    y, label_map = map_labels(df["label"])
    X_text = df["text"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X_text, y, test_size=args.test_size, random_state=args.seed, stratify=y
    )

    vectorizer = TfidfVectorizer(
        lowercase=True,
        analyzer="word",
        ngram_range=(1, 2),
        max_features=50000,
        min_df=2,
        stop_words="english",
    )

    print("Fitting TF-IDF vectorizer...")
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    print("Training LinearSVC baseline...")
    clf = LinearSVC(class_weight=("balanced" if args.balanced else None), random_state=args.seed)
    clf.fit(X_train_vec, y_train)

    print("Evaluating...")
    y_pred = clf.predict(X_test_vec)
    acc = accuracy_score(y_test, y_pred)
    precision, recall, f1, support = precision_recall_fscore_support(y_test, y_pred, average="weighted", zero_division=0)
    report = classification_report(y_test, y_pred, target_names=["ham", "spam"], output_dict=True, zero_division=0)
    cm = confusion_matrix(y_test, y_pred)

    # Save artifacts
    metrics = {
        "accuracy": acc,
        "precision_weighted": precision,
        "recall_weighted": recall,
        "f1_weighted": f1,
        "classification_report": report,
        "label_map": label_map,
        "seed": args.seed,
        "test_size": args.test_size,
    }
    metrics_path = out_dir / "metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    cm_path = out_dir / "confusion_matrix.png"
    plot_confusion(cm, cm_path)

    model_path = out_dir / "model.joblib"
    vec_path = out_dir / "vectorizer.joblib"
    joblib.dump(clf, model_path)
    joblib.dump(vectorizer, vec_path)

    # Simple console summary
    print("=== Results ===")
    print(f"Accuracy: {acc:.4f}")
    print(f"Weighted Precision: {precision:.4f} | Recall: {recall:.4f} | F1: {f1:.4f}")
    print(f"Artifacts saved to: {out_dir.resolve()}")


if __name__ == "__main__":
    main()
