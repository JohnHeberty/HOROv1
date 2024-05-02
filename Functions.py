
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import matplotlib.ticker as tkr
from Rdita_Atrs_2024 import *               # DESENVOLVIDO POR JOHN HEBERTY DE FREITAS - FUNÇÕES AUXILIARES
from glob import glob
import numpy as np
import os
from requests import get
import numpy as np
from sklearn.cluster import KMeans
import numpy as np
import cv2 as cv
import math

from Modulos.BROWSER.Engine import *
from Functions import *
from Script1 import *

# FUNÇÃO PARA CONVERTER COORDENADAS DECIMAL PARA GRAU MINUTOS
def LatLon_to_GrauMinute(latitude, longitude):
    
    def decimal_para_dms(coordenada):
        graus = int(coordenada)
        minutos_flutuantes = (coordenada - graus) * 60
        minutos = int(minutos_flutuantes)
        segundos = round((minutos_flutuantes - minutos) * 60, 1)
        return graus, minutos, segundos
    
    lat_dir = 'N' if latitude >= 0 else 'S'
    lon_dir = 'E' if longitude >= 0 else 'W'
    lat_dms = decimal_para_dms(abs(latitude))
    lon_dms = decimal_para_dms(abs(longitude))
    LatEnd = f"{lat_dms[0]}° {lat_dms[1]}' {lat_dms[2]}''"
    LonEnd = f"{lon_dms[0]}° {lon_dms[1]}' {lon_dms[2]}''"
    return LatEnd, lat_dir, LonEnd, lon_dir

# PRECISA DO NAVEGADOR PARA OBTER A DECLINAÇÃO
def GetMagneticDeclination(lat, lon, driver, timeout=10):
    Declination = ''
    
    # EFETUANDO O CALCULO DA DECLINAÇÃO MAGNETICA
    Lat_GrauMinuto, Lat_Dir, Lon_GrauMinuto, Lon_Dir = LatLon_to_GrauMinute(lat, lon)
    
    # ROTINA PARA OBTER A DECLINAÇÃO
    # Aguardar até que o botão seja clicável
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#declinationIGRF"))
        )
        # Clicar no botão
        element.click()
    except Exception as e:
        pass

    # INSERINDO A DECLINAÇÃO LATITUDE
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#declinationLat1"))
        )
        # Clicar no botão
        element.clear()
        element.send_keys(Lat_GrauMinuto)
        driver.find_elements_by_css_selector(f"[value='{Lat_Dir}']").click()
    except Exception as e:
        pass

    # INSERINDO A DECLINAÇÃO LATITUDE
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#declinationLon1"))
        )
        # Clicar no botão
        element.clear()
        element.send_keys(Lon_GrauMinuto)
        driver.find_elements_by_css_selector(f"[value='{Lon_Dir}']").click()
    except Exception as e:
        pass

    # ESCOLHENDO A INFORMAÇÃO EM HTML
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#declinationHTML"))
        )
        # Clicar no botão
        element.click()
    except Exception as e:
        pass

    # SOLICITANDO O CALCULO
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#calcbutton"))
        )
        # Clicar no botão
        element.click()
    except Exception as e:
        pass

    time.sleep(2)

    # BUSCA A DECLINAÇÃO MAGNETICA 
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), '2024-05-02')]"))
        )
        parent_element = element.find_element(By.XPATH, "./..")
        children_elements = parent_element.find_elements(By.XPATH, ".//*")
        Declination = children_elements[1].text.split("' ")[0]
        # Retornar o elemento
    except Exception as e:
        pass
    
    # RESETANDO PARA PROXIMA DECLINAÇÃO
    driver.delete_all_cookies()
    driver.refresh()
    
    # Dividir a string em graus, minutos e segundos
    graus, minutos, segundos = map(int, Declination.replace("°", "").replace("'", "").replace("''", "").split())

    # Converter para graus
    angulo_graus = round(graus + minutos / 60 + segundos / 3600, 4)
    
    return angulo_graus

