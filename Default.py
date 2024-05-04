from glob import glob
import cv2 as cv
import os

# DESENVOLVIDO POR JOHN HEBERTY DE FREITAS
# E-mail: john.7heberty@gmail.com

Url_MagneticDeclination = "https://ngdc.noaa.gov/geomag/calculators/magcalc.shtml"
DirectionName           = "DIRECAO"                 # NOME COMUM ENTRE OS BANCOS PARA O RUMO DO VENTO
WindName                = "VENTO"                   # NOME COMUM ENTRE OS BANCOS PARA O VENTO
DecimalPlaces           = 3                         # ARREDONDADMENTO EM 3 CASAS DESCIMAIS
RoseWind                = 16                        # QUANTIDADE DE BARRAS QUE RODA DOS VENTOS TERA
LIMITES                 = [3,   13, 20, 25, 40]     # Limites para a Rosas dos Ventos Segundo RBAC154 P/ RUNWAY >= 1500m
WindRunwayLimite        = 20                        # VENTOS MENORES QUE ESTE VALOR SERÁ VENTOS DENTRO DA PISTA, CASO SEJA MAIOR E VENTO DE TRAVEZ - COM BASE NA RBAC154
SectorNames             = {                         # Nome dos Possiveis Nomes para setores padrões
     4: ['N', 'W', 'S', 'E'],
     8: ['N', 'NW', 'W', 'SW', 'S', 'SE', 'E', 'NE'],
    16: ['N', 'NNW', 'NW', 'WNW', 'W', 'WSW', 'SW', 'SSW', 'S', 'SSE', 'SE', 'ESE', 'E', 'ENE', 'NE', 'NNE']
}

# VARIAVEIS PARA OTIMIZAÇÃO DE PISTA
Width_IMG               = 1920#3840                 # LARGURA DA IMAGEM QUE SERA CRIADA A SIMULAÇÃO
Height_IMG              = 1080#2160                 # ALTURA DA IMAGEM QUE SERA CRIADA A SIMULAÇÃO
FonteThickness          = 1                         # ESPESSURA DA FONTE DENTRO DA IMAGEM
FonteSize               = 0.90                      # TAMANHO DA FONTE DENTRO DA IMAGEM
StartLegendRight        = Width_IMG - 510           # ONDE COMEÇA A ESCREVER A LEGENDA NA PARTE DIRETA
StartLegendLeft         = 40                        # ONDE COMEÇA A ESCREVER A LEGENDA NA PARTE ESQUERDA
HeightEspaceLegend      = 40                        # ESPAÇO ENTRE AS LEGENDAS
Fonte                   = cv.FONT_HERSHEY_SIMPLEX   # FONTE A SER USADA NA SIMULAÇÃO
MakeVideo               = True                      # SE ATIVADO IRÁ PRODUZIR UM VIDEO NO FINAL


# PATHS - NÃO MODIFIQUE CAUSARÁ ERROS
FolderImages           = os.path.join(os.getcwd(), "Movies", "IMGS")
caminho_saida_video     = os.path.join(os.getcwd(), "Movies", "{}", "RunwayOrientation-{}.mp4")
WeatherStationsPath     = glob(os.path.join("INPUT", "*.csv"))          # ARQUIVOS PARA ANALISE
WeatherStationsPath_OK  = os.path.join("Modulos", "DADOS", "TREATED")   # ARQUIVOS JÁ TRATADOS