import argparse
from pathlib import Path
import joblib

samples = [
    "Congratulations! You've won a free ticket. Reply WIN to claim.",
    "Can we reschedule our meeting to tomorrow?",
    "URGENT! Your account has been suspended. Click here to verify.",
    "Lunch at 12?",
]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifacts", type=str, default="artifacts", help="Directory with model.joblib and vectorizer.joblib")
    args = parser.parse_args()

    art = Path(args.artifacts)
    clf = joblib.load(art / "model.joblib")
    vec = joblib.load(art / "vectorizer.joblib")

    X = vec.transform(samples)
    preds = clf.predict(X)
    for text, p in zip(samples, preds):
        label = "spam" if p == 1 else "ham"
        print(f"[{label}] {text}")

if __name__ == "__main__":
    main()