# Função para desenhar uma linha radial em qualquer ângulo
def DrawRadialLine(imagem, centro, comprimento, angulo, cor, espessura):
    # Converter o ângulo para radianos
    radiano = np.radians(-angulo-180)
    delta_x = 0
    delta_y = 0
    
    # Calcular os deltas x e y
    if angulo <= 90:
        delta_x = comprimento * np.sin(radiano)
        delta_y = comprimento * np.cos(radiano)
    elif angulo > 90 and angulo <= 180:
        delta_x = comprimento * np.sin(radiano)
        delta_y = comprimento * np.cos(radiano)
    elif angulo > 180 and angulo <= 270:
        delta_x = comprimento * np.sin(radiano)
        delta_y = comprimento * np.cos(radiano)
    elif angulo > 270 and angulo <= 360:
        delta_x = comprimento * np.sin(radiano)
        delta_y = comprimento * np.cos(radiano)
    
    # Calcular os pontos inicial e final da linha
    ponto_inicial = (int(centro[0]), int(centro[1]))
    ponto_final = (int(centro[0] + delta_x), int(centro[1] + delta_y))
    
    # Desenhar a linha
    cv.line(imagem, ponto_inicial, ponto_final, cor, espessura)

# FUNÇÃO QUE DESENHA UM SEMI CIRCULO
def DrawSemiCircle(imagem, centro, comprimento, angulo_min, angulo_max, cor, espessura):
    
    for angulo in np.arange(angulo_min, angulo_max+1):
        
        delta_x = 0
        delta_y = 0
        # Converter o ângulo para radianos
        radiano = np.radians(-angulo-180)
    
        # Calcular os deltas x e y
        if angulo <= 90:
            delta_x = comprimento * np.sin(radiano)
            delta_y = comprimento * np.cos(radiano)
        elif angulo > 90 and angulo <= 180:
            delta_x = comprimento * np.sin(radiano)
            delta_y = comprimento * np.cos(radiano)
        elif angulo > 180 and angulo <= 270:
            delta_x = comprimento * np.sin(radiano)
            delta_y = comprimento * np.cos(radiano)
        elif angulo > 270 and angulo <= 360:
            delta_x = comprimento * np.sin(radiano)
            delta_y = comprimento * np.cos(radiano)
    
        # Calcular os pontos inicial e final da linha
        # ponto_inicial = (int(centro[0]), int(centro[1]))
        ponto_final = (int(centro[0] + delta_x), int(centro[1] + delta_y))
    
        cv.circle(imagem, ponto_final, espessura, cor, -1)

# FUNÇÃO QUE DESENHA A REFERENCIA DOS DADOS
def DrawReferenceRUNWAY(imagem, centro, comprimento, angulo, cor, espessura):
    
    # Converter o ângulo para radianos
    radiano = np.radians(-angulo-180)
    
    delta_x = 0
    delta_y = 0
        
    # Calcular os deltas x e y
    if angulo <= 90:
        delta_x = comprimento * np.sin(radiano)
        delta_y = comprimento * np.cos(radiano)
    elif angulo > 90 and angulo <= 180:
        delta_x = comprimento * np.sin(radiano)
        delta_y = comprimento * np.cos(radiano)
    elif angulo > 180 and angulo <= 270:
        delta_x = comprimento * np.sin(radiano)
        delta_y = comprimento * np.cos(radiano)
    elif angulo > 270 and angulo <= 360:
        delta_x = comprimento * np.sin(radiano)
        delta_y = comprimento * np.cos(radiano)

    # Calcular os pontos inicial e final da linha
    # ponto_inicial = (int(centro[0]), int(centro[1]))
    ponto_final = (int(centro[0] + delta_x), int(centro[1] + delta_y))

    cv.circle(imagem, ponto_final, espessura, cor, -1)

# FUNÇÃO QUE AGRUPA AS AREAS DA ROSEWIND
def Agroup(contornos, clusters=5):
    # Calcule as áreas dos contornos
    areas = np.array([cv.contourArea(contorno) for contorno in contornos]).reshape(-1, 1)
    
    # Aplique o algoritmo k-means para Agroup as áreas
    kmeans = KMeans(n_clusters=clusters)
    kmeans.fit(areas)
    
    # Obtenha os rótulos dos clusters para cada área
    rotulos_clusters = kmeans.labels_
    
    # Inicialize uma lista para armazenar os contornos agrupados para cada cluster
    contornos_agrupados = [[] for _ in range(clusters)]
    
    # Agrupe os contornos de acordo com os rótulos dos clusters
    for i, rotulo in enumerate(rotulos_clusters):
        contornos_agrupados[rotulo].append(contornos[i])
    
    # Retorne os rótulos dos clusters e os contornos agrupados correspondentes
    center_grups = [int(row) for row in sorted(kmeans.cluster_centers_.reshape(1, -1)[0], key=lambda x: x, reverse=True)]
    return rotulos_clusters, contornos_agrupados, center_grups

