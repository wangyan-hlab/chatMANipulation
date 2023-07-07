import yaml
from frchat import openai_api_key
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory


class FRChatBot(object):

    def __init__(self, 
                 llm=ChatOpenAI(openai_api_key=openai_api_key, temperature=0), 
                 memory=ConversationBufferMemory(return_messages=True),
                 prompt=None) -> None:
        
        self.llm = llm
        self.memory = memory
        self.conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)

    
    def chat(self, input):
        """
            Chatting with the bot
        """
        print(f"USER:{input}\n----------\n")
        completion = self.conversation.predict(input=input)
        print(f"FR:{completion}\n==========\n")

        return completion

    
    def read_config(self, file):
        """
            Reading functions from a YAML file
        """
        with open(file, "rb") as f:
            functions = yaml.safe_load(f)
        def read_function(func):
            func_name = func['name']
            args = ", ".join(arg['name'] for arg in func['arguments'])
            desc = func['description']
            arg_desc = ", ".join(f"{arg['name']}:{arg['description']}({arg['type']}型变量)" for arg in func['arguments'])
            ret = func['return']
            return [f"{func_name}", f"功能:'{desc}'", f"参数:'{arg_desc}'", f"返回值:'{ret}'"]
        output = [read_function(func['function']) for func in functions]
        return output
    

if __name__ == "__main__":

    context = ChatPromptTemplate.from_messages([
                SystemMessagePromptTemplate.from_template(
                    "你是一个机器人用户助手,帮助用户控制一个6关节机器人运动"
                    "你需要组合使用一些函数来完成特定任务,只使用用户提供的函数"
                    "不要自行引入其他第三方库(如RoboDK)"
                    "假设已使用如下代码实例化对象:"
                    "```"
                    "from fr_python_sdk.frrpc import RPC"
                    "robot = RPC('192.168.58.2')"
                    "```"
                    "用户提供的函数均为对象的方法.请在输出程序时加上机器人实例化部分的指令"
                    "REMEMBER:最终生成的代码都需要是可执行的函数，并返回函数名称,"
                    "最终返回一个可执行的main函数"
                ),
                MessagesPlaceholder(variable_name="history"),
                HumanMessagePromptTemplate.from_template("{input}")
    ])

    llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0)
    memory = ConversationBufferMemory(return_messages=True)
    chatbot = FRChatBot(llm, memory, context)

    completion = chatbot.chat(input="你好!")
