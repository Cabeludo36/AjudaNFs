from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.common.by as select;
import keyboard as k
from os.path import exists
import os
from json import load

path = "NotasTestes.txt"
linhas:list[str]
qrCodes:list[str]
chrome_driver:str = "./chromedriver"
chrome_path:str
command: str
global config

with open("config.json", "r") as f:
    config = load(f)

chrome_path = config["CaminhoPastaGoogleChrome"]

with open(path, "r") as f:
    linhas = f.readlines()

if exists("chromedriver.exe"):
    chrome_driver = "chromedriver.exe"
elif exists("chromedriver"):
    chrome_driver = "./chromedriver"

if chrome_driver == "./chromedriver":
    command = f'bash {chrome_path}google-chrome --remote-debugging-port=8989 --user-data-dir="{os.path.dirname(__file__)}/ChromeProfile"'
elif chrome_driver == "chromedriver.exe":
    command = f'cmd /k \"{chrome_path}/google-chrome.exe --remote-debugging-port=8989 --user-data-dir=\"{os.path.dirname(__file__)}/ChromeProfile\""'
os.system(command)

while True:
    print("Pressione Ctrl e Shift quando estiver na aba de notas no navegador que abriu.")
    if k.is_pressed("Ctrl+Shift"):
        break

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:8989")
#Change chrome driver path accordingly
driver = webdriver.Chrome(options=chrome_options)

for i in linhas:
    value = i.replace("httpsÇ;;www.nfce.fazenda.sp.gov.br;qrcode:p=", '')
    value = value[:44]
    if value.isnumeric():
        driver.find_element(select.By.XPATH, "//*[@id=\"ac03504b9f4b446da5fa66dcadb8aba8\"]").send_keys(value)
        k.press("Enter")
    else:
        with open("QRErros", "a") as f:
            f.writelines(i)