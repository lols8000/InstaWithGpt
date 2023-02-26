import GetEnv
import openai
import re
import emoji
import os
from textblob import TextBlob

def ChatGpt(prompt, userName):

    openai.api_key = GetEnv.GetApiKey()

    model = "text-davinci-002"

    if not os.path.exists(f"{userName}.txt"):
        with open("settings\MessageHistory\padrao.txt", "r", encoding='utf-8') as file:
            text = file.read()
    else:
        with open(f"settings\MessageHistory\{userName}.txt", "r", encoding='utf-8') as file:
            text = file.read()

    max_input_length = 1024

    parts = [text[i:i + max_input_length] for i in range(0, len(text), max_input_length)]

    # Encontra a pessoa que você deseja imitar na conversa
    person_to_imitate = "Marcos Vinicius"
    imitation_context = ""

    for part in parts:
        # Divide a parte em mensagens individuais
        messages = re.findall(r"\n(.+?): (.+)", part)

        for name, message in messages:
            # Se a mensagem for da pessoa que você deseja imitar, armazena a mensagem no contexto de imitação
            if name == person_to_imitate:
                imitation_context += "\n" + message

    # Define a conversa como o contexto inicial para a conversa com o GPT-3
    context = parts[0]

    for part in parts[1:]:
        while True:
            # Obtém a entrada do usuário
            input_text = prompt

            # Verifica se a entrada contém palavras ou frases inapropriadas
            inappropriate_phrases = ["palavra1", "frase2", "termo3"]
            if any(phrase in input_text.lower() for phrase in inappropriate_phrases):
                print("Por favor, não use linguagem inapropriada.")
                continue

            # Analisa o sentimento da entrada do usuário
            sentiment = TextBlob(input_text).sentiment.polarity
            if sentiment < -0.5:
                print("Por favor, evite mensagens ofensivas ou negativas.")
                continue

            input_text = re.sub(r'(\s|^)([a-zA-Z])\.(?=\s|$)', lambda match: match.group(1) + match.group(2),
                                input_text)
            input_text = emoji.demojize(input_text)

            prompt = context + imitation_context + "\nUsuário: " + input_text + "\nModelo:"
            response = openai.Completion.create(
                engine=model,
                prompt=prompt,
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.7,
            )

            output_text = response.choices[0].text.strip()

            output_text = re.sub(r'(\s|^)([a-zA-Z])\.(?=\s|$)', lambda match: match.group(1) + match.group(2),
                                 output_text)
            output_text = emoji.emojize(output_text)

            context += "\nUsuário: " + input_text + "\nModelo:" + output_text

            if output_text.startswith(person_to_imitate + ":"):
                imitation_context += "\n" + output_text.split(":", 1)[1]

            if imitation_context:
                context += "\n" + person_to_imitate + ": " + imitation_context

            return output_text
