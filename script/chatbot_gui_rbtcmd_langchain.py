from frchat.gui_langchain import FRChatGUI
from frchat.init_prompt_rbtcmd import MSG_RBTCMD_INTRO_LC

if __name__ == "__main__":
    
    frgui = FRChatGUI(title="Fairy指令小助手", init_prompt=MSG_RBTCMD_INTRO_LC)
    frgui.start_gui()
