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
    from funcoes import aplicar_estilo, resumo_colunas
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
    'terciaria': '#2a9d8f',    # terceira série, quando três aparecem juntas (separação conferida para daltonismo)
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


def v_cramer_pares(base, variaveis):
    """V de Cramér entre cada par de variáveis categóricas.

    Parâmetros
    ----------
    base : DataFrame
    variaveis : list de str

    Retorna
    -------
    matriz : DataFrame quadrado (variáveis × variáveis), com 1 na diagonal.
    """
    matriz = pd.DataFrame(1.0, index=variaveis, columns=variaveis)
    for i, a in enumerate(variaveis):
        for b in variaveis[i + 1:]:
            matriz.loc[a, b] = matriz.loc[b, a] = v_cramer(base, a, y=b)
    return matriz


def grafico_v_cramer(matriz, titulo='', subtitulo='', nomes=None):
    """Mapa de calor do V de Cramér entre pares: só o triângulo de baixo, com o valor
    escrito em cada casa. Uma cor só, do claro (associação fraca) ao escuro (forte).

    Parâmetros
    ----------
    matriz : DataFrame
        Saída de `v_cramer_pares`.
    titulo, subtitulo : str
        O subtítulo sai em cinza, logo abaixo do título.
    nomes : dict, opcional
        Nome de exibição de cada variável.
    """
    from matplotlib.colors import LinearSegmentedColormap
    rotulos = [nomes.get(v, v) if nomes else v for v in matriz.index]
    n = len(matriz)
    valores = matriz.to_numpy().copy()
    valores[np.triu_indices(n)] = np.nan              # só os pares abaixo da diagonal
    cores = LinearSegmentedColormap.from_list('v', ['#f4f6fb', CORES['principal']])

    fig, ax = plt.subplots(figsize=(12, 9))
    ax.imshow(valores, cmap=cores, vmin=0, vmax=1)
    ax.grid(False)
    for i in range(n):
        for j in range(i):
            v = valores[i, j]
            ax.text(j, i, f'{v:.2f}'.replace('.', ','), ha='center', va='center', fontsize=9,
                    color='white' if v > 0.5 else '#333333')
    ax.set_xticks(range(n - 1), rotulos[:-1], rotation=45, ha='right')
    ax.set_yticks(range(1, n), rotulos[1:])
    ax.set_xlim(-0.5, n - 1.5)
    ax.set_ylim(n - 0.5, 0.5)
    for lado in ax.spines.values():
        lado.set_visible(False)
    ax.tick_params(length=0)
    fig.suptitle(titulo, fontsize=12, x=0.5, y=0.98)
    if subtitulo:
        fig.text(0.5, 0.94, subtitulo, ha='center', fontsize=10, color='#666666')
    return ax


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
# Variáveis do modelo
# -----------------------------------------------------------------------------
# Situação de cada variável ao fim do 02_variaveis (seção 3): "entra" ou "candidata"
# (a candidata depende do teste com as outras variáveis no modelo).
SITUACAO_VARIAVEIS = {
    'antecedencia': 'entra', 'noites': 'entra', 'diaria': 'candidata',
    'sozinho': 'entra', 'duas_criancas': 'entra', 'com_bebe': 'candidata',
    'pedido_especial': 'candidata', 'ja_veio': 'entra', 'hotel': 'entra',
    'segmento': 'entra', 'canal': 'candidata', 'tem_agencia': 'candidata',
    'paga_empresa': 'entra', 'temporada': 'entra',
}

# Nome de cada variável nos gráficos e nas tabelas para leitura.
NOMES_VARIAVEIS = {
    'antecedencia': 'antecedência', 'noites': 'noites', 'diaria': 'diária',
    'sozinho': 'sozinho', 'duas_criancas': '2 ou mais crianças', 'com_bebe': 'com bebê',
    'pedido_especial': 'pedido especial', 'ja_veio': 'já veio', 'hotel': 'hotel',
    'segmento': 'segmento', 'canal': 'canal', 'tem_agencia': 'tem agência',
    'paga_empresa': 'paga por empresa', 'temporada': 'temporada',
    'temporada_alta': 'temporada (alta × resto)', 'segmento3': 'segmento (3 níveis)',
    'online_ate8': 'agência online até 8 dias',
}


