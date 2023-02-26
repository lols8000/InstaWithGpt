import FindMessageNotRead
import ReturnLastMessage
import AutoInstagram
import random
import OpenAI

#Inicia Automação
AutoInstagram.login()
AutoInstagram.EnterMessageInsta()

# Configurações do loop de checagem de novas mensagens
xpathMessageNotRead = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[1]/div[2]'
xpathMessages = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[1]/div'
lastMessage = None
contador = 1

# Loop de checagem de novas mensagens
while True:

    if FindMessageNotRead.MessageNotRead(AutoInstagram.HtmlPage(xpathMessageNotRead)):

        AutoInstagram.time.sleep(random.randint(10, 15))
        userName = FindMessageNotRead.MessageNotRead(AutoInstagram.HtmlPage(xpathMessageNotRead))[0]
        AutoInstagram.ClickUser(contador)
        html = AutoInstagram.HtmlPage(xpathMessages)
        received_messages, sent_messages = ReturnLastMessage.extract_messages(html)
        responseGPT = OpenAI.ChatGpt(received_messages[-1], userName)
        contador += 1

        if lastMessage != received_messages or lastMessage is None:
            AutoInstagram.SendMessage(responseGPT)
            lastMessage = received_messages

    else:
        print('Não há novas mensagens!')
        contador = 1
        AutoInstagram.time.sleep(5)
