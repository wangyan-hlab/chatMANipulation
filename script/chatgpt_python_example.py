# Instead of the terminal mode, you can also try ChatGPT in a python script
# Here is an example.
#%% Importing libs
import openai
#%% Reading local .env file
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv("dev.env"))  # read local .env file
#%% Defining some helpful functions
def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0.5):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,    # this is the degree of the randomness of the response
    )
    # print(str(response.choices[0].message))
    return response.choices[0].message["content"]

def build_message(role, content):
    message = {'role':role, 'content':content}
    return message

def chat(prompt, temperature=0.5):
    messages.append(build_message('user', prompt))
    response = get_completion_from_messages(messages=messages, temperature=temperature)
    print(response)
    messages.append(build_message('assistant', response))
#%% Providing some context to start a conversation
messages = [
    {'role':'system', 'content':'You are an friendly chatting assistant'},
    {'role':'user', 'content':'Nice to meet you. My name is Yan.'},
    {'role':'assistant', 'content':'Nice to meet you. What can I do for you?'},
]
#%% Starting the conversation with a prompt
chat(prompt=f"""Yes, please remind me what my name is.""")
#%% Going ahead
chat(prompt=f"""Please split my name into single letters. Then give me a nickname based on my name.""")
#%%
prompt = f"""
    Not bad. Would you please translate my nickname into Japanese and output the katakana of it?
"""
chat(prompt)
#%%
prompt = f"""
    Cool. It sounds like 'Monster', doesn\'t it?
"""
chat(prompt)
#%%
prompt = f"""
    I see. How about writing a 7-line poem using my nickname? 
    I want you to use each letter of my nickname as the first letter of each line.
    Can you make it?
"""
chat(prompt)
#%%
prompt = f"""
    That\'s great. Would you please translate your poem into Chinese and German?
    Please output in HTML format so that I can publish it to my homepage.
    Use three keys: 'Origin', 'Chinese', and 'German' in your HTML.
"""
chat(prompt)
#%%
prompt = f"""
    Cool. Based on this, I would like to split the three languages into three columns \
    so that it is easier for others to see. 
    Would you please modify the HTML according to my request?
"""
chat(prompt)
#%%
prompt = f"""
    Cool. But it seems that you forget to add the last sentence \
    'Ready to conquer, ready to fight.' in the HTML.
    Would you please add it to the file?
"""
chat(prompt)
#%%
prompt = f"""
    That is really amazing! I also want to give the poem a title.
    Any advice?
"""
chat(prompt)
#%%
prompt = f"""
    Absolutely! 'Embracing the Day' is a excellent title.
    Please add this title to the HTML. 
"""
chat(prompt)
#%%
