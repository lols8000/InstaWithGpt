import openai

def ChatGpt(prompt):

    # Adicione sua chave de API do OpenAI aqui
    openai.api_key = "API Key"

    # Defina o modelo GPT-3 a ser usado
    model_engine = "text-davinci-003"

    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    response = completions.choices[0].text
    return response