def montar_variaveis(base):
    """As variáveis explicativas no formato escolhido no 02_variaveis, seção 3.

    Cada variável sai como categórica, com a referência como primeiro nível: numa
    fórmula do statsmodels, `C(variavel)` já usa essa referência. Todos os cortes são
    valores fixos (dias, euros, meses, categorias), sem nada calculado a partir das
    linhas da base; por isso a mesma função vale para o treino e para o teste.

    Parâmetros
    ----------
    base : DataFrame
        Saída de `preparar_base` (precisa da coluna noites).

    Retorna
    -------
    DataFrame com o mesmo índice da base: is_canceled, arrival_date_year, as
    variáveis de SITUACAO_VARIAVEIS e três formas testadas no 05_modelo, seção 4:
    temporada_alta (julho e agosto × resto do ano), segmento3 (agência online, grupos e
    demais) e online_ate8 (agência online com até 8 dias de antecedência, a interação
    entre o segmento e a antecedência).
    """
    def niveis(valores, ordem):
        return pd.Categorical(valores, categories=ordem)

    def sim_nao(condicao):
        return niveis(np.where(condicao, 'sim', 'não'), ['não', 'sim'])

    # pd.cut: cada faixa inclui o limite da direita; o -1 serve para incluir o 0
    antecedencia = pd.cut(base['lead_time'], [-1, 0, 8, 25, np.inf], labels=['0', '1–8', '9–25', 'mais de 25'])
    noites = pd.cut(base['noites'], [0, 1, 3, np.inf], labels=['1', '2–3', '4 ou mais'])
    diaria = pd.cut(base['adr'].round(), [-1, 59, np.inf], labels=['até 59', 'mais de 59'])   # diária arredondada para o euro
    mes = base['arrival_date_month']
    temporada = np.select([mes.isin(['January', 'March', 'November']), mes.isin(['July', 'August'])],
                          ['baixa', 'alta'], 'média')

    variaveis = pd.DataFrame({
        'antecedencia': antecedencia.cat.reorder_categories(['mais de 25', '0', '1–8', '9–25']),
        'noites': noites.cat.reorder_categories(['2–3', '1', '4 ou mais']),
        'diaria': diaria.cat.reorder_categories(['mais de 59', 'até 59']),
        'sozinho': sim_nao(base['adults'] == 1),
        'duas_criancas': sim_nao(base['children'] >= 2),
        'com_bebe': sim_nao(base['babies'] > 0),
        'pedido_especial': niveis(np.where(base['total_of_special_requests'] > 0, 'fez pedido', 'nenhum'),
                                  ['nenhum', 'fez pedido']),
        'ja_veio': niveis(np.where(base['previous_bookings_not_canceled'] > 0, 'já veio', 'nunca veio'),
                          ['nunca veio', 'já veio']),
        'hotel': niveis(base['hotel'].map({'City Hotel': 'urbano', 'Resort Hotel': 'resort'}), ['urbano', 'resort']),
        'segmento': niveis(np.where(base['market_segment'].isin(['Online TA', 'Groups']), 'agência online e grupos', 'demais'),
                           ['agência online e grupos', 'demais']),
        'canal': niveis(np.where(base['distribution_channel'] == 'TA/TO', 'agência ou operadora', 'demais'),
                        ['agência ou operadora', 'demais']),
        'tem_agencia': niveis(np.where(base['agent'].notna(), 'com agência', 'sem agência'),
                              ['com agência', 'sem agência']),
        'paga_empresa': niveis(np.where(base['company'].notna(), 'paga por empresa', 'sem empresa'),
                               ['sem empresa', 'paga por empresa']),
        'temporada': niveis(temporada, ['média', 'baixa', 'alta']),
        # formas testadas no 05_modelo, seção 4
        'temporada_alta': niveis(np.where(mes.isin(['July', 'August']), 'alta', 'resto do ano'),
                                 ['resto do ano', 'alta']),
        'segmento3': niveis(base['market_segment'].map({'Online TA': 'agência online', 'Groups': 'grupos'})
                            .fillna('demais'), ['agência online', 'grupos', 'demais']),
        'online_ate8': sim_nao((base['market_segment'] == 'Online TA') & (base['lead_time'] <= 8)),
    }, index=base.index)
    return pd.concat([base[['is_canceled', 'arrival_date_year']], variaveis], axis=1)


def resumir_variaveis(variaveis, periodo='arrival_date_year', y='is_canceled'):
    """Uma linha por nível de cada variável de SITUACAO_VARIAVEIS: situação, se é a
    referência, reservas, % da base, taxa de cancelamento e taxa em cada período.

    Parâmetros
    ----------
    variaveis : DataFrame
        Saída de `montar_variaveis`.

    Retorna
    -------
    DataFrame indexado por variável e nível.
    """
    partes = {}
    for nome, situacao in SITUACAO_VARIAVEIS.items():
        tabela = taxa_por_nivel(variaveis, nome, y=y)[['n', 'pct_base', 'taxa']]
        por_periodo = variaveis.groupby([nome, periodo], observed=True)[y].mean().unstack()
        for p in por_periodo.columns:
            tabela[f'taxa_{p}'] = por_periodo[p]
        tabela.insert(0, 'referencia', np.where(tabela.index == variaveis[nome].cat.categories[0], 'sim', ''))
        tabela.insert(0, 'situacao', situacao)
        partes[nome] = tabela
    return pd.concat(partes, names=['variavel', 'nivel'])


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


# -----------------------------------------------------------------------------
# Variáveis em conjunto
# -----------------------------------------------------------------------------
def ajustar_logistica(formula, base):
    """Regressão logística (GLM binomial do statsmodels) e o BIC no padrão do projeto:
    −2·log-verossimilhança + (coeficientes + intercepto)·ln(n)."""
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    modelo = smf.glm(formula, data=base, family=sm.families.Binomial()).fit()
    modelo.bic_projeto = -2 * modelo.llf + (modelo.df_model + 1) * np.log(modelo.nobs)
    return modelo


