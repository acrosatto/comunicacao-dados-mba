"""
Funções de apoio para a análise de cancelamento de reservas (regressão logística).

Organização:
- Cálculo e gráfico ficam em funções separadas. As de cálculo devolvem uma tabela
  (DataFrame), para o notebook decidir o que mostrar e para os números poderem ir
  para a apresentação. As de gráfico recebem essa tabela e só desenham.
- O que já existe pronto em bibliotecas (pandas, scipy, statsmodels, scikit-learn)
  é usado diretamente. Aqui fica só a organização e o padrão do projeto.
- As funções entram neste arquivo conforme as seções dos notebooks precisam delas.

Uso, a partir de um notebook em analise/<pessoa>/:

    import sys
    sys.path.append('..')
    from funcoes_logistica import aplicar_estilo, resumo_colunas
"""

import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------------------------------------------------------
# Padrão visual
# -----------------------------------------------------------------------------
# Uma cor por papel, a mesma em todos os gráficos do projeto.
CORES = {
    'principal': '#2b4fa3',    # série única; reservas canceladas (y = 1)
    'secundaria': '#e07b39',   # reservas que vieram (y = 0), quando os dois grupos aparecem juntos
    'referencia': '#6b6b6b',   # linhas de referência, como a taxa geral de cancelamento
}


def aplicar_estilo():
    """Aplica o padrão visual do projeto a todos os gráficos do notebook.

    Sem as bordas do topo e da direita, grade horizontal leve e tamanho de fonte
    legível. Chamar uma vez, logo depois dos imports.
    """
    plt.rcParams.update({
        'figure.dpi': 100,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.grid': True,
        'axes.grid.axis': 'y',
        'grid.alpha': 0.3,
        'axes.titlesize': 11,
        'axes.labelsize': 10,
    })


# -----------------------------------------------------------------------------
# Conhecendo os dados
# -----------------------------------------------------------------------------
def _formatar_inteiro(n):
    """1234567 -> '1.234.567' (separador de milhar brasileiro)."""
    return f'{n:,}'.replace(',', '.')


def resumo_colunas(base, n_frequentes=3):
    """Uma linha por coluna: tipo, nº de valores distintos, missing e valores mais comuns.

    Serve para a primeira olhada na base: mostra de uma vez onde há missing, quais
    colunas têm poucos ou muitos níveis e se algum valor muito repetido pode ser um
    código disfarçado (por exemplo, 0 ou 'Undefined').

    Parâmetros
    ----------
    base : DataFrame
    n_frequentes : int
        Quantos valores mais comuns mostrar por coluna.

    Retorna
    -------
    DataFrame com as colunas tipo, n_niveis, missing, pct_missing e mais_frequentes.
    """
    linhas = {}
    for coluna in base.columns:
        serie = base[coluna]
        frequentes = serie.value_counts().head(n_frequentes)
        linhas[coluna] = {
            'tipo': str(serie.dtype),
            'n_niveis': serie.nunique(),
            'missing': int(serie.isna().sum()),
            'pct_missing': serie.isna().mean(),
            'mais_frequentes': ' | '.join(
                f'{valor} ({_formatar_inteiro(n)})' for valor, n in frequentes.items()
            ),
        }
    return pd.DataFrame.from_dict(linhas, orient='index')
