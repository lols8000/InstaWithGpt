# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

#Retorna a quantidade de msg não lidas
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
