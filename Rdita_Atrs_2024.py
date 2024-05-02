import pandas as pd

# CRIANDO A TABELA DE VENTOS
def WindTablePCT(tabelao, n, Direcao_nome="DIRECAO", Vento_nome="VENTO", limites=[3,   13, 20, 40], save=False, verbose=0):

    direcao             = tabelao[[column for column in tabelao.columns if Direcao_nome in column][0]]  # Graus de direção do vento 
    magnetude           = tabelao[[column for column in tabelao.columns if Vento_nome in column][0]]  # Magnitude do vento

    nomes_setores       = {
        4: ['N', 'W', 'S', 'E'],
        8: ['N', 'NW', 'W', 'SW', 'S', 'SE', 'E', 'NE'],
        16: ['N', 'NNW', 'NW', 'WNW', 'W', 'WSW', 'SW', 'SSW', 'S', 'SSE', 'SE', 'ESE', 'E', 'ENE', 'NE', 'NNE']
    }

    name_setores        = nomes_setores[n] if n in nomes_setores else []
    # SE NOME DOS SETORES FICAR VAZIO CRIE NOME NUMERICOS
    if len(name_setores) == 0: 
        name_setores = [f"D{i}" for i in range(1,n+1)]

    # OBTENDO OS ANGULOS DOS SETORES
    setores = calcular_setores(n, name_setores)

    # FILTRANDO DADOS PELOS VENTOS
    DF_WIND = tabelao[[direcao.name, magnetude.name]].copy()
    DF_WIND = DF_WIND.astype("float64")
    columns = {}
    for i in range(len(limites)):
        if i == 0:
            columns[i] = DF_WIND[DF_WIND[DF_WIND.columns[1]]<=limites[i]]
        elif i == len(limites)-1:
            columns[i] = DF_WIND[(DF_WIND[DF_WIND.columns[1]]>limites[i-1]) & (DF_WIND[DF_WIND.columns[1]]<=limites[i])]
            columns[i+1] = DF_WIND[DF_WIND[DF_WIND.columns[1]]>limites[i]]
        else:
            columns[i] = DF_WIND[(DF_WIND[DF_WIND.columns[1]]>limites[i-1]) & (DF_WIND[DF_WIND.columns[1]]<=limites[i])]

    # EFETUANDO A CLASSIFICAÇÃO DOS DADOS
    dict_result = {}
    for setor in setores:
        i, j = setores[setor]
        calc_columns = {}
        for key in list(columns):
            coluna = columns[key]
            if i < j:
                result = coluna[coluna[coluna.columns[0]] >= i]
                result = result[result[result.columns[0]] <= j]
            else:
                result1 = coluna[(coluna[coluna.columns[0]] >= i) & (coluna[coluna.columns[0]] <= 360)]
                result2 = coluna[(coluna[coluna.columns[0]] >= 0) & (coluna[coluna.columns[0]] <= j)]
                result = pd.concat([result1, result2], ignore_index=True)
            calc_columns[key] = len(result)
        dict_result[setor] = [calc_columns[row] for row in calc_columns]

    # OBTENDO OS TITULOS DOS DADOS
    titles = GetTitle(limites)

    # UNINDO TUDO EM UM DATAFRAME
    df_pct_ventos = pd.DataFrame(dict_result, index=titles).T
    df_pct_ventos = ( df_pct_ventos / df_pct_ventos.sum().sum() ) * 100
    if verbose == 1:
        print("TOTAL: ", round(df_pct_ventos.sum().sum(), 2))
    if save is True:
        df_pct_ventos.to_csv("Ventos.csv", sep=";", decimal=",", encoding="UTF-8")
    return df_pct_ventos, name_setores

# CRIANDO OS SETOES
def calcular_setores(n, name_setores):
    meio_setor = (360 / n) / 2
    inicio = 360
    fim = 0
    setores = {}
    for i in range(1,n+1):
        inicio = inicio - meio_setor * (1 if i == 1 else 2)
        fim = (fim if i == 1 else inicio) + meio_setor * (1 if i == 1 else 2)
        setores[name_setores[i-1]] = (inicio, fim)
    return setores

