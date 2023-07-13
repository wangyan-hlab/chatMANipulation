# TODO:NOT GOOD ENOUGH
import yaml
from frchat.bot_rbtcmd_langchain import FRChatBot
from langchain import LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain.llms.base import LLM
from langchain.memory import ConversationBufferMemory
from transformers import AutoTokenizer, AutoModel, AutoConfig, AutoModelForCausalLM
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from torch.mps import empty_cache
import torch


class GLM(LLM):
    max_token: int = 100000
    temperature: float = 0.1
    top_p = 0.9
    tokenizer: object = None
    model: object = None
    history_len: int = 4096
    
    def __init__(self):
        super().__init__()
        
    @property
    def _llm_type(self) -> str:
        return "GLM"
            
    def load_model(self, llm_device="gpu",model_name_or_path=None):
        model_config = AutoConfig.from_pretrained(model_name_or_path, trust_remote_code=True)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path,trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_name_or_path, config=model_config, trust_remote_code=True).half().cuda()

    def _call(self,prompt:str,history:List[str] = [],stop: Optional[List[str]] = None):
        response, _ = self.model.chat(
                        self.tokenizer,prompt,
                        history=history[-self.history_len:] if len(history) > self.history_len else history,
                        max_length=self.max_token,temperature=self.temperature,
                        top_p=self.top_p)
        return response


class FRChatBotGLM(FRChatBot):

    def __init__(self,
                 llm=None,
                 memory=ConversationBufferMemory(human_prefix="question", ai_prefix="answer", return_messages=True),
                 prompt=None) -> None:
        self.llm = llm
        self.memory = memory
        self.conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)
    

if __name__ == "__main__":

    modelpath = "THUDM/chatglm2-6b"

    llm = GLM()
    llm.load_model(model_name_or_path=modelpath)

    from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    )

    template = "你是一个翻译助手,能把 {input_language} 翻译成 {output_language}."
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    chain = LLMChain(llm=llm, prompt=chat_prompt)
    result = chain.run(input_language="中文", output_language="英语", text="请翻译这句话: 我觉得你的观点很有启发性")

    print(result)