def stepwise(base, candidatas, y='is_canceled', criterio='bic'):
    """Seleção stepwise (nos dois sentidos) de variáveis para a regressão logística.

    Começa sem nenhuma variável. A cada passo:
    1. tenta pôr cada candidata que está fora e fica com a que mais reduz o critério;
       se nenhuma reduz, para;
    2. depois de cada entrada, tenta tirar cada variável que está dentro; enquanto
       alguma saída reduzir o critério, tira a que mais reduz.
    Cada variável entra ou sai inteira (todas as dummies de uma categórica juntas), e
    todos os modelos usam as mesmas linhas, para os critérios serem comparáveis. Um
    conjunto de variáveis já visitado não é visitado de novo, o que evita ciclos.

    Parâmetros
    ----------
    base : DataFrame
        Sem vazios nas colunas usadas.
    candidatas : list de str
    y : str
    criterio : 'bic' ou 'aic'
        BIC no padrão do projeto (−2·log-verossimilhança + (coeficientes + 1)·ln n).

    Retorna
    -------
    finais : list
        Variáveis do modelo escolhido, na ordem em que entraram.
    historico : DataFrame
        Um passo por linha: a ação (entra ou sai), a variável, o critério depois do
        passo e quanto ele caiu.
    """
    def valor(variaveis):
        formula = f"{y} ~ {' + '.join(variaveis) if variaveis else '1'}"
        m = ajustar_logistica(formula, base)
        return m.bic_projeto if criterio == 'bic' else m.aic

    atuais = []
    atual = valor(atuais)
    visitados = {frozenset()}
    historico = [{'passo': 0, 'acao': 'início', 'variavel': '', criterio: atual, 'queda': np.nan}]

    def registrar(acao, variavel, novo):
        historico.append({'passo': len(historico), 'acao': acao, 'variavel': variavel,
                          criterio: novo, 'queda': atual - novo})

    while True:
        opcoes = {v: valor(atuais + [v]) for v in candidatas
                  if v not in atuais and frozenset(atuais + [v]) not in visitados}
        if not opcoes:
            break
        v, novo = min(opcoes.items(), key=lambda par: par[1])
        if novo >= atual:
            break
        registrar('entra', v, novo)
        atuais, atual = atuais + [v], novo
        visitados.add(frozenset(atuais))
        while len(atuais) > 1:
            saidas = {v: valor([a for a in atuais if a != v]) for v in atuais
                      if frozenset(a for a in atuais if a != v) not in visitados}
            if not saidas:
                break
            v, novo = min(saidas.items(), key=lambda par: par[1])
            if novo >= atual:
                break
            registrar('sai', v, novo)
            atuais, atual = [a for a in atuais if a != v], novo
            visitados.add(frozenset(atuais))
    return atuais, pd.DataFrame(historico).set_index('passo')


def stepwise_com_sinais(base, candidatas, y='is_canceled', criterio='bic', periodo='arrival_date_year'):
    """Stepwise repetido até todos os sinais valerem nos períodos.

    Roda o `stepwise`; se algum coeficiente do modelo escolhido tem sinais diferentes
    nos ajustes de cada período (`coeficientes_por_periodo`), sai a variável desse
    coeficiente (a de menor queda no critério, se houver mais de uma) e o stepwise roda
    de novo sem ela. Para quando nenhum sinal inverte.

    Retorna
    -------
    finais : list
    historico : DataFrame
        Os passos do último stepwise.
    rodadas : DataFrame
        Uma linha por variável retirada: a rodada, a variável, o coeficiente que
        inverteu e o valor dele em cada período.
    """
    candidatas = list(candidatas)
    rodadas = []
    while True:
        finais, historico = stepwise(base, candidatas, y=y, criterio=criterio)
        sinais = coeficientes_por_periodo(base, f"{y} ~ {' + '.join(finais)}", finais, periodo=periodo)
        invertem = sinais[sinais['mesmo_sinal'] == 'não']
        if invertem.empty:
            break
        dona = {t: next(v for v in finais if t == v or t.startswith(f'{v}[')) for t in invertem.index}
        queda = historico.groupby('variavel')['queda'].last()   # a última vez que a variável entrou
        sai = min(set(dona.values()), key=lambda v: queda.get(v, np.inf))
        for termo, linha in invertem.iterrows():
            if dona[termo] == sai:
                rodadas.append({'rodada': len(rodadas) + 1, 'variavel': sai, 'coeficiente': termo,
                                **linha.filter(regex=r'^(coef|p)_\d').to_dict()})
        candidatas.remove(sai)
    return finais, historico, pd.DataFrame(rodadas)


def razoes_de_chances(modelo, confianca=0.95):
    """Coeficientes de um modelo logístico como razões de chances (e^b), com intervalo.

    Razão de chances 1 = nenhuma diferença em relação à referência; 2 = o dobro da
    chance (odds) de cancelar; 0,5 = metade. Fica sem o intercepto.
    """
    ic = np.exp(modelo.conf_int(alpha=1 - confianca))
    tabela = pd.DataFrame({'coef': modelo.params, 'razao_chances': np.exp(modelo.params),
                           'ic_inf': ic[0], 'ic_sup': ic[1], 'p_valor': modelo.pvalues})
    return tabela.drop(index='Intercept', errors='ignore').rename_axis('coeficiente')


