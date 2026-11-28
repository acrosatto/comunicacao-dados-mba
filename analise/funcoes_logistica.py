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
from matplotlib.ticker import FuncFormatter, PercentFormatter
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
    return pd.DataFrame.from_dict(linhas, orient='index').rename_axis('coluna')


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
                color=CORES['principal'], label='taxa de cancelamento', clip_on=False)
        # os eixos se encontram no 0: sem folga antes do primeiro nível, e o eixo y começa em 0%
        ax.set_xlim(0, len(tabela) - 1)
        ax.set_ylim(bottom=0)
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
    return pd.DataFrame.from_dict(linhas, orient='index').rename_axis('caso')


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
    DataFrame da taxa_por_nivel, com a coluna mediana (mediana da variável na faixa),
    o intervalo de confiança também na escala do logito (logito_inf, logito_sup) e,
    nas faixas por quantis, a coluna decil (ou quantil) com o número da faixa, de 1 em diante.
    """
    if limites is None:
        faixa = pd.qcut(base[variavel], n_faixas, duplicates='drop')
    else:
        faixa = pd.cut(base[variavel], limites)
    dados = base.assign(_faixa=faixa)
    tabela = taxa_por_nivel(dados, '_faixa', y=y)
    tabela['mediana'] = dados.groupby('_faixa', observed=True)[variavel].median()
    if limites is None:
        tabela.insert(0, 'decil' if n_faixas == 10 else 'quantil', range(1, len(tabela) + 1))
    ic = tabela[['ic_inf', 'ic_sup']].clip(1e-4, 1 - 1e-4)
    tabela['logito_inf'] = np.log(ic['ic_inf'] / (1 - ic['ic_inf']))
    tabela['logito_sup'] = np.log(ic['ic_sup'] / (1 - ic['ic_sup']))
    tabela.index.name = variavel
    return tabela


def grafico_logito(tabela, titulo='', rotulo_x='', taxa_geral=None, posicao=None, ax=None):
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
    posicao : sequência, opcional
        Posição horizontal de cada ponto. Por padrão, a mediana da faixa. Para contagens
        com cauda juntada (por exemplo, 4+), use 0, 1, 2... e rotule o eixo no notebook.
    ax : eixo do matplotlib, opcional

    Retorna
    -------
    O eixo do matplotlib.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(6, 3.8))
    erro = [tabela['logito'] - tabela['logito_inf'], tabela['logito_sup'] - tabela['logito']]
    x = tabela['mediana'] if posicao is None else list(posicao)
    ax.plot(x, tabela['logito'], color=CORES['principal'], linewidth=1, alpha=0.5, clip_on=False)
    pontos = ax.errorbar(x, tabela['logito'], yerr=erro, fmt='o', markersize=5, capsize=3,
                         color=CORES['principal'], label='logito (IC 95%)')
    if min(x) == 0:
        # o eixo x começa no 0, encostado no eixo y (sem a folga padrão do matplotlib)
        ax.set_xlim(left=0)
        for parte in pontos.lines[0:1] + pontos.lines[1] + pontos.lines[2]:
            parte.set_clip_on(False)
    if taxa_geral is not None:
        ax.axhline(np.log(taxa_geral / (1 - taxa_geral)), color=CORES['referencia'], linestyle='--',
                   linewidth=1, label=f'taxa geral ({taxa_geral:.1%})'.replace('.', ','))
    ax.set_title(titulo)
    ax.set_xlabel(rotulo_x)
    ax.set_ylabel('logito de p (p = taxa de cancelamento)')
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f'{v:g}'.replace('.', ',')))   # -0,5
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


# -----------------------------------------------------------------------------
# Base do modelo
# -----------------------------------------------------------------------------
def preparar_base(hotel):
    """Aplica o escopo e a limpeza propostos no notebook 01 (seções 4 e 5).

    Escopo: só reservas sem depósito (No Deposit). Limpeza: tira as reservas com
    `children` vazio, as sem hóspede, as diárias fora de 0 a 1.000 e as reservas com
    zero noites (notebook 01, seção 4.4). Acrescenta as
    colunas derivadas usadas na análise: total de noites, total de hóspedes e se a
    linha tem gêmea idêntica na base original.

    Parâmetros
    ----------
    hotel : DataFrame
        A base original, como lida do CSV (antes de qualquer coluna nova, para a
        marcação de linhas idênticas usar só as colunas originais).

    Retorna
    -------
    base : DataFrame
        As reservas que ficam, com as colunas noites, hospedes e tem_gemea.
    passos : DataFrame
        Quantas reservas ficam e quantas saem em cada passo.
    """
    hospedes = hotel['adults'] + hotel['children'].fillna(0) + hotel['babies']
    noites = hotel['stays_in_weekend_nights'] + hotel['stays_in_week_nights']
    tem_gemea = hotel.duplicated(keep=False)

    condicoes = {
        'sem depósito (escopo)': hotel['deposit_type'] == 'No Deposit',
        'children preenchido': hotel['children'].notna(),
        'com hóspede': hospedes > 0,
        'diária entre 0 e 1.000': hotel['adr'].between(0, 1000),
        'com pelo menos uma noite': noites > 0,
    }
    manter = pd.Series(True, index=hotel.index)
    ficam = {'base inteira': len(hotel)}
    for nome, condicao in condicoes.items():
        manter &= condicao
        ficam[nome] = int(manter.sum())
    passos = pd.DataFrame({'reservas': ficam, 'saem neste passo': -pd.Series(ficam).diff()}).rename_axis('passo')

    base = hotel[manter].assign(noites=noites[manter], hospedes=hospedes[manter], tem_gemea=tem_gemea[manter])
    return base, passos


# -----------------------------------------------------------------------------
# Exibição das tabelas
# -----------------------------------------------------------------------------
def tabela_simples(tabela, casas=4):
    """Tabela com todos os nomes de coluna numa linha só, sem o índice à parte.

    O índice (o rótulo das linhas) vira coluna comum, e a exibição esconde o índice.
    Números decimais saem com `casas` casas (4 por padrão: com 3, 36.000 parece milhar
    em português); números inteiros guardados como decimal saem sem casas (49, e não
    49.0000), e valores não nulos menores que a última casa saem como < 0.0001.
    Vazios saem em branco. Índices sem nome recebem um nome padrão quando dá:
    variavel e nivel nas tabelas que juntam variáveis, linha no número da linha da base.

    Parâmetros
    ----------
    tabela : DataFrame
    casas : int

    Retorna
    -------
    Styler do pandas, pronto para exibir no notebook.
    """
    t = tabela.copy()
    if not (isinstance(t.index, pd.RangeIndex) and t.index.name is None):
        nomes = list(t.index.names)
        if all(n is None for n in nomes):
            if len(nomes) == 2:
                nomes = ['variavel', 'nivel']                  # tabelas que juntam várias variáveis
            elif pd.api.types.is_integer_dtype(t.index):
                nomes = ['linha']                              # número da linha na base
        # níveis ainda sem nome viram colunas sem título (nomes em branco distintos)
        t.index = t.index.set_names([n if n is not None else ' ' * (i + 1) for i, n in enumerate(nomes)])
        t = t.reset_index()
    if not isinstance(t.columns, pd.MultiIndex):
        t.columns.name = None

    def numero(v):
        if isinstance(v, (float, np.floating)):
            if np.isnan(v):
                return ''
            if float(v).is_integer():
                return f'{v:.0f}'                             # 49.0 sai como 49
            if abs(v) < 0.5 * 10 ** -casas:
                return f'< {10 ** -casas:.{casas}f}'          # não zero, mas pequeno demais para as casas
            return f'{v:.{casas}f}'
        return v

    return t.style.hide(axis='index').format(numero)


def usar_tabelas_simples(casas=4):
    """Faz o notebook exibir toda tabela (DataFrame) no formato de tabela_simples.

    Chamar uma vez, logo depois dos imports. Vale para as tabelas mostradas no fim de
    uma célula e para as mostradas com display().
    """
    from IPython import get_ipython
    ipython = get_ipython()
    if ipython is not None:
        ipython.display_formatter.formatters['text/html'].for_type(
            pd.DataFrame, lambda tabela: tabela_simples(tabela, casas).to_html())


# -----------------------------------------------------------------------------
# Escolha das faixas
# -----------------------------------------------------------------------------
def comparar_cortes(base, variavel, opcoes, formulas=None, y='is_canceled'):
    """Compara opções de faixas para uma variável numérica pelo AIC.

    Cada opção vira uma regressão logística só com aquela variável, em faixas. O AIC
    mede o ajuste e pune cada coeficiente a mais: quanto menor, melhor. Uma diferença
    de AIC abaixo de uns 2 pontos não distingue duas opções. O BIC pune cada coeficiente
    com mais força (cresce com o tamanho da base) e favorece opções mais simples.

    Parâmetros
    ----------
    base : DataFrame
    variavel : str
        Coluna numérica.
    opcoes : dict
        {nome da opção: limites das faixas}, no formato do pd.cut (fechadas à direita).
    formulas : dict, opcional
        {nome: fórmula} de outros modelos para comparar, como a variável como número
        ('is_canceled ~ lead_time') ou o modelo sem nenhuma variável ('is_canceled ~ 1').
    y : str
        Coluna 0/1 do evento.

    Retorna
    -------
    DataFrame ordenado pelo AIC, com o número de faixas, n_coeficientes, AIC e BIC (e a diferença de cada um
    para a melhor opção),
    menor_faixa (parcela da base na menor faixa) e a taxa de cada faixa, em ordem.
    """
    import statsmodels.api as sm
    import statsmodels.formula.api as smf

    def ajustar(formula, dados):
        modelo = smf.glm(formula, data=dados, family=sm.families.Binomial()).fit()
        bic = -2 * modelo.llf + (modelo.df_model + 1) * np.log(len(dados))
        return modelo.aic, bic, int(modelo.df_model)

    linhas = []
    for nome, formula in (formulas or {}).items():
        aic, bic, n_coef = ajustar(formula, base)
        linhas.append({'opcao': nome, 'faixas': np.nan, 'n_coeficientes': n_coef, 'AIC': aic, 'BIC': bic,
                       'menor_faixa': np.nan, 'taxa_por_faixa': ''})
    for nome, limites in opcoes.items():
        faixa = pd.cut(base[variavel], limites)
        aic, bic, n_coef = ajustar(f'{y} ~ C(_faixa)', base.assign(_faixa=faixa.astype(str)))
        grupos = base.groupby(faixa, observed=True)[y]
        linhas.append({'opcao': nome, 'faixas': len(limites) - 1, 'n_coeficientes': n_coef, 'AIC': aic, 'BIC': bic,
                       'menor_faixa': grupos.size().min() / len(base),
                       'taxa_por_faixa': ' / '.join(f'{t:.1%}'.replace('.', ',') for t in grupos.mean())})
    tabela = pd.DataFrame(linhas).sort_values('AIC')
    tabela.insert(4, 'dif_AIC', tabela['AIC'] - tabela['AIC'].min())
    tabela.insert(6, 'dif_BIC', tabela['BIC'] - tabela['BIC'].min())
    return tabela.set_index('opcao').round({'AIC': 1, 'dif_AIC': 1, 'BIC': 1, 'dif_BIC': 1})


def cortes_por_ganho(base, variavel, min_faixa=0.005, ganho_minimo=0.0005, max_faixas=15, y='is_canceled'):
    """Faixas escolhidas por uma árvore de decisão com ganho de informação, um corte por vez.

    A árvore testa todos os cortes possíveis da variável e escolhe o que dá o maior ganho
    de informação: a maior queda na entropia (em bits) do y, ponderada pelo tamanho dos
    grupos. A cada passo, ela pode fazer mais um corte. O processo para quando o próximo
    corte traz menos que `ganho_minimo` de ganho, ou quando um corte criaria uma faixa
    com menos que `min_faixa` da base.

    Parâmetros
    ----------
    base : DataFrame
    variavel : str
        Coluna numérica (de valores inteiros, como dias ou noites).
    min_faixa : float
        Parcela mínima da base em cada faixa.
    ganho_minimo : float
        Ganho de informação mínimo (em bits) para aceitar mais um corte.
    max_faixas : int
        Limite de segurança para o número de faixas.
    y : str
        Coluna 0/1 do evento.

    Retorna
    -------
    DataFrame com um passo por linha: número de faixas, o corte novo, o ganho que ele
    trouxe, o ganho acumulado, se o corte foi aceito e os cortes até ali. Um corte em c
    quer dizer "até c" e "acima de c".
    """
    from sklearn.tree import DecisionTreeClassifier

    def entropia(p):
        p = np.clip(p, 1e-12, 1 - 1e-12)
        return -(p * np.log2(p) + (1 - p) * np.log2(1 - p))

    def entropia_media(cortes):
        faixa = pd.cut(base[variavel], [-np.inf] + list(cortes) + [np.inf])
        grupos = base.groupby(faixa, observed=True)[y]
        return float((grupos.size() / len(base) * entropia(grupos.mean())).sum())

    inicial = float(entropia(base[y].mean()))
    linhas, anteriores, parou = [], [], False
    for n_faixas in range(2, max_faixas + 1):
        arvore = DecisionTreeClassifier(criterion='entropy', max_leaf_nodes=n_faixas,
                                        min_samples_leaf=int(np.ceil(min_faixa * len(base))), random_state=0)
        arvore.fit(base[[variavel]], base[y])
        cortes = sorted(int(np.floor(t)) for t in arvore.tree_.threshold if t != -2)
        if len(cortes) < n_faixas - 1:
            break                                             # a árvore não acha mais cortes válidos
        novo = [c for c in cortes if c not in anteriores]
        ganho = (inicial - entropia_media(cortes)) - (inicial - entropia_media(anteriores))
        aceito = (not parou) and ganho >= ganho_minimo
        parou = parou or not aceito
        linhas.append({'faixas': n_faixas, 'corte_novo': ', '.join(map(str, novo)), 'ganho': ganho,
                       'ganho_acumulado': inicial - entropia_media(cortes), 'aceito': 'sim' if aceito else 'não',
                       'cortes': ', '.join(map(str, cortes))})
        anteriores = cortes
        if parou and len(linhas) >= 3 and all(l['aceito'] == 'não' for l in linhas[-2:]):
            break                                             # mostra só dois passos depois da parada
    return pd.DataFrame(linhas).set_index('faixas')


def conferir_cortes_por_periodo(base, variavel, passos, periodo='arrival_date_year', y='is_canceled'):
    """Tira os cortes da árvore que não valem nos dois períodos da base.

    Em cada par de faixas vizinhas, a faixa de cima precisa cancelar mais que a de baixo
    nos dois períodos, ou menos nos dois. Se a ordem se inverte em algum par, sai, entre
    os cortes que invertem, o de menor ganho de informação. A conferência se repete com
    as faixas que sobram, até todos os cortes valerem nos dois períodos.

    Parâmetros
    ----------
    base : DataFrame
        Só os dados usados nas decisões (o treino), nunca o teste.
    variavel : str
        Coluna numérica de valores inteiros.
    passos : DataFrame
        Saída de cortes_por_ganho: usa os cortes aceitos e o ganho de cada um.
    periodo : str
        Coluna com os dois períodos comparados (por exemplo, o ano de chegada).
    y : str
        Coluna 0/1 do evento.

    Retorna
    -------
    cortes : list
        Os cortes que ficam, em ordem.
    tabela : DataFrame
        Uma linha por faixa em cada rodada: a taxa em cada período e se a ordem em
        relação à faixa anterior é a mesma nos dois (sim ou não).
    saidas : list
        Uma frase por rodada que tirou um corte.
    """
    aceitos = passos[passos['aceito'] == 'sim']
    ganho = {int(c): g for c, g in zip(aceitos['corte_novo'], aceitos['ganho'])}
    cortes, tabelas, saidas = sorted(ganho), {}, []
    if not cortes:
        return [], pd.DataFrame(), ['A árvore não aceitou nenhum corte: não há o que conferir.']
    minimo = int(base[variavel].min())

    def nomes(cortes):
        limites = [minimo - 1] + cortes
        rotulos = [str(b) if a + 1 == b else f'{a + 1}–{b}' for a, b in zip(limites[:-1], limites[1:])]
        return rotulos + [f'mais de {cortes[-1]}']

    rodada = 1
    while True:
        faixa = pd.cut(base[variavel], [-np.inf] + cortes + [np.inf], labels=nomes(cortes))
        t = base.groupby([faixa, periodo], observed=True)[y].mean().unstack()
        sobe = np.sign(t.diff())
        igual = (sobe.iloc[:, 0] == sobe.iloc[:, 1]).to_numpy()
        t.columns = [f'taxa_{c}' for c in t.columns]
        t['mesma_ordem'] = ['' if i == 0 else ('sim' if ok else 'não') for i, ok in enumerate(igual)]
        tabelas[rodada] = t
        invertem = [c for c, ok in zip(cortes, igual[1:]) if not ok]
        if not invertem:
            break
        sai = min(invertem, key=ganho.get)
        saidas.append(f'Rodada {rodada}: o corte em {sai} inverte a ordem entre os períodos e sai.')
        cortes.remove(sai)
        rodada += 1
    tabela = pd.concat(tabelas, names=['rodada', 'faixa'])
    return cortes, tabela, saidas


def desenhar_arvore(base, variavel, n_faixas, unidade, titulo, ultima='mais de', examinar=(), min_faixa=0.005,
                    y='is_canceled'):
    """Desenha a árvore de decisão (ganho de informação) que corta uma variável em faixas.

    Cada pergunta mostra o corte ("até 8 dias?"), a parcela das reservas que chega até ela,
    a taxa de cancelamento e o ganho de informação do corte. As folhas, embaixo, são as
    faixas finais, com a parcela das reservas e a taxa de cancelamento de cada uma.

    Parâmetros
    ----------
    base : DataFrame
    variavel : str
        Coluna numérica de valores inteiros.
    n_faixas : int
        Número de faixas (folhas) da árvore.
    unidade : str
        Unidade no plural, para os textos (por exemplo, 'dias' ou 'noites'). O singular
        ('dia', 'noite') é usado quando o valor é 1.
    titulo : str
    ultima : str
        Como nomear a última faixa: 'mais de' ("mais de 257 dias") ou 'ou mais'
        ("4 noites ou mais").
    examinar : sequência de int
        Cortes a destacar (borda tracejada e a nota "examinado abaixo"), junto com as
        faixas que eles criam.
    min_faixa : float
        Parcela mínima da base em cada faixa.
    y : str
        Coluna 0/1 do evento.

    Retorna
    -------
    Lista dos cortes, em ordem (um corte em c quer dizer "até c" e "acima de c").
    """
    from sklearn.tree import DecisionTreeClassifier

    arvore = DecisionTreeClassifier(criterion='entropy', max_leaf_nodes=n_faixas,
                                    min_samples_leaf=int(np.ceil(min_faixa * len(base))), random_state=0)
    arvore.fit(base[[variavel]], base[y])
    t = arvore.tree_
    total = t.n_node_samples[0]

    def entropia(p):
        p = min(max(p, 1e-12), 1 - 1e-12)
        return -(p * np.log2(p) + (1 - p) * np.log2(1 - p))

    def taxa(no):
        valor = t.value[no][0]
        return valor[1] / valor.sum()

    def ganho(no):
        e, d = t.children_left[no], t.children_right[no]
        n, ne, nd = t.n_node_samples[no], t.n_node_samples[e], t.n_node_samples[d]
        return n / total * (entropia(taxa(no)) - ne / n * entropia(taxa(e)) - nd / n * entropia(taxa(d)))

    # posições: folhas lado a lado, na ordem dos valores; cada pergunta no meio dos seus ramos
    posicao, profundidade, folhas = {}, {}, []

    def percorrer(no, nivel, minimo, maximo):
        profundidade[no] = nivel
        if t.children_left[no] == -1:
            posicao[no] = len(folhas)
            folhas.append((no, minimo, maximo))
            return
        corte = int(np.floor(t.threshold[no]))
        percorrer(t.children_left[no], nivel + 1, minimo, corte)
        percorrer(t.children_right[no], nivel + 1, corte + 1, maximo)
        posicao[no] = (posicao[t.children_left[no]] + posicao[t.children_right[no]]) / 2

    percorrer(0, 0, int(base[variavel].min()), None)   # a primeira faixa começa no menor valor dos dados
    altura = max(profundidade.values())
    fonte = 9 if len(folhas) <= 6 else 7.5   # com mais de 6 folhas, as caixas vizinhas se encostariam

    singular = unidade[:-1] if unidade.endswith('s') else unidade

    def com_unidade(valor):
        return f'{valor} {singular if valor == 1 else unidade}'

    def nome_faixa(minimo, maximo):
        if minimo is None:
            return com_unidade(maximo) if maximo == 0 else f'até {com_unidade(maximo)}'
        if maximo is None:
            return f'mais de {com_unidade(minimo - 1)}' if ultima == 'mais de' else f'{com_unidade(minimo)} ou mais'
        return com_unidade(minimo) if minimo == maximo else f'{minimo} a {maximo} {unidade}'

    def pct(v):
        return f'{v:.1%}'.replace('.', ',')

    fig, ax = plt.subplots(figsize=(12, 1.6 * (altura + 1) + 0.8))
    caixa_pergunta = dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor=CORES['referencia'])
    caixa_folha = dict(boxstyle='round,pad=0.5', facecolor='#eef1f8', edgecolor=CORES['principal'])
    destacados = set()
    for no in posicao:
        x, yy = posicao[no], -profundidade[no]
        if t.children_left[no] != -1:
            for filho, rotulo in [(t.children_left[no], 'sim'), (t.children_right[no], 'não')]:
                xf, yf = posicao[filho], -profundidade[filho]
                ax.plot([x, xf], [yy, yf], color=CORES['referencia'], linewidth=1, zorder=1)
                ax.text((x + xf) / 2, (yy + yf) / 2, rotulo, fontsize=9, color='#555555', ha='center', va='center',
                        bbox=dict(facecolor='white', edgecolor='none', pad=1), zorder=2)
            corte = int(np.floor(t.threshold[no]))
            if corte == 0:
                pergunta = 'no mesmo dia (0 dias)?' if unidade == 'dias' else f'zero {unidade}?'
            else:
                pergunta = f'até {com_unidade(corte)}?'
            ganho_txt = f'{ganho(no):.4f}'.replace('.', ',')
            texto = (f'{pergunta}\n{pct(t.n_node_samples[no] / total)} das reservas · cancela {pct(taxa(no))}\n'
                     f'ganho do corte: {ganho_txt}')
            destaque = corte in examinar
            if destaque:
                texto += '\nexaminado abaixo'
                destacados.update([t.children_left[no], t.children_right[no]])
            caixa = dict(caixa_pergunta, linestyle='--') if destaque else caixa_pergunta
            ax.text(x, yy, texto, fontsize=fonte, ha='center', va='center', bbox=caixa, zorder=3, color='#333333')
    for no, minimo, maximo in folhas:
        x, yy = posicao[no], -profundidade[no]
        texto = f'{nome_faixa(minimo, maximo)}\n{pct(t.n_node_samples[no] / total)} das reservas\ncancela {pct(taxa(no))}'
        caixa = dict(caixa_folha, linestyle='--', facecolor='white') if no in destacados else caixa_folha
        ax.text(x, yy, texto, fontsize=fonte, ha='center', va='center', bbox=caixa, zorder=3, color='#333333')
    ax.set_xlim(-0.6, len(folhas) - 0.4)
    ax.set_ylim(-altura - 0.6, 0.6)
    ax.axis('off')
    ax.set_title(titulo)
    plt.show()
    return sorted(int(np.floor(c)) for c in t.threshold if c != -2)
