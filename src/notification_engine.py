import pandas as pd
from config import NOTIFICATIONS_CSV, NOTIFICATIONS_HTML, PREDICTIONS_PATH, RISK_THRESHOLD, WARNING_DAYS


def classificar_motivo(row: pd.Series) -> str:
    motivos = []
    if row["risk_score"] >= RISK_THRESHOLD:
        motivos.append("risco preditivo elevado")
    if row["dias_para_vencer"] <= WARNING_DAYS:
        motivos.append("prazo próximo do vencimento")
    if row.get("taxa_atraso_fornecedor", 0) >= 0.5:
        motivos.append("histórico de atraso do fornecedor")
    return "; ".join(motivos) if motivos else "monitoramento preventivo"


def montar_mensagem(row: pd.Series) -> str:
    return (
        f"Prezado fornecedor {row['fornecedor']},\n\n"
        f"A Ordem de Fornecimento {row['OF_id']} apresenta prioridade {row['prioridade']} "
        f"no acompanhamento de entrega. O prazo registrado é {row['prazo_entrega']} "
        f"e o escore de risco calculado é {row['risk_score']:.2f}.\n\n"
        "Solicitamos confirmação do status da entrega e previsão atualizada, quando aplicável.\n\n"
        "Esta mensagem foi gerada pelo protótipo de monitoramento de compras públicas."
    )


def gerar_notificacoes() -> pd.DataFrame:
    df = pd.read_csv(PREDICTIONS_PATH, parse_dates=["prazo_entrega"])

    selecionadas = df[
        (df["risk_score"] >= RISK_THRESHOLD)
        | (df["dias_para_vencer"] <= WARNING_DAYS)
    ].copy()

    if selecionadas.empty:
        selecionadas = df.sort_values("risk_score", ascending=False).head(10).copy()

    selecionadas["motivo_notificacao"] = selecionadas.apply(classificar_motivo, axis=1)
    selecionadas["assunto"] = selecionadas.apply(
        lambda row: f"Acompanhamento da OF {row['OF_id']} - prioridade {row['prioridade']}", axis=1
    )
    selecionadas["mensagem"] = selecionadas.apply(montar_mensagem, axis=1)
    selecionadas["status_envio"] = "simulado"

    colunas = [
        "OF_id",
        "fornecedor",
        "categoria",
        "valor",
        "prazo_entrega",
        "dias_para_vencer",
        "risk_score",
        "prioridade",
        "motivo_notificacao",
        "assunto",
        "mensagem",
        "status_envio",
    ]

    NOTIFICATIONS_CSV.parent.mkdir(parents=True, exist_ok=True)
    selecionadas[colunas].to_csv(NOTIFICATIONS_CSV, index=False)
    selecionadas[colunas].to_html(NOTIFICATIONS_HTML, index=False)

    print(f"Notificações simuladas geradas em: {NOTIFICATIONS_CSV}")
    print(f"Relatório HTML gerado em: {NOTIFICATIONS_HTML}")
    return selecionadas[colunas]


if __name__ == "__main__":
    gerar_notificacoes()