def parcela_capturada(y, pontuacao, fracao):
    """Parcela dos eventos (cancelamentos) nas reservas de maior pontuação, quando se
    contata uma fração das reservas.

    Reservas com a mesma pontuação empatam. Se o corte cai no meio de um grupo empatado,
    entra a parte proporcional dos eventos desse grupo, o que equivale a sortear quem
    entra dentro do grupo. Sem isso, o resultado dependeria da ordem das linhas.
    """
    d = pd.DataFrame({'y': np.asarray(y), 's': np.asarray(pontuacao)})
    g = d.groupby('s')['y'].agg(['size', 'sum']).sort_index(ascending=False)
    k = fracao * len(d)
    antes = g['size'].cumsum() - g['size']
    parte = (k - antes).clip(lower=0, upper=g['size']) / g['size']
    return float((parte * g['sum']).sum() / d['y'].sum())


def curva_ganho(y, pontuacoes, fracoes):
    """Parcela dos eventos encontrados por cada forma de ordenar as reservas, em cada
    fração de reservas contatadas (`parcela_capturada`).

    Parâmetros
    ----------
    y : array 0/1
    pontuacoes : dict
        {nome: pontuação de cada reserva}; maior pontuação = contatada antes.
    fracoes : list de float

    Retorna
    -------
    DataFrame com uma linha por fração e uma coluna por forma de ordenar.
    """
    return pd.DataFrame({nome: [parcela_capturada(y, s, f) for f in fracoes] for nome, s in pontuacoes.items()},
                        index=pd.Index(fracoes, name='pct_contatadas'))


def taxa_por_bloco(y, prob, passo=0.05):
    """Taxa de cancelamento de cada bloco de ligações, com as reservas ordenadas da
    maior para a menor probabilidade: o bloco de 0% a 5% das reservas, de 5% a 10%...
    Os empates entram pela parte proporcional (`parcela_capturada`). Mostra até onde
    cada ligação a mais ainda encontra mais cancelamentos que a média.

    Retorna
    -------
    DataFrame com uma linha por bloco: de, ate, taxa_bloco e cancel_acum (parcela
    acumulada dos cancelamentos encontrados até o fim do bloco).
    """
    y = np.asarray(y)
    fracoes = np.round(np.arange(0, 1 + passo / 2, passo), 10)
    acum = [parcela_capturada(y, prob, f) for f in fracoes]
    total, n = y.sum(), len(y)
    return pd.DataFrame({'de': fracoes[:-1], 'ate': fracoes[1:],
                         'taxa_bloco': np.diff(acum) * total / (n * passo),
                         'cancel_acum': acum[1:]}).set_index(['de', 'ate'])


def taxa_por_faixa(y, prob, limites, limiar=None):
    """Taxa real de cancelamento em cada faixa de probabilidade prevista, da faixa mais
    alta para a mais baixa.

    As faixas vão de 0 a 1, com fronteiras em `limites`. Se houver `limiar` (o ponto de
    corte), ele vira mais uma fronteira, e as reservas com probabilidade exatamente igual
    a ele (empatadas) formam uma faixa própria, porque um limiar não as separa.

    Parâmetros
    ----------
    y : Series
        Resposta (0 ou 1).
    prob : Series
        Probabilidade prevista, no mesmo índice de `y`.
    limites : list de float
        Fronteiras internas das faixas, entre 0 e 1 (por exemplo, [0.1, 0.2, 0.4]).
    limiar : float, opcional
        Ponto de corte: liga para as reservas com probabilidade acima dele.

    Retorna
    -------
    DataFrame com uma linha por faixa: reservas, parcela (das reservas), de (onde a faixa
    começa na fila, da mais arriscada para a menos arriscada), prob_media (prevista),
    taxa (real), empate (a faixa das empatadas no limiar) e liga (faixa acima do limiar).
    """
    def num(v):
        return f'{v * 100:.1f}'.rstrip('0').rstrip('.').replace('.', ',') + '%'

    p = pd.Series(np.asarray(prob), index=y.index).round(10)
    lim = None if limiar is None else round(limiar, 10)
    fronteiras = sorted({0.0, 1.0, *limites} | ({lim} if lim is not None else set()), reverse=True)
    linhas = []
    for alto, baixo in zip(fronteiras[:-1], fronteiras[1:]):
        if alto == lim:   # a faixa logo abaixo do limiar exclui as empatadas
            dentro = (p >= baixo) & (p < alto)
        elif baixo == lim:   # a faixa logo acima do limiar também exclui as empatadas
            dentro = (p > baixo) & ((p < alto) if alto < 1 else (p <= alto))
        else:
            dentro = (p >= baixo) & ((p < alto) if alto < 1 else (p <= alto))
        nome = (f'{num(baixo)} ou mais' if alto == 1 else f'menos de {num(alto)}' if baixo == 0
                else f'{num(baixo)} a {num(alto)}')
        linhas.append((nome, dentro, False, lim is not None and baixo >= lim))
        if baixo == lim:
            linhas.append((f'exatamente {num(lim)}', p == lim, True, False))
    tabela = pd.DataFrame([{'faixa': nome, 'reservas': int(dentro.sum()), 'parcela': dentro.mean(),
                            'prob_media': p[dentro].mean(), 'taxa': y[dentro].mean(),
                            'empate': empate, 'liga': liga} for nome, dentro, empate, liga in linhas])
    assert tabela['reservas'].sum() == len(y), 'as faixas precisam cobrir todas as reservas'
    tabela.insert(3, 'de', tabela['parcela'].cumsum() - tabela['parcela'])
    return tabela.set_index('faixa')