# CRIA CORES UNIDAS EM ESCALA DE CINZA
def GenerateUniqueGrayColors(n_cores):
    # Lista para armazenar as cores
    cores = []
    # Calcular o espaçamento entre cada cor em escala de cinza
    passo = 255 // (n_cores - 1) if n_cores > 1 else 255
    # Gerar cores linearmente espaçadas em escala de cinza
    for i in range(1,n_cores+1):
        tom_de_cinza = i * passo
        cores.append((tom_de_cinza, tom_de_cinza, tom_de_cinza))
    return cores

# IDENTIFICANDO O CENTRO DA AREA
def BaricentroArea(area):
    # Converter a lista de pontos para o formato de array numpy
    area = np.array(area)
    # Calcular os momentos da área
    momentos = cv.moments(area)
    # Calcular as coordenadas x e y do baricentro
    x_baricentro = int(momentos['m10'] / momentos['m00'])
    y_baricentro = int(momentos['m01'] / momentos['m00'])
    return x_baricentro, y_baricentro

# CALCULA O AZIMUTE ENTRE 2 PONTOS            
def CalculateAzimuth(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    delta_x = x2 - x1
    delta_y = y2 - y1

    # Calcular o ângulo em radianos
    if delta_x == 0:
        if delta_y > 0:
            azimute = 90
        elif delta_y < 0:
            azimute = 270
        else:
            azimute = None  # Pontos iguais, não há azimute definido
    else:
        azimute = math.atan(delta_y / delta_x) * (180 / math.pi)
        if delta_x < 0:
            azimute += 180
        elif delta_y < 0:
            azimute += 360

    return azimute

# LIMPA TODOS OS ITENS DENTRO DA PASTA
def ClearFolder(caminho_pasta):
    # Verifique se o caminho da pasta é válido
    if not os.path.isdir(caminho_pasta):
        print(f"O caminho '{caminho_pasta}' não é uma pasta válida.")
        return

    # Lista todos os arquivos na pasta
    arquivos = os.listdir(caminho_pasta)

    # Exclua cada arquivo na pasta
    for arquivo in arquivos:
        caminho_arquivo = os.path.join(caminho_pasta, arquivo)
        try:
            os.remove(caminho_arquivo)
        except Exception as e:
            print(f"Erro ao excluir arquivo '{arquivo}': {e}")

# PRECISA INCLUIR NORTE MAGNETICO
# CRIA A ORIENTAÇÃO DE PISTA
def HeadboardRunway(PISTA):
    CONTRARIO = PISTA - 180 if (PISTA - 180) > 0 else PISTA + 180
    PISTA = int(round(PISTA / 10, 0))
    CONTRARIO = int(round(CONTRARIO / 10, 0))
    return f"{PISTA}-{CONTRARIO}"

# CRIANDO VIDEO DO RESULTADO FINAL
def CreateVideo(pasta_imagens, caminho_saida_video, largura=1280, altura=720, fps=10):
    
    # Lista todas as imagens na pasta
    imagens = sorted(glob(os.path.join(f"{pasta_imagens}", "*jpg")), key=lambda x: int(x.split(".")[0].split("\\")[-1].replace("IMG","")))

    # Define o codec de vídeo
    codec = cv.VideoWriter_fourcc(*'XVID')

    # Inicializa o objeto VideoWriter
    video_writer = cv.VideoWriter(caminho_saida_video, codec, fps, (largura, altura))

    # Itera sobre as imagens e escreve no vídeo
    for img_path in imagens:
        imagem = cv.imread(img_path)
        imagem = cv.resize(imagem, (largura, altura))
        video_writer.write(imagem)

    # Libera os recursos e fecha o vídeo
    video_writer.release()
    cv.destroyAllWindows()
