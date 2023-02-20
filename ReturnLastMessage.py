# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

#Extrai a conversa completa do usuário
def extract_messages(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Find all the `div` elements with class `_acd2` or `_acd3`
    sent_message_divs = soup.find_all('div', {'class': '_acd2'})
    received_message_divs = soup.find_all('div', {'class': '_ac1r _ac1w'})

    # Extract the text content of each message
    received_messages = []
    sent_messages = []
    for div in sent_message_divs:
        message_content = div.find('div', {'class': '_aacl _aaco _aacu _aacx _aad6 _aade'})
        if message_content:
            sent_messages.append(message_content.text)

    for div in received_message_divs:
        message_content = div.find('div', {'class': '_aacl _aaco _aacu _aacx _aad6 _aade'})
        if message_content:
            received_messages.append(message_content.text)

    return received_messages, sent_messages



