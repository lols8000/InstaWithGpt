from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import GetEnv
import time

# Abre navegador e acessa o Instagram
global driver
site = "https://www.instagram.com/"
driver = webdriver.Firefox()
driver.get(site)
driver.maximize_window()

def type_like_gpt(text, xpathTextarea):
    for character in text:
        send_keys(xpathTextarea, character)
        time.sleep(0.05)

def send_keys(xpath, key):
    # Adicione um tempo de espera explícito
    #time.sleep(4)
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.XPATH, xpath))).send_keys(key)

def send_click(xpath):
    # Adicione um tempo de espera explícito
    time.sleep(4)
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.XPATH, xpath))).click()

# Efetua o login
def login():
    xpathUser = '//*[@id="loginForm"]/div/div[1]/div/label/input'
    xpathPassword = '//*[@id="loginForm"]/div/div[2]/div/label/input'
    xpathEnter = '//*[@id="loginForm"]/div/div[3]/button/div'

    send_keys(xpathUser, GetEnv.GetUsuarioInstagram())
    send_keys(xpathPassword, GetEnv.GetSenhaInstagram())
    send_click(xpathEnter)

# Acessa as mensagens do Instagram
def EnterMessageInsta():
    skipPopUp_1 = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/button'
    skipPopUp_2 = '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]'
    clickMessage = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[5]/div/a/div'

    # Ignora popups 1
    send_click(skipPopUp_1)
    # Ignora popups 2
    send_click(skipPopUp_2)
    # Clica em mensagens do Instagram
    send_click(clickMessage)

# Clica no usuário que tem mensagens não lidas
def ClickUser(cont):
    xpathUserMessage = f'/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[1]/div[2]/div/div/div/div/div[{str(cont)}]'
    send_click(xpathUserMessage)

# Envia uma mensagem
def SendMessage(message):
    xpathTextarea = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea'
    xpathSend = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]'

    # Escreve a mensagem no textarea
    type_like_gpt(message, xpathTextarea)
    # Envia a mesnagem
    send_click(xpathSend)

# Obtem as HTML completo de acordo com o xpath recebido
def HtmlPage(xpath):
    wait = WebDriverWait(driver, 20)

    # Encontre o elemento de mensagem na página
    element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    # Obtem a conversa com o usuário
    message = element.get_attribute("innerHTML")

    # Imprima a última mensagem
    return message