def grafico_faixas(tabela, media, rotulo_corte, titulo='', subtitulo=''):
    """Taxa real de cancelamento por faixa de probabilidade prevista (saída de
    `taxa_por_faixa`), da faixa mais alta (à esquerda) para a mais baixa.

    A largura de cada barra é a parcela das reservas na faixa; o eixo x é, ao mesmo
    tempo, a fila das reservas e a probabilidade. As faixas que recebem ligação ficam
    na cor principal; as outras, em cinza. A linha tracejada é a média, e a pontilhada,
    o corte (fim das faixas que recebem ligação).

    Parâmetros
    ----------
    tabela : DataFrame
        Saída de `taxa_por_faixa`, com limiar.
    media : float
        Taxa média, para a linha de referência.
    rotulo_corte : str
        Texto ao lado da linha do corte.
    """
    from matplotlib.ticker import PercentFormatter
    t = tabela.reset_index()
    centro = t['de'] + t['parcela'] / 2
    corte = t.loc[t['liga'], 'parcela'].sum()
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.bar(centro, t['taxa'], width=t['parcela'] - 0.006,
           color=[CORES['principal'] if liga else '#c8c8c8' for liga in t['liga']])
    ax.axhline(media, color=CORES['referencia'], linestyle='--', linewidth=1)
    ax.annotate(f'média: {media:.1%}'.replace('.', ','), xy=(1, media), xycoords=('axes fraction', 'data'),
                xytext=(-4, 4), textcoords='offset points', ha='right', va='bottom', fontsize=9, color='#333333')
    for x, taxa in zip(centro, t['taxa']):
        ax.annotate(f'{taxa:.1%}'.replace('.', ','), xy=(x, taxa), xytext=(0, 3), textcoords='offset points',
                    ha='center', va='bottom', fontsize=9, color='#333333')
    ax.axvline(corte, color='#333333', linestyle=':', linewidth=1)
    ax.annotate(rotulo_corte, xy=(corte, 0.97), xycoords=('data', 'axes fraction'), xytext=(8, 0),
                textcoords='offset points', ha='left', va='top', fontsize=9, color='#333333')
    # nomes das faixas: quebra de linha nas barras estreitas; as empatadas levam a marca
    rotulos = [nome.replace('exatamente ', 'exatamente\n') + '\n(empatadas)' if empate
               else nome.replace(' a ', ' a\n').replace(' ou ', ' ou\n') if parcela < 0.1 else nome
               for nome, empate, parcela in zip(t['faixa'], t['empate'], t['parcela'])]
    ax.set_xticks(centro, rotulos, fontsize=9)
    ax.tick_params(axis='x', length=0)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, t['taxa'].max() * 1.2)
    ax.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    ax.set_xlabel('probabilidade de cancelar prevista pelo modelo (largura da barra = parcela das reservas)')
    ax.set_ylabel('cancelaram de fato')
    fig.suptitle(titulo, fontsize=12, y=0.98)
    if subtitulo:
        fig.text(0.5, 0.935, subtitulo, ha='center', fontsize=10, color='#666666')
    fig.subplots_adjust(top=0.88, bottom=0.17)
    return ax


def grafico_ganho(tabela, titulo='', subtitulo='', estilos=None):
    """Curva de ganho: parcela dos eventos encontrados (eixo y) contra a parcela das
    reservas contatadas (eixo x), uma linha por coluna de `curva_ganho`, com a diagonal
    do contato ao acaso, com legenda (as linhas se encontram nas pontas).

    estilos : dict, opcional
        {coluna: dict de argumentos do plot (cor, tracejado...)}.
    """
    from matplotlib.ticker import PercentFormatter
    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.plot([0, 1], [0, 1], color=CORES['referencia'], linestyle='--', linewidth=1)
    ax.annotate('ao acaso', xy=(0.85, 0.85), xytext=(8, -4), textcoords='offset points',
                color=CORES['referencia'], fontsize=9, va='top')
    for coluna in tabela.columns:
        estilo = {'linewidth': 1.5, **(estilos or {}).get(coluna, {})}
        ax.plot(tabela.index, tabela[coluna], label=coluna, **estilo)
    ax.legend(frameon=False, loc='lower right')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.xaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    ax.yaxis.set_major_formatter(PercentFormatter(1, decimals=0))
    ax.set_xlabel('reservas contatadas, da maior para a menor pontuação')
    ax.set_ylabel('cancelamentos encontrados')
    fig.suptitle(titulo, fontsize=12, y=0.98)
    if subtitulo:
        fig.text(0.5, 0.92, subtitulo, ha='center', fontsize=10, color='#666666')
    fig.subplots_adjust(top=0.86)
    return ax


