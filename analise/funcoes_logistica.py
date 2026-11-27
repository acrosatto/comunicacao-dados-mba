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

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
from statsmodels.stats.proportion import proportion_confint


# -----------------------------------------------------------------------------
# Padrão visual
# -----------------------------------------------------------------------------
# Uma cor por papel, a mesma em todos os gráficos do projeto.
CORES = {
    'principal': '#2b4fa3',    # série única; reservas canceladas (y = 1)
    'secundaria': '#e07b39',   # reservas que vieram (y = 0), quando os dois grupos aparecem juntos
    'referencia': '#a6a6a6',   # linhas de referência (como a taxa geral), eixos e marcas dos eixos
}


def aplicar_estilo():
    """Aplica o padrão visual do projeto a todos os gráficos do notebook.

    Sem as bordas do topo e da direita, eixos e marcas em cinza claro (para não
    competir com os dados), grade horizontal leve, tamanho de fonte legível e
    espaço entre o título e o gráfico e entre os títulos dos eixos e os números. Os
    textos dos eixos continuam escuros, para a leitura. Chamar uma vez, logo depois
    dos imports.
    """
    plt.rcParams.update({
        'figure.dpi': 100,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.edgecolor': CORES['referencia'],
        'xtick.color': CORES['referencia'],
        'ytick.color': CORES['referencia'],
        'xtick.labelcolor': '#333333',
        'ytick.labelcolor': '#333333',
        'axes.grid': True,
        'axes.grid.axis': 'y',
        'grid.alpha': 0.3,
        'axes.titlesize': 11,
        'axes.labelsize': 10,
        'axes.titlepad': 14,   # espaço entre o título e o gráfico
        'axes.labelpad': 10,   # espaço entre os títulos dos eixos e os números
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


# -----------------------------------------------------------------------------
# Taxa de cancelamento por grupo
# -----------------------------------------------------------------------------
def taxa_por_nivel(base, variavel, y='is_canceled', confianca=0.95):
    """Taxa do evento (y = 1) em cada nível de uma variável, com intervalo de confiança.

    Para cada nível: n, % da base, nº de eventos, taxa, intervalo de confiança da taxa
    e logito empírico.

    - Intervalo de confiança de Wilson: mais confiável que o intervalo "p ± 1,96·erro"
      quando o nível tem poucas linhas ou a taxa está perto de 0% ou 100%.
    - Logito empírico: ln((eventos + 0,5) / (não eventos + 0,5)). O 0,5 evita
      log(0) quando um nível não tem nenhum evento (ou só tem eventos).

    Parâmetros
    ----------
    base : DataFrame
    variavel : str
        Coluna que define os grupos. Os níveis saem na ordem natural da coluna
        (numérica, de data ou categórica ordenada); para texto, em ordem alfabética.
    y : str
        Coluna 0/1 do evento.
    confianca : float
        Nível do intervalo de confiança.

    Retorna
    -------
    DataFrame indexado pelos níveis, com as colunas n, pct_base, eventos, taxa,
    ic_inf, ic_sup e logito.
    """
    tabela = base.groupby(variavel, observed=True)[y].agg(n='size', eventos='sum')
    tabela['pct_base'] = tabela['n'] / tabela['n'].sum()
    tabela['taxa'] = tabela['eventos'] / tabela['n']
    tabela['ic_inf'], tabela['ic_sup'] = proportion_confint(
        tabela['eventos'], tabela['n'], alpha=1 - confianca, method='wilson'
    )
    nao_eventos = tabela['n'] - tabela['eventos']
    tabela['logito'] = np.log((tabela['eventos'] + 0.5) / (nao_eventos + 0.5))
    return tabela[['n', 'pct_base', 'eventos', 'taxa', 'ic_inf', 'ic_sup', 'logito']]


def grafico_taxa_por_nivel(tabela, taxa_geral=None, titulo='', linha=False, ax=None):
    """Desenha a taxa de cada nível com o intervalo de confiança (saída de taxa_por_nivel).

    Parâmetros
    ----------
    tabela : DataFrame
        Saída de taxa_por_nivel.
    taxa_geral : float, opcional
        Taxa da base inteira, desenhada como linha de referência tracejada.
    titulo : str
    linha : bool
        False: pontos com barras de erro, para níveis sem ordem (hotel, segmento).
        True: linha com faixa de confiança, para níveis em sequência (meses, faixas).
    ax : eixo do matplotlib, opcional
        Para desenhar dentro de uma figura com vários gráficos.

    Retorna
    -------
    O eixo do matplotlib, para ajustes finos no notebook.
    """
    if ax is None:
        largura = max(6, min(14, 0.45 * len(tabela) + 3))
        _, ax = plt.subplots(figsize=(largura, 3.8))
    posicoes = np.arange(len(tabela))
    rotulos = [str(nivel) for nivel in tabela.index]

    if linha:
        ax.fill_between(posicoes, tabela['ic_inf'], tabela['ic_sup'],
                        color=CORES['principal'], alpha=0.15, linewidth=0, label='IC 95%')
        ax.plot(posicoes, tabela['taxa'], marker='o', markersize=4,
                color=CORES['principal'], label='taxa de cancelamento')
    else:
        erro = [tabela['taxa'] - tabela['ic_inf'], tabela['ic_sup'] - tabela['taxa']]
        ax.errorbar(posicoes, tabela['taxa'], yerr=erro, fmt='o', capsize=4,
                    color=CORES['principal'], label='taxa de cancelamento (IC 95%)')

    if taxa_geral is not None:
        ax.axhline(taxa_geral, color=CORES['referencia'], linestyle='--', linewidth=1,
                   label=f'taxa geral ({taxa_geral:.1%})'.replace('.', ','))

    passo = max(1, len(rotulos) // 15)   # no máximo uns 15 rótulos no eixo x
    ax.set_xticks(posicoes[::passo], rotulos[::passo],
                  rotation=45 if len(rotulos) > 6 else 0,
                  ha='right' if len(rotulos) > 6 else 'center')
    ax.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    ax.set_ylabel('cancelamento')
    ax.set_title(titulo)
    ax.legend(frameon=False, fontsize=9)
    return ax


# -----------------------------------------------------------------------------
# Qualidade dos dados
# -----------------------------------------------------------------------------
def contar_casos(base, casos, y='is_canceled'):
    """Quantas linhas atendem a cada condição e quanto elas cancelam.

    Serve para checar de uma vez uma lista de situações suspeitas (reserva sem
    hóspede, diária negativa...). A taxa de cancelamento ajuda a decidir: um grupo
    pequeno que cancela igual ao resto pesa pouco; um grupo que cancela muito mais
    ou muito menos merece atenção.

    Parâmetros
    ----------
    base : DataFrame
    casos : dict
        {nome do caso: série True/False com o mesmo índice da base}.
    y : str
        Coluna 0/1 do evento.

    Retorna
    -------
    DataFrame com uma linha por caso e as colunas n, pct_base e taxa.
    """
    linhas = {}
    for nome, condicao in casos.items():
        linhas[nome] = {
            'n': int(condicao.sum()),
            'pct_base': condicao.mean(),
            'taxa': base.loc[condicao, y].mean() if condicao.any() else np.nan,
        }
    return pd.DataFrame.from_dict(linhas, orient='index')


# -----------------------------------------------------------------------------
# Linearidade no logito
# -----------------------------------------------------------------------------
def logito_por_faixa(base, variavel, n_faixas=10, limites=None, y='is_canceled'):
    """Taxa e logito empírico por faixa de uma variável numérica, com a posição de cada faixa.

    Serve para conferir se a variável pode entrar como número: na regressão logística,
    o efeito é uma reta no logito. Se o logito das faixas cai numa reta contra o valor
    típico de cada faixa, a variável entra como número; se não, vira faixas.

    Parâmetros
    ----------
    base : DataFrame
    variavel : str
        Coluna numérica.
    n_faixas : int
        Número de faixas por quantis (decis por padrão). Usado quando `limites` é None.
        Valores repetidos podem juntar quantis, e aí saem menos faixas.
    limites : lista, opcional
        Limites fixos das faixas, para contagens (por exemplo, [-1, 0, 1, 2, np.inf]).
        Os intervalos são fechados à direita, como no pd.cut.
    y : str
        Coluna 0/1 do evento.

    Retorna
    -------
    DataFrame da taxa_por_nivel, com a coluna x (mediana da variável na faixa) e o
    intervalo de confiança também na escala do logito (logito_inf, logito_sup).
    """
    if limites is None:
        faixa = pd.qcut(base[variavel], n_faixas, duplicates='drop')
    else:
        faixa = pd.cut(base[variavel], limites)
    dados = base.assign(_faixa=faixa)
    tabela = taxa_por_nivel(dados, '_faixa', y=y)
    tabela['x'] = dados.groupby('_faixa', observed=True)[variavel].median()
    ic = tabela[['ic_inf', 'ic_sup']].clip(1e-4, 1 - 1e-4)
    tabela['logito_inf'] = np.log(ic['ic_inf'] / (1 - ic['ic_inf']))
    tabela['logito_sup'] = np.log(ic['ic_sup'] / (1 - ic['ic_sup']))
    tabela.index.name = variavel
    return tabela


def grafico_logito(tabela, titulo='', rotulo_x='', taxa_geral=None, ax=None):
    """Logito empírico de cada faixa contra a mediana da faixa (saída de logito_por_faixa).

    Pontos com barras do intervalo de confiança, ligados por uma linha fina. Se o
    desenho é uma reta, a variável pode entrar como número.

    Parâmetros
    ----------
    tabela : DataFrame
        Saída de logito_por_faixa.
    titulo, rotulo_x : str
    taxa_geral : float, opcional
        Taxa da base, desenhada como linha de referência (convertida para logito).
    ax : eixo do matplotlib, opcional

    Retorna
    -------
    O eixo do matplotlib.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(6, 3.8))
    erro = [tabela['logito'] - tabela['logito_inf'], tabela['logito_sup'] - tabela['logito']]
    ax.plot(tabela['x'], tabela['logito'], color=CORES['principal'], linewidth=1, alpha=0.5)
    ax.errorbar(tabela['x'], tabela['logito'], yerr=erro, fmt='o', markersize=5, capsize=3,
                color=CORES['principal'], label='logito (IC 95%)')
    if taxa_geral is not None:
        ax.axhline(np.log(taxa_geral / (1 - taxa_geral)), color=CORES['referencia'], linestyle='--',
                   linewidth=1, label=f'taxa geral ({taxa_geral:.1%})'.replace('.', ','))
    ax.set_title(titulo)
    ax.set_xlabel(rotulo_x)
    ax.set_ylabel('logito do cancelamento')
    ax.legend(frameon=False, fontsize=9)
    return ax


# -----------------------------------------------------------------------------
# Força da associação
# -----------------------------------------------------------------------------
def v_cramer(base, variavel, y='is_canceled'):
    """V de Cramér entre uma variável categórica e o y (de 0 a 1).

    Mede a força da associação a partir do qui-quadrado da tabela cruzada, sem
    depender do tamanho da base. Serve para ordenar as candidatas. Variáveis com
    muitos níveis (como códigos de agência) tendem a ter V maior só pelo número de
    níveis, então a comparação vale melhor entre variáveis com poucos níveis.

    Parâmetros
    ----------
    base : DataFrame
    variavel : str
    y : str

    Retorna
    -------
    float
    """
    from scipy.stats import chi2_contingency
    tabela = pd.crosstab(base[variavel], base[y])
    qui2 = chi2_contingency(tabela, correction=False)[0]
    return float(np.sqrt(qui2 / (tabela.values.sum() * (min(tabela.shape) - 1))))
