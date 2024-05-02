from selenium import webdriver
import os

timeout = 60
Driver = None

def OpenBrowser(url="https://www.google.com.br"):
    global Driver

    # PAHTS
    path_browserdriver = "Modulos\\BROWSER\\chrome-win\\"
    path_browser_exe = os.path.join(os.getcwd(), path_browserdriver, "chrome.exe")
    path_driver = os.path.join(os.getcwd(), path_browserdriver, "chromedriver.exe")

    # OPÇÕES PARA ABRIR NO CHROMIUM SEM CABEÇA
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    chrome_options.binary_location = path_browser_exe

    # ABRINDO O NAVEGADOR
    driver = webdriver.Chrome(path_driver, options=chrome_options)
    driver.set_page_load_timeout(timeout*5)
    driver.get(url)
    
    return driver