def grupos_de_risco(prob, n_grupos=10):
    """Grupos de risco pelos quantis da probabilidade prevista (1 = o de menor risco),
    cada um com cerca de 1/n_grupos das reservas. Reservas com a mesma probabilidade
    ficam no mesmo grupo; por isso, havendo muitos empates, os grupos podem ter tamanhos
    diferentes e ser menos de n_grupos."""
    return pd.qcut(np.asarray(prob), n_grupos, labels=False, duplicates='drop') + 1


def calibracao(y, prob, grupos):
    """Probabilidade média prevista e taxa real por grupo (por exemplo, grupos de risco
    ou segmentos), com a diferença em pontos percentuais (real − prevista)."""
    d = pd.DataFrame({'y': np.asarray(y), 'prob': np.asarray(prob), 'grupo': np.asarray(grupos)})
    t = d.groupby('grupo', observed=True).agg(reservas=('y', 'size'), prob_media=('prob', 'mean'), taxa_real=('y', 'mean'))
    t['dif_pp'] = (t['taxa_real'] - t['prob_media']) * 100
    return t


def hosmer_lemeshow(y, prob, n_grupos=10, fora_da_amostra=False):
    """Teste de Hosmer-Lemeshow: compara eventos previstos e observados nos grupos de
    risco (`grupos_de_risco`). H0: o modelo está calibrado. Estatística qui-quadrado
    com (número de grupos − 2) graus de liberdade na base em que o modelo foi ajustado,
    e com o número de grupos numa base nova (fora_da_amostra=True), porque ali nenhum
    parâmetro foi estimado com aqueles dados. Com dezenas de milhares de linhas,
    qualquer desvio pequeno dá p-valor baixo: a tabela de calibração diz se o desvio
    importa.

    Retorna
    -------
    dict com estatistica, gl e p_valor.
    """
    from scipy.stats import chi2
    t = calibracao(y, prob, grupos_de_risco(prob, n_grupos))
    previstos = t['prob_media'] * t['reservas']
    observados = t['taxa_real'] * t['reservas']
    estat = (((observados - previstos) ** 2) / (previstos * (1 - t['prob_media']))).sum()
    gl = len(t) if fora_da_amostra else len(t) - 2
    return {'estatistica': float(estat), 'gl': gl, 'p_valor': float(chi2.sf(estat, gl))}


def comparar_modelos(base, formulas, base_comparacao=None):
    """Compara modelos ajustados nos mesmos dados pelo AIC e pelo BIC (quanto menor, melhor).

    Parâmetros
    ----------
    base : DataFrame
    formulas : dict
        {nome do modelo: fórmula}.
    base_comparacao : str, opcional
        Nome de um dos modelos. Quando dado, a tabela traz também a diferença de AIC e
        de BIC de cada modelo para ele (negativa = melhor que ele).

    Retorna
    -------
    DataFrame ordenado pelo BIC, com n_coeficientes, AIC, BIC e as diferenças para o
    melhor modelo (dif_AIC, dif_BIC) e, se pedido, para o modelo de comparação.
    """
    linhas = []
    for nome, formula in formulas.items():
        m = ajustar_logistica(formula, base)
        linhas.append({'modelo': nome, 'n_coeficientes': int(m.df_model), 'AIC': m.aic, 'BIC': m.bic_projeto})
    tabela = pd.DataFrame(linhas).set_index('modelo').sort_values('BIC')
    tabela['dif_AIC'] = tabela['AIC'] - tabela['AIC'].min()
    tabela['dif_BIC'] = tabela['BIC'] - tabela['BIC'].min()
    colunas = ['n_coeficientes', 'AIC', 'dif_AIC', 'BIC', 'dif_BIC']
    if base_comparacao is not None:
        tabela['AIC_vs_base'] = tabela['AIC'] - tabela.loc[base_comparacao, 'AIC']
        tabela['BIC_vs_base'] = tabela['BIC'] - tabela.loc[base_comparacao, 'BIC']
        colunas += ['AIC_vs_base', 'BIC_vs_base']
    return tabela[colunas].round(1)


