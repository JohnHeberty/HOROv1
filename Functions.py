
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from sklearn.cluster import KMeans
from datetime import datetime
from glob import glob
import numpy as np
import cv2 as cv
import math
import time
import os

from Modulos.BROWSER.Engine import *
from Modulos.SITRAER import *
from Functions import *

# DESENVOLVIDO POR JOHN HEBERTY DE FREITAS
# E-mail: john.7heberty@gmail.com

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
def GetMagneticDeclinatioOLD(lat, lon, driver, timeout=60):
    """
    # OBTEN A DECLINAÇÃO MAGNETIVA
    
    Está função foi depreciada e so roda na versão do seleium 3.141

    Args:
        lat (_type_): _description_
        lon (_type_): _description_
        driver (_type_): _description_
        timeout (int, optional): _description_. Defaults to 60.

    Returns:
        _type_: _description_
    """
    
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
        time.sleep(1)
        driver.find_element_by_css_selector(f"[value='{Lat_Dir}']").click()
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
        time.sleep(1)
        driver.find_element_by_css_selector(f"[value='{Lon_Dir}']").click()
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
        data_find = datetime.now().strftime("%Y-%m-%d")
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '{data_find}')]"))
        )
        parent_element = element.find_element(By.XPATH, "./..")
        children_elements = parent_element.find_elements(By.XPATH, ".//*")
        Declination = children_elements[1].text.split("changing")[0].strip().upper()
        # Retornar o elemento
    except Exception as e:
        pass
       
    # RESETANDO PARA PROXIMA DECLINAÇÃO
    driver.delete_all_cookies()
    driver.refresh()
    
    Direction = Declination[-1:].strip()
    Declination = Declination[:-1].strip()
    
    graus       = 0
    minutos     = 0
    segundos    = 0
    try:    
        # Dividir a string em graus, minutos e segundos
        graus, minutos, segundos    = list(map(int, Declination.replace("°", "").replace("'", "").replace("''", "").split()))
    except Exception as e:
        try:    
            # Dividir a string em graus, minutos e segundos
            graus, minutos          = list(map(int, Declination.replace("°", "").replace("'", "").replace("''", "").split()))
        except Exception as e:
            try:    
                # Dividir a string em graus, minutos e segundos
                graus               = list(map(int, Declination.replace("°", "").replace("'", "").replace("''", "").split()))
            except Exception as e:
                pass
    
    # Converter para graus e atribundo sinal engativo se for W
    angulo_graus = round(graus + minutos / 60 + segundos / 3600, 4)
    angulo_graus = -angulo_graus if Direction == "W" else angulo_graus
    
    # ESPERA 5S SOMENTE PARA RENDERIZAR O MAPA
    time.sleep(5)
    
    return angulo_graus

# Função para obter a declinação magnética
def GetMagneticDeclination(lat, lon, driver, timeout=60):
    Declination = ''
    
    # Converte latitude e longitude para grau e minuto
    Lat_GrauMinuto, Lat_Dir, Lon_GrauMinuto, Lon_Dir = LatLon_to_GrauMinute(lat, lon)
    
    # Aguardar até que o botão seja clicável
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#declinationIGRF"))
        )
        element.click()
    except Exception as e:
        pass

    # Inserindo latitude
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#declinationLat1"))
        )
        element.clear()
        element.send_keys(Lat_GrauMinuto)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, f"[value='{Lat_Dir}']").click()
    except Exception as e:
        pass

    # Inserindo longitude
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#declinationLon1"))
        )
        element.clear()
        element.send_keys(Lon_GrauMinuto)
        time.sleep(1)
        driver.find_element(By.CSS_SELECTOR, f"[value='{Lon_Dir}']").click()
    except Exception as e:
        pass

    # Escolhendo a informação em HTML
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#declinationHTML"))
        )
        element.click()
    except Exception as e:
        pass
    
    # Solicitando o cálculo
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#calcbutton"))
        )
        element.click()
    except Exception as e:
        pass

    time.sleep(2)

    # Buscando a declinação magnética
    try:
        data_find = datetime.now().strftime("%Y-%m-%d")
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '{data_find}')]"))
        )
        parent_element = element.find_element(By.XPATH, "./..")
        children_elements = parent_element.find_elements(By.XPATH, ".//*")
        Declination = children_elements[1].text.split("changing")[0].strip().upper()
    except Exception as e:
        pass
    
    driver.delete_all_cookies()
    driver.refresh()
    
    Direction = Declination[-1:].strip()
    Declination = Declination[:-1].strip()
    
    graus = minutos = segundos = 0
    try:
        graus, minutos, segundos = list(map(int, Declination.replace("°", "").replace("'", "").replace("''", "").split()))
    except Exception:
        try:
            graus, minutos = list(map(int, Declination.replace("°", "").replace("'", "").replace("''", "").split()))
        except Exception:
            try:
                graus = int(Declination.replace("°", "").replace("'", "").replace("''", ""))
            except Exception as e:
                pass
    
    # Converte para graus
    angulo_graus = round(graus + minutos / 60 + segundos / 3600, 4)
    angulo_graus = -angulo_graus if Direction == "W" else angulo_graus
    
    time.sleep(5)
    
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
    PISTA = int(PISTA)
    if int(str(PISTA)[-1]) >= 5:
        PISTA = PISTA + (10 - int(str(PISTA)[-1]))
    else:
        PISTA = PISTA - int(str(PISTA)[-1])
    PISTA_ = ("0"*(3 - len(str(PISTA))) + f"{PISTA}")[:-1]
    CONTRARIO = PISTA - 180 if (PISTA - 180) > 0 else PISTA + 180
    CONTRARIO = int(round(CONTRARIO / 10, 0))
    return f"{PISTA_}-{CONTRARIO}"

# CRIANDO VIDEO DO RESULTADO FINAL
def CreateVideo(FolderImages, caminho_saida_video, largura=1920, altura=1080, fps=10):
    
    # Lista todas as imagens na pasta
    imagens = sorted(glob(os.path.join(f"{FolderImages}", "*jpg")), key=lambda x: int("".join([row for row in os.path.basename(x) if row.isdigit()])))
    
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