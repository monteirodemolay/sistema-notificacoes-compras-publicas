# Protótipo de Sistema Inteligente para Monitoramento, Notificação e Priorização de Entregas em Compras Públicas

#### Aluno: Luís Eduardo Monteiro Lima [https://github.com/monteirodemolay/sistema-notificacoes-compras-publicas]
#### Orientadora: Manoela Kohler

---

Trabalho apresentado ao curso BI MASTER - Business Intelligence Master - Sistemas Inteligentes de Apoio à Decisão em Negócios / 2023.2 como pré-requisito para conclusão de curso e obtenção de crédito na disciplina "Projetos de Sistemas Inteligentes de Apoio à Decisão" (https://ica.ele.puc-rio.br/cursos/mba-bi-master/).

---

### Resumo

A gestão de compras públicas enfrenta desafios relacionados ao acompanhamento de Ordens de Fornecimento (OFs), especialmente quanto ao cumprimento de prazos e à comunicação entre órgãos contratantes e fornecedores. Este trabalho apresenta o desenvolvimento de um protótipo de sistema inteligente para monitoramento, notificação e priorização de entregas em compras públicas, utilizando técnicas de Ciência de Dados e Aprendizado de Máquina.

A solução contempla um pipeline de ingestão e tratamento de dados, extração de informações de documentos, cálculo de indicadores operacionais, geração automatizada de notificações e construção de um dashboard gerencial para acompanhamento das entregas. Como diferencial, foi desenvolvido um modelo preditivo capaz de estimar o risco de atraso das Ordens de Fornecimento, permitindo a priorização de ações preventivas pelos gestores públicos.

Os resultados demonstraram a viabilidade da utilização de métodos analíticos para apoiar a tomada de decisão, proporcionando maior controle dos prazos, identificação antecipada de situações de risco e melhoria do acompanhamento contratual.

**Palavras-chave:** Compras Públicas, Ordens de Fornecimento, Monitoramento, Machine Learning, Dashboard, Notificações Automáticas.

### Abstract

Public procurement management faces challenges related to monitoring Purchase Orders, especially regarding delivery deadlines and communication between public agencies and suppliers. This project presents the development of an intelligent prototype system for monitoring, notification and prioritization of deliveries in public procurement using Data Science and Machine Learning techniques.

The proposed solution includes a data ingestion and processing pipeline, document information extraction, operational indicators calculation, automated notifications and a managerial dashboard for monitoring deliveries. A predictive model was developed to estimate delivery delay risk, allowing managers to prioritize preventive actions.

The results demonstrated the feasibility of using analytical methods to support decision-making, providing greater control over deadlines, early identification of risk situations and improved contract monitoring.

**Keywords:** Public Procurement, Purchase Orders, Monitoring, Machine Learning, Dashboard, Automated Notifications.

### 1. Introdução

As compras públicas representam uma atividade essencial para o funcionamento da Administração Pública. Apesar dos avanços trazidos pela Lei nº 14.133/2021, o acompanhamento das Ordens de Fornecimento ainda é frequentemente realizado por processos manuais, dificultando o controle dos prazos de entrega e a identificação antecipada de riscos.

Este projeto propõe uma solução tecnológica baseada em Ciência de Dados para automatizar o monitoramento das entregas, gerar notificações automáticas e apoiar a tomada de decisão por meio de indicadores gerenciais e modelos preditivos.

### 2. Modelagem

O desenvolvimento seguiu os princípios da metodologia CRISP-DM, contemplando:

- Compreensão do problema;
- Entendimento e preparação dos dados;
- Construção do pipeline de ingestão;
- Desenvolvimento do modelo preditivo;
- Implementação do sistema de notificações;
- Construção do dashboard gerencial.

Foi utilizada uma base simulada com 1.000 Ordens de Fornecimento distribuídas ao longo de 24 meses, contendo informações de fornecedores, valores, prazos e entregas.

O modelo preditivo foi desenvolvido utilizando o algoritmo Random Forest para classificação do risco de atraso das entregas.

### 3. Resultados

O sistema desenvolvido foi capaz de:

- Automatizar a ingestão e tratamento de dados;
- Extrair informações de documentos;
- Calcular indicadores operacionais;
- Gerar notificações automáticas;
- Classificar Ordens de Fornecimento por nível de risco;
- Disponibilizar dashboard para acompanhamento gerencial.

O modelo apresentou desempenho satisfatório para a finalidade proposta, alcançando:

- ROC-AUC: 0,87
- Precision: 0,84
- Recall: 0,81

Os resultados demonstraram capacidade de identificar previamente situações com maior probabilidade de atraso, permitindo atuação preventiva por parte dos gestores.

### 4. Conclusões

O trabalho demonstrou a viabilidade da aplicação de técnicas de Ciência de Dados e Aprendizado de Máquina no acompanhamento de compras públicas.

A integração entre modelo preditivo, sistema de notificações e dashboard gerencial possibilitou maior controle operacional, melhor rastreabilidade das informações e apoio à tomada de decisão baseada em evidências.

Como trabalhos futuros, recomenda-se ampliar a base histórica utilizada no treinamento dos modelos, integrar o sistema a plataformas institucionais e incorporar algoritmos mais avançados para aprimoramento das previsões.

---

### Tecnologias Utilizadas

- Python
- Pandas
- Scikit-Learn
- Streamlit
- Plotly
- OCR (Tesseract)
- PyMuPDF
- Machine Learning (Random Forest)

### Estrutura da Solução

- Ingestão de dados (CSV, PDF e OCR)
- Tratamento e validação dos dados
- Cálculo de indicadores
- Modelo preditivo de risco de atraso
- Sistema de notificações automáticas
- Dashboard gerencial

---

Matrícula: 231.101.071

Pontifícia Universidade Católica do Rio de Janeiro

Curso de Pós-Graduação Business Intelligence Master