def gvif(base, variaveis):
    """VIF generalizado (GVIF) de cada variável, com todas juntas.

    O VIF comum mede quanto a variância de um coeficiente aumenta porque a variável é
    explicada pelas outras. Uma categórica com vários níveis tem várias dummies; o GVIF
    trata a variável inteira de uma vez (Fox e Monette, 1992):
    GVIF = det(R11) · det(R22) / det(R), em que R é a matriz de correlação das dummies,
    R11 a parte da variável e R22 a das outras. Para comparar variáveis com números
    diferentes de níveis, usa-se GVIF^(1/(2·gl)), na escala da raiz do VIF; elevado ao
    quadrado, volta à escala do VIF comum (vif_equivalente). Numa variável sim ou não,
    o GVIF é igual ao VIF comum.

    Parâmetros
    ----------
    base : DataFrame
    variaveis : list de str

    Retorna
    -------
    DataFrame ordenado do maior para o menor: gl (número de dummies), GVIF e
    vif_equivalente.
    """
    import patsy
    X = patsy.dmatrix(' + '.join(variaveis), base, return_type='dataframe').drop(columns='Intercept')
    R = np.corrcoef(X.to_numpy(), rowvar=False)
    det_R = np.linalg.det(R)
    linhas = {}
    for v in variaveis:
        dela = [i for i, c in enumerate(X.columns) if c == v or c.startswith(f'{v}[')]
        outras = [i for i in range(X.shape[1]) if i not in dela]
        valor = np.linalg.det(R[np.ix_(dela, dela)]) * np.linalg.det(R[np.ix_(outras, outras)]) / det_R
        linhas[v] = {'gl': len(dela), 'GVIF': valor, 'vif_equivalente': valor ** (1 / len(dela))}
    return pd.DataFrame(linhas).T.astype({'gl': int}).sort_values('vif_equivalente', ascending=False).rename_axis('variavel')


def coeficientes_por_periodo(base, formula, variaveis, periodo='arrival_date_year'):
    """Coeficientes de algumas variáveis no modelo ajustado no treino todo e em cada
    período separado, para conferir se o sinal se mantém.

    Parâmetros
    ----------
    base : DataFrame
    formula : str
    variaveis : list de str
        Nomes das variáveis cujos coeficientes entram na tabela (cada nível conta como
        um coeficiente, como 'diaria[T.até 59]').
    periodo : str

    Retorna
    -------
    DataFrame com uma linha por coeficiente: coef e p-valor no treino todo, o coef e
    o p-valor em cada período e mesmo_sinal (sim ou não). Um nível sem nenhuma
    reserva num período fica em branco nesse período e de fora da conferência (sem
    isso, o ajuste daria 0 para ele, e a conferência marcaria "não").
    """
    def presente(termo, dados):
        # o termo tem dados no período? (cada parte 'variavel[T.nivel]' precisa de pelo menos uma reserva)
        for parte in termo.split(':'):
            if '[T.' in parte:
                v, nivel = parte.split('[T.')
                if not (dados[v].astype(str) == nivel.rstrip(']')).any():
                    return False
        return True

    todos = ajustar_logistica(formula, base)
    termos = [t for t in todos.params.index if any(t == v or t.startswith(f'{v}[') for v in variaveis)]
    tabela = pd.DataFrame({'coef': todos.params[termos], 'p_valor': todos.pvalues[termos]})
    for p, dados in base.groupby(periodo):
        m = ajustar_logistica(formula, dados)
        com_dados = [t for t in termos if presente(t, dados)]
        tabela[f'coef_{p}'] = m.params.reindex(com_dados).reindex(termos)
        tabela[f'p_{p}'] = m.pvalues.reindex(com_dados).reindex(termos)
    sinais = np.sign(tabela.filter(like='coef_'))
    tabela['mesmo_sinal'] = np.where(sinais.nunique(axis=1) <= 1, 'sim', 'não')
    ordem = ['coef', 'p_valor'] + [c for c in tabela.columns if c.startswith('coef_')]         + [c for c in tabela.columns if c.startswith('p_') and c != 'p_valor'] + ['mesmo_sinal']
    return tabela[ordem].rename_axis('coeficiente')


def sentido_dos_efeitos(base, modelo, variaveis, y='is_canceled'):
    """Compara o sentido de cada coeficiente do modelo com o da comparação direta: a
    taxa do nível contra a taxa da referência, sem as outras variáveis.

    Um coeficiente com sentido contrário ao da comparação direta diz, por exemplo, que
    "sem agência cancela mais" quando, nos dados, sem agência cancela menos. Esse efeito
    existe só depois de descontar as outras variáveis ao mesmo tempo e não se explica
    para quem vai usar o modelo.

    Retorna
    -------
    DataFrame com uma linha por coeficiente: coef, taxa_nivel, taxa_referencia e
    mesmo_sentido (sim ou não).
    """
    linhas = {}
    for termo, coef in modelo.params.drop('Intercept').items():
        v = next(v for v in variaveis if termo.startswith(f'{v}['))
        nivel = termo.split('[T.')[1].rstrip(']')
        referencia = base[v].cat.categories[0]
        taxa_nivel = base.loc[base[v] == nivel, y].mean()
        taxa_ref = base.loc[base[v] == referencia, y].mean()
        linhas[termo] = {'coef': coef, 'taxa_nivel': taxa_nivel, 'taxa_referencia': taxa_ref,
                         'mesmo_sentido': 'sim' if np.sign(coef) == np.sign(taxa_nivel - taxa_ref) else 'não'}
    return pd.DataFrame(linhas).T.astype({'coef': float, 'taxa_nivel': float, 'taxa_referencia': float}).rename_axis('coeficiente')


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


