# Previsão de Default para a X-Health

Este repositório contém o projeto desenvolvido para a previsão de default (não-pagamento) de clientes de uma empresa fictícia (a X-Health), que atua no comércio de dispositivos eletrônicos voltados para a saúde. O objetivo é minimizar o número de defaults por meio de um modelo de machine learning capaz de identificar previamente as transações com maior risco de default.

Para mais informações, consulte a [apresentação de slides](./docs/slides.pdf) que detalha o contexto, a abordagem adotada, os resultados obtidos e as considerações sobre o impacto e limitações do modelo.

## Estrutura do Repositório

- [notebooks](./notebooks): Contém os Jupyter Notebooks usados durante o desenvolvimento do projeto
  - [1_analise_de_dados.ipynb](./notebooks/1_analise_de_dados.ipynb): análise exploratória de dados
  - [2_treinamento.ipynb](./notebooks/2_treinamento.ipynb): pipeline de treinamento do modelo
  - [3_predicao.ipynb](./notebooks/3_predicao.ipynb): função de predição
- [src/processing.py](./src/processing.py): contém funções auxiliares, descritas no notebook de treinamento
- [docs/slides.pdf](./docs/slides.pdf): apresentação de slides sobre o projeto
- [model.pickle](./model.pickle): modelo treinado
- [requirements.txt](./requirements.txt): lista de dependências necessárias para rodar o projeto
- [_data/dataset_2021-5-26-10-14.csv](./dataset_2021-5-26-10-14.csv): contém os dados utilizados no projeto

## Dependências

O projeto foi desenvolvido usando Python 3.10 e depende de diversas bibliotecas de análise de dados e machine learning, dentre as quais:

- numpy
- pandas
- matplotlib
- seaborn
- scikit-learn
- scipy
- lightgbm
- optuna

Para instalar as dependências, execute:

```bash
pip install -r requirements.txt
```

Essas dependências são suficientes para executar os notebooks no VS Code. Para utilizar outro ambiente de execução, será necessário instalá-lo. Por exemplo:

```bash
pip install notebook  # interface clássica
pip install jupyterlab # JupyterLab
```

## Dados

Os dados utilizados neste projeto estão localizados em [_data/dataset_2021-5-26-10-14.csv](./_data/dataset_2021-5-26-10-14.csv) e incluem variáveis internas e externas, como detalhado na apresentação.

## Como Usar

1. Clone o repositório para o seu ambiente local.
2. Instale as dependências necessárias.
3. Explore os notebooks na pasta [notebooks/](./notebooks/) para entender a análise de dados, o processo de treinamento e a função de predição.
4. Para previsões, use o notebook [3_predicao.ipynb](./notebooks/3_predicao.ipynb), alimentando-o com novos dados em forma de dicionário, conforme os exemplos fornecidos.
