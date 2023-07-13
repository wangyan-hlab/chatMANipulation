from frchat.gui_rbtcmd_langchain import FRChatGUI
from frchat.bot_langchain_chatglm import GLM, FRChatBotGLM
from frchat.init_prompt_rbtcmd import MSG_RBTCMD_INTRO_LC_TEMPLATE

if __name__ == "__main__":
    
    frgui = FRChatGUI(title="Fairy指令小助手")

    modelpath = "THUDM/chatglm2-6b"
    llm = GLM()
    llm.load_model(model_name_or_path=modelpath)
    
    # frgui.bot = FRChatBotGLM(llm=llm, prompt=MSG_RBTCMD_INTRO_LC_TEMPLATE)

    from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
    empty_prompt = ChatPromptTemplate.from_messages([
                    SystemMessagePromptTemplate.from_template("你是一个聊天机器人,随便聊什么都行"),
                    MessagesPlaceholder(variable_name="history"),
                    HumanMessagePromptTemplate.from_template("{input}")
                    ])
    frgui.bot = FRChatBotGLM(llm=llm, prompt=empty_prompt)
    
    frgui.start_gui()
