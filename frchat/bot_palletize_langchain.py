import yaml
from frchat import openai_api_key
from frchat.bot_langchain import FRChatBot
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory

class FRChatBotPalletize(FRChatBot):
    """
        A ChatBot generating robot palletization programs

        Author: wangyan
        Date: 2023/07/07
    """
    
    def __init__(self, 
                 llm=ChatOpenAI(openai_api_key=openai_api_key, temperature=0), 
                 memory=ConversationBufferMemory(return_messages=True),
                 prompt=None) -> None:
        super().__init__(llm, memory, prompt)

    def read_config(self, file):
        """
            Reading palletization params from a YAML file
        """
        with open(file, "rb") as f:
            params = yaml.safe_load(f)
        
        return params
        