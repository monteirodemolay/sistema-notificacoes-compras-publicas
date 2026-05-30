from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_RAW = BASE_DIR / "data" / "raw" / "ordens_fornecimento.csv"
DATA_PROCESSED = BASE_DIR / "data" / "processed" / "ordens_processadas.csv"
MODEL_PATH = BASE_DIR / "models" / "modelo_atraso.pkl"
METRICS_PATH = BASE_DIR / "outputs" / "metricas_modelo.json"
PREDICTIONS_PATH = BASE_DIR / "outputs" / "predicoes_risco.csv"
NOTIFICATIONS_CSV = BASE_DIR / "outputs" / "notificacoes" / "notificacoes_geradas.csv"
NOTIFICATIONS_HTML = BASE_DIR / "outputs" / "notificacoes" / "notificacoes_geradas.html"

RANDOM_STATE = 42
TEST_SIZE = 0.25
RISK_THRESHOLD = 0.70
WARNING_DAYS = 5
