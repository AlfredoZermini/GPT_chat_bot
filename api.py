import openai

with open("/Users/alfredo/Documents/Jya/code/hidden.txt") as file:
    openai.api_key = file.read() 

def get_api_response(prompt: str) -> str | None:
    text: str | None = None

    try:
        response: dict = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.9, # the higher the more random the bot
            max_tokens=150, #minimum
            top_p=1, # alternative to temperature
            frequency_penalty=0., # reduce verbative line repetitiveness
            presence_penalty=0.6, # how often the AI is going to talk about new subjects
            stop = [' Human:', ' AI:']
        )


        choices: dict = response.get('choices')[0] # choices from the JSON, first index
        text = choices.get('text')

    except Exception as e:
        print('Error', e)

    return text


# creates message history
def update_list(message: str, pl:list[str]):
    pl.append(message)


# creates a single string
def create_prompt(message: str, pl:list[str]) -> str: #returns string
    p_message: str = f'\nHuman: {message}'
    update_list(p_message, pl)
    prompt: str = ''.join(pl)
    return prompt


# get response from bot in clean format
def get_bot_response(message: str, pl:list[str]) -> str:
    prompt: str = create_prompt(message, pl)
    bot_response: str = get_api_response(prompt)

    # check if bot_response is not None
    if bot_response:
        update_list(bot_response, pl)
        pos: int = bot_response.find('\nAI: ')
        bot_response = bot_response[pos + 5:] # everything after '\nAI: ' is the bot response

    else:
        bot_response = 'Something went wrong'

    return bot_response


# glue everything together
def main():
    # training data
    prompt_list: list[str] = ['You will pretend to be a professional AI assistant, which is expert in code generation',
                            '\nHuman: How do I do generate code which does this and this?'
                            '\nAI: See the code below:']

    while True:
        user_input: str = input('You: ')
        response: str = get_bot_response(user_input, prompt_list)
        print(f'Bot: {response}')



if __name__ == '__main__':
    main()