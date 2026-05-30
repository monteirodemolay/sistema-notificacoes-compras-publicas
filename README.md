# Sistema inteligente de notificações e priorização de entregas em compras públicas

Projeto de apoio à decisão para monitoramento de Ordens de Fornecimento (OFs), previsão de risco de atraso e geração de notificações parametrizadas.

## Estrutura

```text
data/raw/ordens_fornecimento.csv        Base de entrada
src/config.py                           Parâmetros do projeto
src/data_processing.py                  Tratamento dos dados
src/train_model.py                      Treinamento, métricas e salvamento do modelo
src/notification_engine.py              Geração de notificações simuladas
src/run_pipeline.py                     Execução completa do fluxo
dashboard/app.py                        Painel Streamlit
models/                                 Modelos treinados
outputs/                                Métricas, base processada e notificações
```

## Instalação no VS Code

```bash
python -m venv .venv
.venv\Scriptsctivate
pip install -r requirements.txt
```

No Linux/Mac:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Executar o pipeline completo

```bash
python src/run_pipeline.py
```

## Executar somente o treinamento

```bash
python src/train_model.py
```

## Abrir o painel

```bash
streamlit run dashboard/app.py
```

## Observação

O módulo de notificações gera mensagens simuladas em CSV e HTML. O envio real por e-mail deve ser configurado apenas com credenciais institucionais, controle de acesso, registro de consentimento operacional e regras de segurança compatíveis com a LGPD.
