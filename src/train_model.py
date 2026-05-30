import json
import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from config import DATA_RAW, DATA_PROCESSED, METRICS_PATH, MODEL_PATH, PREDICTIONS_PATH, RANDOM_STATE, TEST_SIZE
from data_processing import prepare_dataset

NUMERIC_FEATURES = [
    "valor",
    "valor_log",
    "dias_prazo",
    "dias_para_vencer",
    "taxa_atraso_fornecedor",
    "total_of_fornecedor",
    "valor_medio_fornecedor",
]

CATEGORICAL_FEATURES = ["fornecedor", "categoria"]
TARGET = "atraso"


def build_model() -> Pipeline:
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, NUMERIC_FEATURES),
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
        ]
    )

    classifier = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_leaf=2,
        class_weight="balanced",
        random_state=RANDOM_STATE,
    )

    return Pipeline(steps=[("preprocessor", preprocessor), ("model", classifier)])


def baseline_score(df: pd.DataFrame) -> pd.Series:
    """Baseline heurístico: maior risco quando o fornecedor tem histórico de atraso e o prazo é curto."""
    prazo_curto = (df["dias_prazo"] <= df["dias_prazo"].median()).astype(float)
    risco = 0.7 * df["taxa_atraso_fornecedor"] + 0.3 * prazo_curto
    return risco.clip(0, 1)


def train() -> None:
    df = prepare_dataset(DATA_RAW)
    DATA_PROCESSED.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PROCESSED, index=False)

    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    model = build_model()
    model.fit(X_train, y_train)

    y_prob = model.predict_proba(X_test)[:, 1]
    y_pred = (y_prob >= 0.5).astype(int)

    baseline_prob = baseline_score(df.loc[X_test.index])
    baseline_pred = (baseline_prob >= 0.5).astype(int)

    metrics = {
        "modelo_random_forest": {
            "roc_auc": float(roc_auc_score(y_test, y_prob)),
            "pr_auc": float(average_precision_score(y_test, y_prob)),
            "accuracy": float(accuracy_score(y_test, y_pred)),
            "precision": float(precision_score(y_test, y_pred, zero_division=0)),
            "recall": float(recall_score(y_test, y_pred, zero_division=0)),
            "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
            "classification_report": classification_report(y_test, y_pred, zero_division=0),
        },
        "baseline_heuristico": {
            "roc_auc": float(roc_auc_score(y_test, baseline_prob)),
            "pr_auc": float(average_precision_score(y_test, baseline_prob)),
            "accuracy": float(accuracy_score(y_test, baseline_pred)),
            "precision": float(precision_score(y_test, baseline_pred, zero_division=0)),
            "recall": float(recall_score(y_test, baseline_pred, zero_division=0)),
            "confusion_matrix": confusion_matrix(y_test, baseline_pred).tolist(),
        },
        "features_numericas": NUMERIC_FEATURES,
        "features_categoricas": CATEGORICAL_FEATURES,
    }

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=4)

    df["risk_score"] = model.predict_proba(df[NUMERIC_FEATURES + CATEGORICAL_FEATURES])[:, 1]
    df["prioridade"] = pd.cut(
        df["risk_score"],
        bins=[-0.01, 0.39, 0.69, 1.0],
        labels=["Baixa", "Média", "Alta"],
    )
    df.to_csv(PREDICTIONS_PATH, index=False)

    print("Modelo treinado com sucesso.")
    print(f"Modelo salvo em: {MODEL_PATH}")
    print(f"Métricas salvas em: {METRICS_PATH}")
    print(f"Predições salvas em: {PREDICTIONS_PATH}")
    print(json.dumps(metrics["modelo_random_forest"], ensure_ascii=False, indent=4))


if __name__ == "__main__":
    train()
