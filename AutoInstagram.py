from selenium import webdriver
from bs4 import BeautifulSoup
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


def ClickUser(cont):
    # Clica no usuário que tem mensagens não lidas
    send_click(
        f'/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[1]/div[2]/div/div/div/div/div[{str(cont)}]')


def MessageNotRead(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Encontre todos os elementos `div` com o padrão de ID
    id_divs = soup.find_all('div', {'class': '_ab8w _ab94 _ab99 _ab9f _ab9m _ab9p _abcm'})

    # Crie um vetor para armazenar todos os nomes
    names = []

    # Armazene cada nome no vetor `names`
    for div in id_divs:
        name_div = div.find('div', {'class': '_aacl _aaco _aacw _aacx _aada'})
        name = name_div.text if name_div is not None else ''
        if name:
            names.append(name)

    # Retorna quantidade de mensagens não lidas
    return len(names)


# Envia uma mensagem
def SendMessage(message):
    # Escreve a mensagem no textarea
    send_keys(
        '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea', message)

    # Envia a mesnagem
    send_click(
        '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[2]/div/div/div[3]')


# Obtem as mensagens do usuário
def MessageHtml():
    wait = WebDriverWait(driver, 20)

    # Encontre o elemento de mensagem na página
    element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[1]/div')))

    # Obtem a conversa com o usuário
    message = element.get_attribute("innerHTML")

    # Imprima a última mensagem
    return message


def Message():
    wait = WebDriverWait(driver, 20)

    # Encontre o elemento de mensagem na página
    element = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[1]/div[2]')))

    # Obtem a conversa com o usuário
    HtmlElement = element.get_attribute("innerHTML")

    # Imprima a última mensagem
    return HtmlElement

login()
EnterMessageInsta()

# LastMessage = armazena a ultima mensagem e randonTime randomiza uma tempo entre 15 a 25 segundos
lastMessage = None
randonTime = random.randint(15, 25)
contador = 0

# Fica lendo as mensagens continuamente, e sempre que a pessoa envia uma msg ele responde
while True:
    time.sleep(randonTime)

    if MessageNotRead(Message()) == 0:
        print('Aguardando nova mensagem!')
        contador = 0

    else:
        contador += 1
        ClickUser(contador)
        html = MessageHtml()
        received_messages, sent_messages = ReturnLastMessage.extract_messages(html)
        responseGPT = OpenAI.ChatGpt(received_messages[-1])

        if lastMessage != received_messages or lastMessage is None:
            SendMessage(responseGPT)
            lastMessage = received_messages
        else:
            print('Aguardando nova mensagem!')
