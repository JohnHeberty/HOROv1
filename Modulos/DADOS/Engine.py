import pandas as pd
import numpy as np
import pickle
import os

# FUNÇÃO PARA LER OS DADOS, NÃO HÁ DEFINIÇÃO DE UNICODE DOS DADOS DE ENNTRADA
def ReadDatasets(Paths, DecimalPlaces=3, MtoNo=1.944, reanalysis=False, SaveAnalysis=""):
    """
    MtoNo = RAZÃO DE METROS/S PARA NÓS/S
    
    """
    
    pd.set_option('future.no_silent_downcasting', True)
    
    DataFiles = {}
    
    # BASE PATH
    FileName = 'DataFiles.pickle'
    path_pickle = os.path.join(SaveAnalysis, FileName)
    
    # SE O PICKLE NÃO EXISTIR
    if os.path.exists(path_pickle) is False or reanalysis is True:
        
        # PERCORRENDO OS PATHS
        for filePath in Paths:
            print(f"READ PATH: {filePath}")
            with open(filePath,"r") as file:
                text_lines = file.readlines()
                Name = [row.strip() for row in text_lines[0].strip().split("Nome:") if row != ""][0]
                Latitude = [row.strip() for row in text_lines[2].strip().split("Latitude:") if row != ""][0]
                Longitude = [row.strip() for row in text_lines[3].strip().split("Longitude:") if row != ""][0]
                Altitude = [row.strip() for row in text_lines[4].strip().split("Altitude:") if row != ""][0]
                title = text_lines[10].strip()[:-1].split(";")
                dataset = text_lines[11:]
                dataset = [line.strip()[:-1].split(";") for line in dataset]
                dataset = [line for line in dataset if line[0] != ""]
                dataset = [{title[index]:line[index] for index in range(len(title))} for line in dataset]
                df = pd.DataFrame(dataset)
                df["DATA"] = (df[df.columns[0]] + " " + df[df.columns[1]]).apply(lambda x: str(x).strip())
                datas = []
                for data in df["DATA"].values:
                    if ":00:00" in data:
                        data = data.replace(":00:00",":00")
                    if len(data.split()[1].split(":")[0].strip())==1:
                        data = data.replace(" "," 0")
                    datas.append(data)
                df["DATA"] = datas
                formats = ["%Y-%m-%d %H%M", "%d-%m-%Y %H%M", "%d/%m/%Y %H%M", "%d/%m/%Y %H:%M"]
                for format in formats:
                    try:
                        df["DATA"] = pd.to_datetime(df["DATA"], format=format)
                    except Exception as e:
                        print(e)
                # list([row for row in df.columns if "TEMPERATURA ORVALHO MAX" in row]) + \
                # list([row for row in df.columns if "TEMPERATURA ORVALHO MIN" in row]) + \
                # list([row for row in df.columns if "PRESSAO ATMOSFERICA MAX" in row]) + \
                # list([row for row in df.columns if "PRESSAO ATMOSFERICA MIN" in row]) + \
                # columns = ["DATA"] + list([row for row in df.columns if "UMIDADE RELATIVA" in row])
                # columns = columns  + list([row for row in df.columns if "TEMPERATURA DO PONTO DE ORVALHO" in row])
                # columns = columns  + list([row for row in df.columns if "TEMPERATURA MINIMA" in row])
                # columns = columns  + list([row for row in df.columns if "TEMPERATURA MAXIMA" in row])
                # columns = columns  + list([row for row in df.columns if "BULBO SECO" in row])
                # columns = columns  + list([row for row in df.columns if "PRESSAO" in row and "ESTACAO" in row])
                # columns = columns  + list([row for row in df.columns if "PRESSAO" in row and "MAR" in row])
                columns = ["DATA"]
                DIRECAO = list([row for row in df.columns if "DIRECAO" in row])
                columns = columns  + DIRECAO
                VENTO_MAX_AUTO = list([row for row in df.columns if ("VENTO" in row and "RAJADA" in row)])
                VENTO_NORM = list([row for row in df.columns if ("VENTO" in row and "VELOCIDADE" in row and "RAJADA" not in row)])
                VENTO = (VENTO_MAX_AUTO if len(VENTO_MAX_AUTO) > 0 else VENTO_NORM)
                columns = columns + VENTO
                df = df[columns].copy()
                for column in [row for row in df.columns if "DATA" not in row]:
                    df[column] = df[column].replace(["None", "none", "null", "Null", ""], np.nan).infer_objects(copy=False)
                # DROPANDO VALORES NULOS NO VENTO E DIRECAO
                df.loc[df[VENTO + DIRECAO].dropna(axis=0).index]
                df = df.reset_index(drop=True)
                df.columns = [
                    "DATA",
                    # f"UMIDADE RELATIVA",
                    #f"TEMPERATURA DO PONTO DE ORVALHO",
                    # f"TEMPERATURA MINIMA",
                    # f"TEMPERATURA MAXIMA",
                    # f"TEMPERATURA ORVALHO MAX",
                    # f"TEMPERATURA ORVALHO MIN",
                    # f"BULBO SECO",
                    # f"PRESSAO ATMOSFERICA MAX",
                    # f"PRESSAO ATMOSFERICA MIN",
                    #f"PRESSAO AO NIVEL DA ESTACAO",
                    #f"PRESSAO AO NIVEL DO MAR",
                    f"DIRECAO",
                    f"VENTO",
                ]
                def Convert(x):
                    x = str(x).replace(",",".")
                    try:
                        return float(x)
                    except Exception as e:
                        return x
                for column in [row for row in df.columns if "DATA" not in row]:
                    df[column] = df[column].apply(lambda x: Convert(x))
                    df[column] = df[column].apply(lambda x: round(x, DecimalPlaces))
                df = df.drop_duplicates()
                # ELIMINANDO VENTOS ZERADOS
                df = df[df[df.columns[-1]]>0]
                # TRANSFORMANDO M/S PARA NÓS/S
                df[df.columns[-1]] = df[df.columns[-1]].apply(lambda x:  round(x * MtoNo, DecimalPlaces))
                df = df.sort_values(["DATA"]).reset_index(drop=True)
                DataFiles[Name] = {
                    "Local": (eval(Latitude), eval(Longitude)), 
                    "Altidude": Altitude, 
                    "Dataset": df,
                    "Name File": os.path.basename(filePath),
                    "Path File": filePath
                }

        # SE EXISTIR DADOS SALVA O PICKLE
        if DataFiles != {} and SaveAnalysis != "":
            with open(path_pickle, 'wb') as arquivo:
                pickle.dump(DataFiles, arquivo)
    
    # SE EXISTIR PEGUE DO HISTORICO
    else:
        
        # Carregar o dicionário do arquivo usando pickle
        with open(path_pickle, 'rb') as arquivo:
            DataFiles = pickle.load(arquivo)
    
    return DataFiles
