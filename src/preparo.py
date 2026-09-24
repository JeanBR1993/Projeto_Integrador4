"""Carregamento, limpeza e partição dos dados.

Todos os notebooks usam estas funções para trabalhar exatamente com os mesmos dados
(sem duplicatas) e com a mesma divisão treino/teste, salva em arquivo.
"""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedKFold, train_test_split

# Sementes: SEED para a partição e o ajuste de hiperparâmetros;
# SEED_COMPARACAO para os folds da comparação final (folds diferentes dos usados no ajuste)
SEED = 42
SEED_COMPARACAO = 2024

# Caminhos (relativos à raiz do projeto, independentemente de onde o notebook é executado)
RAIZ_PROJETO = Path(__file__).resolve().parents[1]
# Base do Kaggle/ULB versionada comprimida (xz) no repositório; o pandas descomprime ao ler.
CAMINHO_DADOS = RAIZ_PROJETO / 'dados' / 'creditcard.csv.xz'
DIR_RESULTADOS = RAIZ_PROJETO / 'resultados'
CAMINHO_SPLIT = DIR_RESULTADOS / 'split_indices.npz'

# Colunas
ALVO = 'Class'
COLUNAS_V = [f'V{i}' for i in range(1, 29)]
COLUNAS_ORIGINAIS = ['Time'] + COLUNAS_V + ['Amount', ALVO]
# Mesma ordem de colunas do X do notebook original (V1..V28, Amount, Horas_Dia)
COLUNAS_ATRIBUTOS = COLUNAS_V + ['Amount', 'Horas_Dia']


def carregar_dados(caminho=CAMINHO_DADOS):
    """Lê o CSV original (por padrão, dados/creditcard.csv.xz, descomprimido pelo pandas).

    O índice do DataFrame é o número da linha no arquivo (0 a 284.806).
    """
    return pd.read_csv(caminho)


def remover_duplicatas(df):
    """Remove linhas repetidas em todas as colunas originais, mantendo a primeira ocorrência.

    O índice original é preservado. Retorna (df_sem_duplicatas, resumo).
    """
    repetidas = df.duplicated(subset=COLUNAS_ORIGINAIS, keep='first')
    df_limpo = df.loc[~repetidas].copy()

    resumo = {
        'linhas_antes': int(len(df)),
        'linhas_depois': int(len(df_limpo)),
        'duplicatas_removidas': int(repetidas.sum()),
        'fraudes_antes': int(df[ALVO].sum()),
        'fraudes_depois': int(df_limpo[ALVO].sum()),
        'copias_de_fraude_removidas': int(df.loc[repetidas, ALVO].sum()),
    }
    return df_limpo, resumo


def criar_atributos(df):
    """Retorna uma cópia com Horas_Dia = hora do dia (0 a 23) derivada de Time.

    Supõe que Time = 0 corresponde à meia-noite (não documentado no dataset; é coerente
    com o vale de transações entre 1h e 6h). A coluna Time é mantida porque é usada
    na partição temporal.
    """
    df = df.copy()
    df['Horas_Dia'] = ((df['Time'] // 3600) % 24).astype(int)
    return df


def preparar_dados(caminho=CAMINHO_DADOS):
    """Carrega o CSV, remove duplicatas e cria os atributos. Retorna apenas o DataFrame."""
    dados = carregar_dados(caminho)
    dados, _ = remover_duplicatas(dados)
    return criar_atributos(dados)


def dividir_treino_teste(df, test_size=0.20, seed=SEED):
    """Divisão estratificada por Class. Retorna (idx_treino, idx_teste): rótulos do índice de df."""
    idx_treino, idx_teste = train_test_split(
        df.index.to_numpy(),
        test_size=test_size,
        random_state=seed,
        stratify=df[ALVO].to_numpy(),
    )
    return idx_treino, idx_teste


def salvar_split(idx_treino, idx_teste, caminho=CAMINHO_SPLIT):
    """Salva os índices de treino e teste em um arquivo .npz (cria a pasta se preciso)."""
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(caminho, idx_treino=idx_treino, idx_teste=idx_teste)


def carregar_particao(df=None, caminho=CAMINHO_SPLIT):
    """Retorna (X_treino, X_teste, y_treino, y_teste) usando a partição salva em arquivo.

    Se df for None, os dados são preparados com preparar_dados(). Se o arquivo não
    existir, a partição é calculada com dividir_treino_teste() e salva.
    """
    if df is None:
        df = preparar_dados()
    if 'Horas_Dia' not in df.columns:
        df = criar_atributos(df)

    caminho = Path(caminho)
    if caminho.exists():
        with np.load(caminho) as arquivo:
            idx_treino = arquivo['idx_treino']
            idx_teste = arquivo['idx_teste']
    else:
        idx_treino, idx_teste = dividir_treino_teste(df)
        salvar_split(idx_treino, idx_teste, caminho)
        print(f'Aviso: partição não encontrada; nova partição criada e salva em {caminho}')

    # Validação: os índices salvos precisam existir no DataFrame recebido
    salvos = np.concatenate([idx_treino, idx_teste])
    ausentes = salvos[~np.isin(salvos, df.index.to_numpy())]
    if len(ausentes) > 0:
        raise ValueError(
            f'{len(ausentes)} índices de {caminho} não existem no DataFrame '
            f'(ex.: {ausentes[:5].tolist()}). O arquivo foi gerado com outros dados? '
            'Use preparar_dados() ou apague o arquivo para recriar a partição.'
        )
    if len(np.intersect1d(idx_treino, idx_teste)) > 0:
        raise ValueError(f'O arquivo {caminho} tem índices presentes no treino e no teste.')

    X_treino = df.loc[idx_treino, COLUNAS_ATRIBUTOS]
    X_teste = df.loc[idx_teste, COLUNAS_ATRIBUTOS]
    y_treino = df.loc[idx_treino, ALVO]
    y_teste = df.loc[idx_teste, ALVO]
    return X_treino, X_teste, y_treino, y_teste


def particao_temporal(df, quantil=0.8):
    """Partição por tempo (verificação de robustez): treino = transações até o quantil de Time,
    teste = transações posteriores. Retorna (X_treino, X_teste, y_treino, y_teste).
    """
    if 'Horas_Dia' not in df.columns:
        df = criar_atributos(df)
    corte = df['Time'].quantile(quantil)
    no_treino = df['Time'] <= corte

    X_treino = df.loc[no_treino, COLUNAS_ATRIBUTOS]
    X_teste = df.loc[~no_treino, COLUNAS_ATRIBUTOS]
    y_treino = df.loc[no_treino, ALVO]
    y_teste = df.loc[~no_treino, ALVO]
    return X_treino, X_teste, y_treino, y_teste


def cv_tuning(seed=SEED):
    """Folds do ajuste de hiperparâmetros: 5 folds estratificados."""
    return StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)


def cv_comparacao(seed=SEED_COMPARACAO):
    """Folds da comparação entre modelos: 5 folds estratificados repetidos 3 vezes (15 medidas)."""
    return RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=seed)
