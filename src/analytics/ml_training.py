import argparse
import json
import os
import sys
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from analytics.data_utils import clean_interactions, fetch_interactions, prepare_ml_dataset

ARTIFACT_DIR = (
    Path(__file__).resolve().parents[2] / "artifacts"
)  # repo_root/artifacts
MODEL_PATH = ARTIFACT_DIR / "interaction_classifier.pkl"
METRICS_PATH = ARTIFACT_DIR / "ml_metrics.json"


def train_model(test_size: float = 0.2, random_state: int = 42) -> dict:
    """Train a simple classifier to label touch events."""
    raw_df = fetch_interactions(limit=5000)
    clean_df = clean_interactions(raw_df)
    dataset = prepare_ml_dataset(clean_df)

    if dataset.empty or dataset["label"].nunique() < 2:
        raise RuntimeError(
            "Dados de toque insuficientes para treinar. "
            "Execute o simulador por alguns minutos antes de rodar o script."
        )

    X = dataset[["duration", "touch_x", "touch_y"]]
    y = dataset["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=random_state
    )

    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            (
                "clf",
                LogisticRegression(max_iter=500, solver="lbfgs"),
            ),
        ]
    )

    pipeline.fit(X_train, y_train)
    predictions = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions, output_dict=True)

    ARTIFACT_DIR.mkdir(exist_ok=True)
    import joblib  # lazy import to keep dependencies localized

    joblib.dump(pipeline, MODEL_PATH)

    metrics = {
        "accuracy": accuracy,
        "samples": int(len(dataset)),
        "duration_range": {
            "min": float(dataset["duration"].min()),
            "max": float(dataset["duration"].max()),
        },
        "class_distribution": (
            dataset["label"].value_counts(normalize=True).round(3).to_dict()
        ),
        "classification_report": report,
    }

    with open(METRICS_PATH, "w", encoding="utf-8") as fp:
        json.dump(metrics, fp, indent=2, ensure_ascii=False)

    return metrics


def print_summary(metrics: dict):
    """Pretty-print metrics to the console."""
    print("\n=== Resultado do Modelo Supervisionado ===")
    print(f"Amostras utilizadas: {metrics['samples']}")
    print(f"Acurácia: {metrics['accuracy']*100:.2f}%")
    print("Distribuição de classes:", metrics["class_distribution"])
    print("Intervalo de duração:", metrics["duration_range"])
    print("\nRelatório detalhado:")
    print(json.dumps(metrics["classification_report"], indent=2, ensure_ascii=False))
    print(f"\nArtefatos salvos em: {ARTIFACT_DIR}")


def show_saved_metrics():
    if not METRICS_PATH.exists():
        raise FileNotFoundError(
            "Nenhum treinamento encontrado. Rode o script sem argumentos primeiro."
        )
    with open(METRICS_PATH, "r", encoding="utf-8") as fp:
        metrics = json.load(fp)
    print_summary(metrics)


def main():
    parser = argparse.ArgumentParser(
        description="Treina e avalia o modelo supervisionado de interações."
    )
    parser.add_argument(
        "--show-last",
        action="store_true",
        help="Apenas exibe as métricas treinadas anteriormente.",
    )
    args = parser.parse_args()

    if args.show_last:
        show_saved_metrics()
    else:
        metrics = train_model()
        print_summary(metrics)


if __name__ == "__main__":
    main()

