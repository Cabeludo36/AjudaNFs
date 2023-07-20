from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.common.by as select;
import keyboard as k
from os.path import exists
import os
from json import load
from selenium.webdriver.common.keys import Keys

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

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:8989")
#Change chrome driver path accordingly
driver = webdriver.Chrome(options=chrome_options)

for n, i in enumerate(linhas):
    value = linhas[n].replace("httpsÇ;;www.nfce.fazenda.sp.gov.br;qrcode:p=", '').replace("httpsÃ‡;;www.nfce.fazenda.sp.gov.br;qrcode:p=", "")
    value = value[:44]
    if value.isnumeric():
        el = driver.find_element(select.By.XPATH, "/html/body/form/div[4]/div[6]/div[2]/div[2]/fieldset/div[4]/fieldset/input")
        el.send_keys(value)
        el.send_keys(Keys.ENTER)
    else:
        with open("QRErros", "a") as f:
            f.writelines(i)