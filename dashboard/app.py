import json
from pathlib import Path
import joblib
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parents[1]
PREDICTIONS_PATH = BASE_DIR / "outputs" / "predicoes_risco.csv"
METRICS_PATH = BASE_DIR / "outputs" / "metricas_modelo.json"
MODEL_PATH = BASE_DIR / "models" / "modelo_atraso.pkl"
DATA_RAW = BASE_DIR / "data" / "raw" / "ordens_fornecimento.csv"

st.set_page_config(page_title="Compras Públicas - Risco de Entrega", layout="wide")
st.title("Sistema inteligente de notificações e priorização de entregas")
st.caption("Protótipo para monitoramento de Ordens de Fornecimento em compras públicas")

if not PREDICTIONS_PATH.exists():
    st.warning("Execute primeiro: python src/run_pipeline.py")
    st.stop()

df = pd.read_csv(PREDICTIONS_PATH, parse_dates=["data_emissao", "prazo_entrega", "data_entrega_real"])

st.sidebar.header("Filtros")
fornecedor = st.sidebar.multiselect("Fornecedor", sorted(df["fornecedor"].unique()))
categoria = st.sidebar.multiselect("Categoria", sorted(df["categoria"].unique()))
prioridade = st.sidebar.multiselect("Prioridade", ["Alta", "Média", "Baixa"], default=["Alta", "Média", "Baixa"])
risco_min = st.sidebar.slider("Risco mínimo", 0.0, 1.0, 0.0, 0.05)

filtered = df.copy()
if fornecedor:
    filtered = filtered[filtered["fornecedor"].isin(fornecedor)]
if categoria:
    filtered = filtered[filtered["categoria"].isin(categoria)]
if prioridade:
    filtered = filtered[filtered["prioridade"].isin(prioridade)]
filtered = filtered[filtered["risk_score"] >= risco_min]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de OFs", len(filtered))
col2.metric("Risco médio", f"{filtered['risk_score'].mean():.2f}" if len(filtered) else "0.00")
col3.metric("OFs de alta prioridade", int((filtered["prioridade"] == "Alta").sum()))
col4.metric("Taxa observada de atraso", f"{filtered['atraso'].mean():.1%}" if len(filtered) else "0.0%")

st.subheader("Ordens priorizadas")
st.dataframe(
    filtered.sort_values("risk_score", ascending=False)[
        [
            "OF_id",
            "fornecedor",
            "categoria",
            "valor",
            "data_emissao",
            "prazo_entrega",
            "data_entrega_real",
            "dias_prazo",
            "risk_score",
            "prioridade",
            "atraso",
        ]
    ],
    use_container_width=True,
)

st.subheader("Risco médio por fornecedor")
risco_fornecedor = (
    filtered.groupby("fornecedor", as_index=False)
    .agg(risco_medio=("risk_score", "mean"), total_of=("OF_id", "count"), taxa_atraso=("atraso", "mean"))
    .sort_values("risco_medio", ascending=False)
)
st.bar_chart(risco_fornecedor.set_index("fornecedor")["risco_medio"])
st.dataframe(risco_fornecedor, use_container_width=True)

st.subheader("Distribuição por prioridade")
st.bar_chart(filtered["prioridade"].value_counts())

st.subheader("Métricas do modelo")
if METRICS_PATH.exists():
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        metrics = json.load(f)
    st.json(metrics)
else:
    st.info("As métricas serão exibidas após o treinamento.")

st.subheader("Simulação de nova Ordem de Fornecimento")
if MODEL_PATH.exists():
    model = joblib.load(MODEL_PATH)
    raw = pd.read_csv(DATA_RAW)
    fornecedor_input = st.selectbox("Fornecedor", sorted(raw["fornecedor"].unique()))
    categoria_input = st.selectbox("Categoria", sorted(raw["categoria"].unique()))
    valor_input = st.number_input("Valor da OF", min_value=0.0, value=10000.0, step=1000.0)
    dias_prazo_input = st.number_input("Prazo em dias", min_value=1, value=15, step=1)

    hist = df.groupby("fornecedor").agg(
        taxa_atraso_fornecedor=("atraso", "mean"),
        total_of_fornecedor=("OF_id", "count"),
        valor_medio_fornecedor=("valor", "mean"),
    )

    h = hist.loc[fornecedor_input] if fornecedor_input in hist.index else hist.mean()
    novo = pd.DataFrame(
        [{
            "valor": valor_input,
            "valor_log": __import__("math").log1p(valor_input),
            "dias_prazo": dias_prazo_input,
            "dias_para_vencer": dias_prazo_input,
            "taxa_atraso_fornecedor": h["taxa_atraso_fornecedor"],
            "total_of_fornecedor": h["total_of_fornecedor"],
            "valor_medio_fornecedor": h["valor_medio_fornecedor"],
            "fornecedor": fornecedor_input,
            "categoria": categoria_input,
        }]
    )
    prob = model.predict_proba(novo)[0, 1]
    st.metric("Risco estimado de atraso", f"{prob:.2%}")
else:
    st.info("Modelo ainda não treinado.")
