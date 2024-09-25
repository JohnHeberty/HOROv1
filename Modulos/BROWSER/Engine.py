from selenium import webdriver
import zipfile
import shutil
import os

class Browser():

    def __init__(self) -> None:
        self.BaseUrl =   "https://www.google.com.br"
        self.Driver = None
        self.timeout = 60
        self.path_browserdriver = os.path.join("Modulos","BROWSER","chrome-win")
        if self.CleanChome(): print(" BROWSER AMTIGO LIMPO COM SUCESSO!")
        if self.ExtractZip(): print(" BROWSER EXTRAIDO COM SUCESSO!")
    
    def CleanChome(self) -> bool:
        if not os.path.exists(self.path_browserdriver):
            try:
                shutil.rmtree(self.path_browserdriver)
            except Exception as e:
                print(f" NÃO FOI POSSIVEL DELETAR O BROWSER ANTIGO. - {e}")
        return not os.path.exists(self.path_browserdriver)
    
    def ExtractZip(self) -> str:
        zip_path = f"{self.path_browserdriver}.zip"
        extract_to = self.path_browserdriver.replace(os.path.basename(self.path_browserdriver),"")
        if not os.path.exists(extract_to): os.makedirs(extract_to)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref: zip_ref.extractall(extract_to)
        return os.path.exists(self.path_browserdriver)
    
    def OpenBrowser(self) -> webdriver.Chrome:

        # PAHTS
        path_browser_exe = os.path.join(os.getcwd(), self.path_browserdriver, "chrome.exe")
        path_driver = os.path.join(os.getcwd(), self.path_browserdriver, "chromedriver.exe")

        # OPÇÕES PARA ABRIR NO CHROMIUM SEM CABEÇA
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        chrome_options.binary_location = path_browser_exe

        # ABRINDO O NAVEGADOR
        self.driver = webdriver.Chrome(path_driver, options=chrome_options)
        self.driver.set_page_load_timeout(self.timeout*5)
        self.driver.get(self.BaseUrl)
        
        return self.driver
    