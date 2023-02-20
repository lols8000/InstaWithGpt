import FindMessageNotRead
import ReturnLastMessage
import AutoInstagram
import random
import OpenAI

#Inicia Automação
AutoInstagram.login()
AutoInstagram.EnterMessageInsta()

xpathMessageNotRead = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[1]/div[2]'
xpathMessages = '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div/div[2]/div/section/div/div/div/div/div[2]/div[2]/div/div[1]/div'
randonTime = random.randint(15, 25)
lastMessage = None
contador = 0

# Loop para ler as mensagens continuamente, e sempre que houver uma nova mensagem, responder.
while True:
    AutoInstagram.time.sleep(randonTime)

    if FindMessageNotRead.MessageNotRead(AutoInstagram.HtmlPage(xpathMessageNotRead)) == 0:
        contador = 1

    else:
        contador += 1

    AutoInstagram.ClickUser(contador)
    html = AutoInstagram.HtmlPage(xpathMessages)
    received_messages, sent_messages = ReturnLastMessage.extract_messages(html)
    responseGPT = OpenAI.ChatGpt(received_messages[-1])

    if lastMessage != received_messages or lastMessage is None:
        AutoInstagram.SendMessage(responseGPT)
        lastMessage = received_messages
    else:
        print('Aguardando nova mensagem!')