def conferir_largura_minima(base, variavel, passos, largura):
    """Tira os cortes da árvore que criam faixas mais estreitas que `largura`.

    Uma faixa estreita demais (por exemplo, de 62 a 63 €) costuma separar uma tarifa ou um
    caso específico, e não um nível da variável. Entre os cortes que limitam faixas
    estreitas, sai o de menor ganho de informação, e a conferência se repete até todas as
    faixas terem pelo menos `largura` valores. A última faixa, aberta, não conta.

    Parâmetros
    ----------
    base : DataFrame
    variavel : str
        Coluna numérica de valores inteiros.
    passos : DataFrame
        Saída de cortes_por_ganho.
    largura : int
        Número mínimo de valores inteiros em cada faixa (por exemplo, 10 euros).

    Retorna
    -------
    passos_que_ficam : DataFrame
        As linhas de `passos` dos cortes aceitos que ficam, no formato de cortes_por_ganho
        (pode ir direto para conferir_cortes_por_periodo).
    saidas : list
        Uma frase por corte que saiu.
    """
    aceitos = passos[passos['aceito'] == 'sim']
    ganho = {int(c): g for c, g in zip(aceitos['corte_novo'], aceitos['ganho'])}
    cortes, saidas = sorted(ganho), []
    minimo = int(base[variavel].min())
    while True:
        limites = [minimo - 1] + cortes
        estreitos = {c for a, b in zip(limites[:-1], limites[1:]) if b - a < largura for c in (a, b) if c in cortes}
        if not estreitos:
            break
        sai = min(estreitos, key=ganho.get)
        saidas.append(f'O corte em {sai} cria uma faixa com menos de {largura} valores e sai.')
        cortes.remove(sai)
    return aceitos[aceitos['corte_novo'].astype(int).isin(cortes)], saidas


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
        if not cortes:
            break                                             # nenhum corte vale nos dois períodos
        rodada += 1
    tabela = pd.concat(tabelas, names=['rodada', 'faixa'])
    return cortes, tabela, saidas


def agrupar_categorias(base, coluna, periodo='arrival_date_year', min_faixa=0.005, ganho_minimo=0.0005,
                       y='is_canceled'):
    """Agrupa as categorias de uma variável com a árvore de decisão e a conferência por período.

    É o método das numéricas aplicado a uma categórica:
    1. as categorias com menos de `min_faixa` da base se juntam em "outras";
    2. as categorias são ordenadas pela taxa de y, e cada uma recebe a sua posição nessa ordem;
    3. a árvore de decisão (cortes_por_ganho) procura onde cortar essa ordem;
    4. a conferência por período (conferir_cortes_por_periodo) tira os cortes que invertem.

    Parâmetros
    ----------
    base : DataFrame
        Só os dados usados nas decisões (o treino).
    coluna : str
        Coluna categórica.
    periodo, min_faixa, ganho_minimo, y
        Como em cortes_por_ganho e conferir_cortes_por_periodo.

    Retorna
    -------
    grupo : Series
        O grupo de cada linha (os nomes das categorias do grupo, separados por vírgula).
    tabela : DataFrame
        Uma linha por categoria, na ordem da taxa: reservas, parcela da base, taxa, taxa em
        cada período e o grupo final.
    saidas : list
        Uma frase por corte que a árvore aceitou e que saiu na conferência.
    """
    import re
    contagem = base[coluna].value_counts()
    pequenas = contagem[contagem / len(base) < min_faixa].index
    categoria = base[coluna].astype(str).where(~base[coluna].isin(pequenas), 'outras')
    ordem = list(base.groupby(categoria)[y].mean().sort_values().index)
    posicao = categoria.map({c: i for i, c in enumerate(ordem)})
    dados = base.assign(_posicao=posicao)
    passos = cortes_por_ganho(dados, '_posicao', min_faixa=min_faixa, ganho_minimo=ganho_minimo, y=y)
    cortes, _, saidas_numeros = conferir_cortes_por_periodo(dados, '_posicao', passos, periodo=periodo, y=y)

    def entre(c):
        return f'entre {ordem[c]} e {ordem[c + 1]}'
    saidas = []
    for frase in saidas_numeros:
        numeros = re.findall(r'corte em (\d+)', frase)
        if numeros:
            saidas.append(f'O corte {entre(int(numeros[0]))} inverte a ordem entre os períodos e sai.')
    aceitos = [int(c) for c in passos.loc[passos['aceito'] == 'sim', 'corte_novo']]
    limites = [-1] + cortes + [len(ordem) - 1]
    nome_grupo = {}
    for a, b in zip(limites[:-1], limites[1:]):
        membros = ordem[a + 1:b + 1]
        for m in membros:
            nome_grupo[m] = ', '.join(membros)
    grupo = categoria.map(nome_grupo)

    tabela = base.groupby(categoria)[y].agg(reservas='size', taxa='mean').reindex(ordem)
    tabela.insert(1, 'pct_base', tabela['reservas'] / len(base))
    por_periodo = base.groupby([categoria, periodo])[y].mean().unstack().reindex(ordem)
    for p in por_periodo.columns:
        tabela[f'taxa_{p}'] = por_periodo[p]
    tabela['grupo'] = [nome_grupo[c] for c in ordem]
    if not aceitos:
        saidas = ['A árvore não aceitou nenhum corte.'] + saidas
    return grupo, tabela.rename_axis(coluna), saidas


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
