from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.common.by as select;
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
import keyboard as k
from os.path import exists
from json import load
from selenium.webdriver.common.keys import Keys
import re

def voltarTelaCupons(wd: webdriver.Chrome):
    actions = ActionChains(wd)
    try:
        actions.move_to_element(wd.find_element(select.By.XPATH, "//*[@id=\"menuSuperior\"]/ul/li[4]/a")).perform()
        actions.click(wd.find_element(select.By.XPATH, "//*[@id=\"menuSuperior:submenu:12\"]/li[1]/a")).perform()
    except NoSuchElementException:
        actions.move_to_element(wd.find_element(select.By.XPATH, "//*[@id=\"ctl00_Menu_mnControl_LoginView1_menuSuperior\"]/ul/li[4]/a")).perform()
        actions.click(wd.find_element(select.By.XPATH, "//*[@id=\"ctl00_Menu_mnControl_LoginView1_menuSuperior:submenu:12\"]/li[1]/a")).perform()
    wd.find_element(select.By.XPATH, "/html/body/form/table[2]/tbody/tr/td[2]/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/table/tbody/tr/td/input[1]").click()
    select_nome = wd.find_element(select.By.XPATH, '/html/body/form/table[2]/tbody/tr/td[2]/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/table[1]/tbody/tr[1]/td[2]/select')
    sn = Select(select_nome)
    sn.select_by_index(1)
    
    select_mes = wd.find_element(select.By.XPATH, '/html/body/form/table[2]/tbody/tr/td[2]/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/table[1]/tbody/tr[2]/td[2]/select')
    sm = Select(select_mes)
    mes: str
    while True:
        comProblema = False
        i = input("Digite o mês: ")
        
        if len(i) > 2 or not i.isnumeric():
            print("Digite um mês válido")
            comProblema = True
        if len(i) == 2 and i[0] == "0":
            if int(i[1]) > 9 or int(i[1]) < 1:
                print("Digite um mês válido")
                comProblema = True
        if len(i) == 2 and i[0] != "0":
            if int(i) > 12 or int(i) < 1:
                print("Digite um mês válido")
                comProblema = True
        if len(i) < 2:
            mes = "0" + i
        else:
            mes = i
        
        if mes == "00" or mes == "0":
            print("Digite um mês válido")
            comProblema = True
        if not comProblema:
            break
    sm.select_by_value(mes)
    wd.find_element(select.By.XPATH, "/html/body/form/table[2]/tbody/tr/td[2]/div/table/tbody/tr/td[2]/table/tbody/tr[2]/td[2]/table[2]/tbody/tr/td/input").click()
    wd.find_element(select.By.XPATH, "/html/body/div[4]/div[1]/a").click()
    
def main():
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
        value = re.sub('\D', '', linhas[n])
        
        if value.isnumeric():
            if len(value) < 44:
                with open("QRErros.txt", "a") as f:
                    f.writelines("A nota: \n" + i + "\n Não pode ser cadastrada com sucesso, pois não possi 44 digitos\n"+ ("-" * 50) + "\n")
                continue
            
            try: 
                el = driver.find_element(select.By.XPATH, "/html/body/form/div[4]/div[6]/div[2]/div[2]/fieldset/div[4]/fieldset/input")
            except NoSuchElementException:
                voltarTelaCupons(driver)
                el = driver.find_element(select.By.XPATH, "/html/body/form/div[4]/div[6]/div[2]/div[2]/fieldset/div[4]/fieldset/input")
            
            el.send_keys(Keys.CONTROL + "A")
            el.send_keys(Keys.BACKSPACE)
            el.send_keys(value)
            el.send_keys(Keys.ENTER)
            
            try:
                info = driver.find_element(select.By.XPATH, "//*[@id=\"lblInfo\"]")
            except NoSuchElementException:
                info = driver.find_element(select.By.XPATH, "//*[@id=\"lblErro\"]")
                with open("QRErros.txt", "a") as f:
                    f.writelines("A nota: \n" + i + "\n Não pode ser cadastrada com sucesso e retornou o seguinte erro: \n" + info.text + "\n" + ("-" * 50) + "\n")
        else:
            with open("QRErros.txt", "a") as f:
                f.writelines("A nota \n" + i + "\n não pode ser cadastrada pois não possui um QR Code válido \n" + ("-" * 50) + "\n")

    exit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        with open("QRErros.txt", "a") as f:
            f.writelines("Ocorreu um erro inesperado: \n" + str(e) + "\n" + ("-" * 50) + "\n")
