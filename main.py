from pyautogui import click, write
import pyperclip as pc
from mouse import get_position
import keyboard as k
from time import sleep
from json import load
from os.path import exists

path = "NotasTestes.txt"
configPath ="config.json"
qrCodes:list[str]
mousePos:tuple

def getPos():
    global mousePos 
    mousePos = get_position()
    

print(get_position())
with open(path, "r") as f:
    qrCodes = f.read().replace("httpsÇ;;www.nfce.fazenda.sp.gov.br;qrcode:p=", '').split('\n')

if not exists(configPath):
    print("Pressione Ctrl + Shift, para marcar o local")
    while True:
        if k.is_pressed("Ctrl+Shift"):
            break
    with open("config.json", "a") as f:
        f.write("{")
        f.write("\"NFPositionX\": " + str(mousePos[0]) + ",")
        f.write("\"NFPositionY\": " + str(mousePos[1]) + "")
        f.write("}")
    pass #TODO criar tratamento para configurações, deve dar opção ao usuario de criar configurações
    
with open(configPath, "r") as f:
    content = load(f)


for i in qrCodes:
    if not not i:
        click(content["NFPositionX"],content["NFPositionY"])
        write(i)
        k.press("Enter")
        sleep(1.5)