# CRIA O TITULO DO DATAFRAME FINAL CONFORME VARIAÇÃO DOS LIMITES
def GetTitle(limites):
    # CRIANDO O TITULO PERSONALIZAVEL
    columns_end = []
    for i in range(len(limites)):
        if i == 0:
            titulo = f"[0-{limites[i]}]"
            columns_end.append(titulo)
        elif i == len(limites)-1:
            titulo = f"[{limites[i-1]}-{limites[i]}]"
            columns_end.append(titulo)
            titulo = f"[{limites[i]}-*]"
            columns_end.append(titulo)
        else:
            titulo = f"[{limites[i-1]}-{limites[i]}]"
            columns_end.append(titulo)
    return columns_end

# CALCULANDO ANGULOS DA ROSA DOS VENTOS
def angulos_rosa(n, name_setores):
    passo = (360 / n)
    inicio = 360
    setores = {}
    for i in range(1,n+1):
        if i != 1:
            inicio = inicio - passo
        setores[name_setores[i-1]] = inicio if i == 1 else (inicio)
    return setores

# FUNÇÃO QUE ENCONTRA AS POSSIVEIS PISTAS A 180 GRAUS
def PistasPossiveis(directions):
    opposite_directions = set()
    for direction, angle in directions.items():
        opposite_angle = (angle + 180) % 360
        opposite_direction = None
        for dir, ang in directions.items():
            if ang == opposite_angle:
                opposite_direction = dir
                break
        if opposite_direction:
            opposite_directions.add(tuple(sorted([direction, opposite_direction])))
    return opposite_directions

##### METODO DESCONTINUADO

#     limite_dentro_ppd   = [3,   13, 20  ]
#     limite_fora_ppd     = [20,  25, 40  ]

# # OBTENDO OS ANGULOS DA ROSA DOS VENTOS
# dicionario_angulos = angulos_rosa(RosadosVentos, name_setores)
# directions_SUM = PistasPossiveis(dicionario_angulos)

# # OBTENDO AS COLUNAS QUE SE SOMAM PARA CALCULAR A DIREÇAO DA PISTA
# Columns_Dentro_PPD = GetTitle(limite_dentro_ppd)[:-1]
# Columns_Fora_PPD = GetTitle(limite_fora_ppd)[1:]

# # SOMANDO OS VENTOS DENTRO E FORA DA PISTA
# dict_ok_end = {}
# dict_not_ok_end = {}
# for direction in directions_SUM:
#     d1, d2 = direction
#     dict_ok_end[f"{d1}-{d2}"] = (df_pct_ventos[Columns_Dentro_PPD].loc[d1] + df_pct_ventos[Columns_Dentro_PPD].loc[d2]).sum()
#     dict_not_ok_end[f"{d1}-{d2}"] = (df_pct_ventos[Columns_Fora_PPD].loc[d1] + df_pct_ventos[Columns_Fora_PPD].loc[d2]).sum()

# # JUNTANDO TUDO EM UMA DATAFRAME
# data_dentro_fora = pd.DataFrame([dict_ok_end, dict_not_ok_end], index=["Dentro","Frota"]).reset_index(drop=False, names=["LOCAL"])
# data_dentro_fora



##### METODO DESCONTINUADO
# CRIANDO OS PERIODOS DE ANALISE - DESCONTINUADO

# Periodos        = {}
# Dias_Analise    = (365 * Tempo_Analise)
# data_start      = tabelao.DATA.min()
# data_max        = tabelao.DATA.max()
# n_periodo       = 1
# while True:
#     info = {}
#     info["START"]       = data_start
#     info["END"]         = data_start + timedelta(days=Dias_Analise)
#     data_start          = data_start + timedelta(days=(30 * Tempo_Busca))
#     Periodos[n_periodo] = info
#     n_periodo           +=1
#     if info["END"] >= data_max: break
# Periodos = pd.DataFrame(Periodos).T
# Periodos.head()