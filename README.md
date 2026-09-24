# Projeto Integrador 4 - Detecção de Fraude em Cartão de Crédito

Comparação de três classificadores para detectar transações fraudulentas:
**SGDClassifier** (modelo linear), **LightGBM** (boosting de árvores) e uma **rede neural**.

## Dados

[Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud) (Machine Learning Group da
ULB, via Kaggle): 284.807 transações de dois dias, com 492 fraudes (0,17%). As colunas `V1` a `V28` são componentes
PCA anonimizadas; `Time` são os segundos desde a primeira transação, `Amount` é o valor e `Class` é o alvo (1 = fraude).

A base já vem no repositório, comprimida em **`dados/creditcard.csv.xz`** (60 MB; o CSV original tem 150 MB e passa
do limite de 100 MB por arquivo do GitHub). Não é preciso baixar nada: o `pandas` lê o arquivo comprimido
diretamente, e `src/preparo.py` já aponta para ele. O conteúdo é idêntico ao CSV do Kaggle (SHA-256 do CSV
descomprimido: `76274b691b16a6c49d3f159c883398e03ccd6d1ee12d9d8ee38f4b4b98551a89`). Para ter o CSV puro:
`xz -dk dados/creditcard.csv.xz`.

Licença: [Database Contents License (DbCL) v1.0](https://opendatacommons.org/licenses/dbcl/1-0/). Entre os trabalhos
que os autores pedem para citar está: Andrea Dal Pozzolo, Olivier Caelen, Reid A. Johnson e Gianluca Bontempi, *Calibrating
Probability with Undersampling for Unbalanced Classification*, IEEE Symposium on Computational Intelligence and
Data Mining (CIDM), 2015.

## Estrutura

| Caminho | Conteúdo |
|---|---|
| `analise_exploratoria.ipynb` | Etapa 1: análise exploratória e preparo dos dados (remoção de duplicatas e partição treino/teste) |
| `light_gbm.ipynb`, `rede_neural.ipynb`, `sgdRegressor.ipynb` | Notebooks de modelagem do grupo (em desenvolvimento) |
| `src/preparo.py` | Carregamento, remoção de duplicatas, atributos, partição treino/teste salva, partição temporal e folds |
| `dados/creditcard.csv.xz` | Base de dados comprimida (ver acima) |
| `resultados/split_indices.npz` | Índices de treino e teste gravados pela análise exploratória |
| `requirements.txt` | Versões exatas das bibliotecas, testadas no Python 3.12 |

## Ambiente

Use **Python 3.12** (versão testada). Com [uv](https://docs.astral.sh/uv/), na pasta do projeto:

```bash
uv venv --python 3.12 .venv
uv pip install -r requirements.txt
```

Alternativa sem uv:

```bash
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

(Requer um Python 3.12 instalado no sistema. Se o comando `python3.12` não existir, use o caminho com uv acima,
que baixa o Python 3.12 automaticamente.)

**Selecionar o kernel da `.venv`:**

- **VS Code**: abra o notebook, clique em *Select Kernel* (canto superior direito), *Python Environments* e escolha `.venv (Python 3.12)`.
- **Jupyter Lab/Notebook**: registre o kernel uma vez com
  `.venv/bin/python -m ipykernel install --user --name pi4 --display-name "Python 3.12 (PI4)"`
  e escolha *Python 3.12 (PI4)* em *Kernel > Change Kernel*.
- **Linha de comando**: `.venv/bin/python -m jupyter nbconvert --to notebook --execute --inplace analise_exploratoria.ipynb`
  (o nbconvert chamado pelo Python da `.venv` usa o kernel da própria `.venv`).

**Por que não usar o Python do sistema (3.14)?** Ele não tem o `lightgbm` (e o `pip install` no Python do
sistema é bloqueado pelo PEP 668), e o `joblib` 1.4.2 instalado nele quebra qualquer `n_jobs > 1`
(RecursionError no Python 3.14), recurso usado na validação cruzada. A `.venv` isola as versões testadas.

## Como usar os dados na modelagem

A partição treino/teste foi criada pelo `analise_exploratoria.ipynb` (seção 7) e está versionada em
`resultados/split_indices.npz`. Para que todos usem exatamente as mesmas linhas, carregue os dados assim:

```python
from src.preparo import carregar_particao

X_treino, X_teste, y_treino, y_teste = carregar_particao()
# treino: 226.980 transações (378 fraudes); teste: 56.746 (95 fraudes)
# 30 atributos: V1-V28, Amount e Horas_Dia (Time fica de fora)
```

`carregar_particao()` lê a base, remove as duplicatas, cria `Horas_Dia` e aplica os índices salvos. Se o arquivo
de índices não existir, ela recria a mesma partição.

## Decisões de preparo

- **Duplicatas removidas antes da divisão**: 1.081 linhas repetidas (19 delas cópias de fraudes). Restam
  283.726 transações e 473 fraudes. Sem isso, cópias da mesma transação caem no treino e no teste e inflam a métrica.
- **Partição única e salva**: 80% treino / 20% teste, estratificada (`random_state=42`).
- **Sem escalonamento nos dados**: cada modelo deve escalonar dentro do próprio `Pipeline`, ajustado só no treino
  de cada fold (os modelos baseados em árvores dispensam escalonamento).
- **Outliers mantidos**: nas colunas `V` eles são o próprio sinal de fraude.

As recomendações da análise exploratória para a modelagem (métrica principal, escolha do limiar, validação e
cuidados com cada modelo) estão na seção 8 do `analise_exploratoria.ipynb`.
