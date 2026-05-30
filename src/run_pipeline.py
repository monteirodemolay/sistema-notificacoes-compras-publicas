from train_model import train
from notification_engine import gerar_notificacoes


def main() -> None:
    train()
    gerar_notificacoes()
    print("Pipeline concluído.")


if __name__ == "__main__":
    main()
