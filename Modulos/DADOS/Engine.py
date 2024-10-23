from unidecode import unidecode
import pandas as pd
import numpy as np
import warnings
import pickle
import os

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

class DatasetReader:
    
    def __init__(self, 
        paths, 
        decimal_places=3, 
        m_to_knots=1.944, 
        reanalysis=False, 
        sep=";", 
        vento="VENTO", 
        direcao="DIREÇÃO",
        encoding="ISO 8859-2"
    ):
        """
        Inicializa o DatasetReader com parâmetros fornecidos.
        
        :param paths: Lista de caminhos de arquivos.
        :param decimal_places: Casas decimais para arredondamento.
        :param m_to_knots: Fator de conversão de m/s para nós.
        :param reanalysis: Se True, força a reanálise dos arquivos.
        :param save_analysis: Caminho para salvar o arquivo pickle.
        """
        self.sep = sep
        self.vento = vento
        self.encoding = encoding
        self.direcao = direcao
        self.paths = paths
        self.decimal_places = decimal_places
        self.m_to_knots = m_to_knots
        self.reanalysis = reanalysis
        self.save_analysis = os.path.join("Modulos","DADOS","TREATED")
        if not os.path.exists(self.save_analysis): os.makedirs(self.save_analysis)
        self.data_files = {}
    
    def read_datasets(self):
        """
        Lê os arquivos de dados ou carrega de um pickle existente.
        """
        path_pickle = os.path.join(self.save_analysis, 'DataFiles.pickle')

        if not os.path.exists(path_pickle) or self.reanalysis:
            for file_path in self.paths:
                self.process_file(file_path)

            if self.data_files and self.save_analysis:
                self.save_to_pickle(path_pickle)
        else:
            self.load_from_pickle(path_pickle)

        return self.data_files

    def process_file(self, file_path):
        """
        Processa um único arquivo de dados meteorológicos.
        """
        print(f"READING FILE: {file_path}")
        with open(file_path, "r", encoding=self.encoding) as file:
            text_lines = file.readlines()

        name, latitude, longitude, altitude = self.extract_metadata(text_lines)
        print("  ",name, latitude, longitude, altitude)
        dataset = self.create_dataframe(text_lines)
        dataset = self.clean_data(dataset)
        dataset = self.transform_wind_speed(dataset)
        try:
            dataset.columns = ["DATA", self.direcao, self.vento]
        except ValueError as e:
            colunas = str(dataset.columns.values)
            raise ValueError(f"Error: Mais ou menos de uma coluna como resultado final para vento ou direção. Colunas Dataset: {colunas}. Esperado: 3 colunas ['DATA', '{self.direcao}', '{self.vento}']. Erro original: {str(e)}")        
        self.data_files[name] = {
            "Local": (eval(latitude), eval(longitude)),
            "Altitude": altitude,
            "Dataset": dataset,
            "File Name": os.path.basename(file_path),
            "Path File": file_path
        }

    def extract_metadata(self, text_lines):
        """
        Extrai metadados do arquivo.
        """
        name = self.extract_value(text_lines,       "ESTACAO:",     self.sep)
        latitude = self.extract_value(text_lines,   "LATITUDE:",    self.sep)
        longitude = self.extract_value(text_lines,  "LONGITUDE:",   self.sep)
        altitude = self.extract_value(text_lines,   "ALTITUDE:",    self.sep)
        return name, latitude, longitude, altitude

    @staticmethod
    def extract_value(text_lines, label, sep=";"):
        """
        Extrai valores com base no rótulo.
        """
        for text_line in text_lines:
            text_line = unidecode(text_line.strip()).upper().replace(sep, " ").replace("  ", " ").replace("  ", " ").replace(",", ".")
            if label in text_line: break
        lines = [item.strip() for item in text_line.strip().split(label) if item != ""]
        return lines[-1] if len(lines) > 0 else "NÃO LOCALIZADO"

    def create_dataframe(self, text_lines):
        """
        Cria um DataFrame a partir do conteúdo do arquivo.
        """
        for n, line in enumerate(text_lines): 
            if self.sep in line and len(pd.Series([row for row in line.split(self.sep) if row.strip() != ""]).unique()) > 2: break
        title       = [unidecode(row. strip()).replace("  ", " ").replace(",", ".") for row in text_lines[n].split(self.sep)]
        data        = [unidecode(line.strip()).replace("  ", " ").replace(",", ".").split(self.sep) for line in text_lines[n+1:] if line.strip() != ""]
        df          = pd.DataFrame(data, columns=title)
        df["DATA"]  = pd.to_datetime(self.format_dates(df))
        return df[[row for row in df.columns if row.strip() != ""]]

    def format_dates(self, df, Ncol_Data="Data", Ncol_Hora="Hora"):
        """
        Formata as datas do DataFrame.
        """
        formats = [
            "%Y-%m-%d %H%M", "%d-%m-%Y %H%M", 
            "%d/%m/%Y %H%M", "%Y/%m/%d %H%M"
            "%d/%m/%Y %H:%M"
        ]
        try:
            col_Data =      [row for row in df.columns if Ncol_Data.upper().strip() in row.upper().strip()][0]
        except IndexError as e:
            raise IndexError(f"Error: Nome Data não foi localizado no bando de dados. Erro original: {str(e)}")
        try:
            col_Hora =      [row for row in df.columns if Ncol_Hora.upper().strip() in row.upper().strip()][0]
        except IndexError as e:
            raise IndexError(f"Error: Nome Hora não foi localizado no bando de dados. Erro original: {str(e)}")
        df[col_Hora] = df[col_Hora].apply(lambda x: x.replace("UTC" ,"").replace("UTM" ,"").strip())
        df[col_Hora] = df[col_Hora].apply(lambda x: x.replace("0000","00:00"))
        df[col_Hora] = df[col_Hora].apply(lambda x: x.replace("1000","10:00"))
        df[col_Hora] = df[col_Hora].apply(lambda x: x.replace("2000","20:00"))
        df[col_Hora] = df[col_Hora].apply(lambda x: x.replace("00",":00") if ":00" not in x else x)
        df["DATA"] = (df[col_Data] + " " + df[col_Hora])
        for fmt in formats:
            try:
                return pd.to_datetime(df["DATA"], format=fmt)
            except:
                pass
        return df["DATA"]

    def clean_data(self, df):
        """
        Limpa e formata o DataFrame removendo valores nulos e aplicando conversões.
        """
        columns  =   ["DATA"]
        columns +=  self.get_columns_by_keyword(df, self.direcao)
        columns +=  self.get_columns_by_keyword(df, self.vento, exclude1=self.direcao, exclude2="RAJADA")
        
        df = df[columns].copy()
        for col in columns[1:]:
            df[col] = df[col].replace(["None", "null", ""], np.nan).infer_objects(copy=False)
            df.iloc[:, df.columns.get_loc(col)] = df.iloc[:, df.columns.get_loc(col)].apply(self.convert_to_float)
        return df.reset_index(drop=True)

    def transform_wind_speed(self, df):
        """
        Converte a velocidade do vento de metros/s para nós/s.
        """
        try:
            wind_column = [row for row in df.columns if self.vento.upper().strip() in row.upper().strip()][0]
        except IndexError as e:
            raise IndexError(f"Parametro 'vento' definido como {self.vento} não localizado nos dados. Erro original: {str(e)}")
        df[wind_column] = df[wind_column].apply(lambda x: str(x).replace(",",".").strip())
        df = df[df[wind_column]!=""]
        df.reset_index(drop=True)
        df[wind_column] = df[wind_column].apply(lambda x: round(float(x) * self.m_to_knots, self.decimal_places))
        return df[df[wind_column] > 0].sort_values("DATA").reset_index(drop=True)

    @staticmethod
    def get_columns_by_keyword(df, keyword, exclude1=None, exclude2=None):
        """
        Retorna colunas que contêm a palavra-chave, excluindo as que contêm a palavra de exclusão (se fornecida).
        """
        return list(pd.Series([col for col in df.columns if keyword in col and (exclude1 is None or exclude1 not in col) and (exclude2 is None or exclude2 not in col)]).unique())

    @staticmethod
    def convert_to_float(value):
        """
        Converte valores para float, tratando exceções.
        """
        try:
            return round(float(str(value).replace(",", ".")), 3)
        except ValueError:
            return np.nan

    def save_to_pickle(self, path_pickle):
        """
        Salva os dados no formato pickle.
        """
        with open(path_pickle, 'wb') as file:
            pickle.dump(self.data_files, file)

    def load_from_pickle(self, path_pickle):
        """
        Carrega os dados do arquivo pickle.
        """
        with open(path_pickle, 'rb') as file:
            self.data_files = pickle.load(file)
    