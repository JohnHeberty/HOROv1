import pandas as pd

# CODIGO E SEU PSEUDOCODIGO
def WindTablePCT_V2(DIRECAO, MAGNETUDE, NOMESETORES, LIMITES):
    """
    ################################################
    ###################### V1 ######################
    ################################################

    (DIRECAO, MAGNETUDE, NOMESETORES, LIMITES) <- DADOS DE ENTRADA 
    
    # VARIAVEIS INICIAIS PARA O CALCULO DOS SETORES
    N                               <- armazene quantidade de SETORES_DIRECIONAIS com base em NOMESETORES
    FIM                             <- armazene 0
    INICIO                          <- armazene 360
    MEIO_SETOR                      <- calcule ( ( INICIO / N ) / 2 )
    SETORES_DIRECIONAIS             <- declare um dicionario {}
    PARA cada i dentro de range(1,N+1) FAÇA:
        INICIO                      <- calcule  INICIO - MEIO_SETOR * (1 se SE for iqual a 1 SENÃO 2)
        FIM                         <- calcule  (FIM SE i for iqual a 1 SENÃO INICIO) + MEIO_SETOR * (1 SE i for iqual a 1 SENÃO 2)
        SETORES_DIRECIONAIS[NOMESETORES[i-1]] <- armzene (inicio, FIM)
    FIM PARA
    
    # VARIAVEIS INICIAIS PARA EFETUAR OS FILTROS NOS VENTOS RESPECTIVOS SEUS LIMITES 
    DF_WIND                         <- Crie um dataframe com as colunas sendo DIRECAO e MAGNETUDE
    FILTRO_LIMITES                  <- declare um dicionario {}
    PARA cada i, lIMITE dentro de enumerate(LIMITES) FAÇA:
        SE i iqual 0:
            FILTRO_LIMITES[i]       <- filtre os valores de MAGNETUDE dentro de DF_WIND sendo menor ou iqual ao LIMITE
        CASO i iqual ao tamanho de ( LIMITES - 1 ):
            FILTRO_LIMITES[i]       <- filtre os valores de MAGNETUDE dentro de DF_WIND maior que o LIMITES[i - 1] e menor que lIMITE
            FILTRO_LIMITES[i + 1]   <- filtre os valores de MAGNETUDE dentro de DF_WIND maior que o lIMITE
        SENÃO:
            FILTRO_LIMITES[i]       <- filtre os valores de MAGNETUDE dentro de DF_WIND maior que LIMITES[i - 1] e menor ou iqual a lIMITE
    FIM PARA
    
    # CRIANDO UM DICIONARIOS COM OS RESULTADOS DOS VENTOS DENTRO DOS SETORES_DIRECIONAIS
    RESULTADOS                      <- declare um dicionario {}
    PARA cada setor, (COMECO_SETOR, FIM_SETOR) dentro das chaves de SETORES_DIRECIONAIS FAÇA:
        QUANTIDADE_VENTOS           <- declare um dicionario {}
        PARA cada Chave e Valores dentro de FILTRO_LIMITES FAÇA:
            SE COMECO_SETOR < FIM_SETOR:
                FILTRO              <- filtre a quantidade de Ventos dentro de Valores usando a DIRECAO maior ou iqual a COMECO_SETOR e menor ou iqual a FIM_SETOR  
            SE NAO:
                FILTRO1             <- filtre a quantidade de Ventos dentro de Valores usando a DIRECAO maior ou iqual a COMECO_SETOR e menor ou iqual a 360  
                FILTRO2             <- filtre a quantidade de Ventos dentro de Valores usando a DIRECAO maior ou iqual a 0 e menor ou iqual a FIM_SETOR  
                FILTRO              <- Junte os valores do FILTRO1 com o do FILTRO2
            QUANTIDADE_VENTOS       <- armazene na Chave o tamanho de FILTRO
        RESULTADOS                  <- armazene no setor os valores da QUANTIDADE_VENTOS em forma de lista
    FIM PARA
        
    # CRIANDO OS TITULOS PARA A TABELA FINAL DE VENTOS
    TITULOS = []
    PARA cada i, lIMITE dentro de enumerate( LIMITES ):
        SE i for iqual 0:
            adicione f"[0-{lIMITE}]" a lista de TITULOS
        elif i == len(LIMITES) - 1:
            adicione f"[{LIMITES[i - 1]}-{lIMITE}]" a lista de TITULOS
        else:
            adicione f"[{LIMITES[i - 1]}-{lIMITE}]" a lista de TITULOS
    FIM PARA
    adicione f"[{lIMITE}-*]" a lista de TITULOS
    
    # CRIANDO O RESULTADO FINAL DA TABELA DE VENTOS
    DF_QUANTIDADE_VENTOS            <- crie um dataframe transposto com base em RESULTADOS com seu indice sendo sendo TITULOS
    DF_VENTOS_PERCENT               <- calcule um dataframe das porcentagem usando DF_QUANTIDADE_VENTOS em que 100% e a soma de tudo
    retorne DF_VENTOS_PERCENT
    
    ################################################
    ###################### V2 ######################
    ################################################
    
    Receba os dados de direção do vento, sua magnitude, nomes dos setores e os limites de magnitude para cada setor.
    Divida o círculo de direção do vento em setores de igual tamanho.
    Para cada setor, conte a quantidade de ventos que se encaixam nos limites de magnitude especificados.
    Calcule a porcentagem de ventos para cada setor em relação ao total.
    Retorne a tabela de porcentagens de ventos por setor.
    
    """
    
    # VARIAVEIS INICIAIS PARA O CALCULO DOS SETORES
    N = len(NOMESETORES)
    FIM = 0
    INICIO = 360
    MEIO_SETOR = (INICIO / N) / 2
    SETORES_DIRECIONAIS = {}
    for i in range(1, N + 1):
        INICIO -= MEIO_SETOR * (1 if i == 1 else 2)
        FIM = (FIM if i == 1 else INICIO) + MEIO_SETOR * (1 if i == 1 else 2)
        SETORES_DIRECIONAIS[NOMESETORES[i - 1]] = (INICIO, FIM)

    # VARIAVEIS INICIAIS PARA EFETUAR OS FILTROS NOS VENTOS RESPECTIVOS SEUS LIMITES
    DF_WIND = pd.DataFrame({'DIRECAO': DIRECAO, 'MAGNETUDE': MAGNETUDE})
    FILTRO_LIMITES = {}
    for i, limite in enumerate(LIMITES):
        if i == 0:
            FILTRO_LIMITES[i] = DF_WIND[DF_WIND['MAGNETUDE'] <= limite]
        elif i == len(LIMITES) - 1:
            FILTRO_LIMITES[i] = DF_WIND[(DF_WIND['MAGNETUDE'] > LIMITES[i - 1]) & (DF_WIND['MAGNETUDE'] <= limite)]
            FILTRO_LIMITES[i + 1] = DF_WIND[DF_WIND['MAGNETUDE'] > limite]
        else:
            FILTRO_LIMITES[i] = DF_WIND[(DF_WIND['MAGNETUDE'] > LIMITES[i - 1]) & (DF_WIND['MAGNETUDE'] <= limite)]

    # CRIANDO UM DICIONARIOS COM OS RESULTADOS DOS VENTOS DENTRO DOS SETORES_DIRECIONAIS
    RESULTADOS = {}
    for setor, (comeco_setor, fim_setor) in SETORES_DIRECIONAIS.items():
        quantidade_ventos = {}
        for chave, valores in FILTRO_LIMITES.items():
            if comeco_setor < fim_setor:
                filtro = valores[(valores['DIRECAO'] >= comeco_setor) & (valores['DIRECAO'] <= fim_setor)]
            else:
                filtro1 = valores[(valores['DIRECAO'] >= comeco_setor) & (valores['DIRECAO'] <= 360)]
                filtro2 = valores[(valores['DIRECAO'] >= 0) & (valores['DIRECAO'] <= fim_setor)]
                filtro = pd.concat([filtro1, filtro2])
            quantidade_ventos[chave] = len(filtro)
        RESULTADOS[setor] = list(quantidade_ventos.values())

    # CRIANDO OS TITULOS PARA A TABELA FINAL DE VENTOS
    TITULOS = []
    for i, limite in enumerate(LIMITES):
        if i == 0:
            TITULOS.append(f"[0-{limite}]")
        elif i == len(LIMITES) - 1:
            TITULOS.append(f"[{LIMITES[i - 1]}-{limite}]")
        else:
            TITULOS.append(f"[{LIMITES[i - 1]}-{limite}]")
    TITULOS.append(f"[{limite}-*]")

    # CRIANDO O RESULTADO FINAL DA TABELA DE VENTOS
    DF_QUANTIDADE_VENTOS = pd.DataFrame(RESULTADOS, index=TITULOS).T
    DF_VENTOS_PERCENT = DF_QUANTIDADE_VENTOS / DF_QUANTIDADE_VENTOS.sum().sum() * 100

    return DF_VENTOS_PERCENT

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