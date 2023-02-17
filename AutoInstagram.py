from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ReturnLastMessage
import GetEnv
import OpenAI
import time
import random

# Abre navegador e acessa o Instagram
global driver
driver = webdriver.Firefox()
driver.get("https://www.instagram.com/")
driver.maximize_window()


def send_keys(xpath, key):
    # Adicione um tempo de espera explícito
    time.sleep(4)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, xpath))).send_keys(key)


def send_click(xpath):
    # Adicione um tempo de espera explícito
    time.sleep(4)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, xpath))).click()

# Efetua o login
def login():
    send_keys('//*[@id="loginForm"]/div/div[1]/div/label/input', GetEnv.GetUsuarioInstagram())
    send_keys('//*[@id="loginForm"]/div/div[2]/div/label/input', GetEnv.GetSenhaInstagram())
    send_click('//*[@id="loginForm"]/div/div[3]/button/div')


# Acessa as mensagens do Instagram
def EnterMessageInsta():
    # Ignora popups
    send_click(
        '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/button')
    send_click(
        '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[2]')

    # Entra em mensagens do Instagram
    send_click(
        '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div[5]/div/a/div')

    # Clica na primeira caixa de mensagem
    send_click(
        '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[1]/div[2]/div/div/div/div/div[1]/div')

# Envia uma mensagem
def SendMessage(message):
    # Escreve a mensagem no textarea
    send_keys(
        '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea',
        message)

    # Envia a mesnagem
    send_click(
        '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]')


# Obtem as mensagens do primeiro contato do usuário
def MessageHtml():
    wait = WebDriverWait(driver, 20)

    # Encontre o elemento de mensagem na página
    element = wait.until(EC.presence_of_element_located((By.XPATH,
        '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[1]/div')))

    # Obtenha a última mensagem
    last_message = element.get_attribute("innerHTML")

    # Imprima a última mensagem
    return last_message

login()
EnterMessageInsta()

#LastMessage = armazena a ultima mensagem e randonTime randomiza uma tempo entre 15 a 25 segundos
lastMessage = None
randonTime = random.randint(15, 25)

#Fica lendo as mensagens continuamente, e sempre que a pessoa envia uma msg ele responde
while True:
    time.sleep(randonTime)
    html = MessageHtml()
    received_messages, sent_messages = ReturnLastMessage.extract_messages(html)
    responseGPT = OpenAI.ChatGpt(received_messages[-1])

    if lastMessage != received_messages or lastMessage is None:
        SendMessage(responseGPT)
        lastMessage = received_messages
    else:
        print('Aguardando nova mensagem!')



