from frchat.bot import FRChatBot
from frchat.gui import FRChatGUI
from frchat.init_prompt_rbtcmd import MSG_RBTCMD_INTRO


if __name__ == "__main__":
    # 设置ChatBot
    messages = MSG_RBTCMD_INTRO
    frcb = FRChatBot(messages, temperature=0.1)
    # GUI
    frgui = FRChatGUI(frcb, title="Fairy指令小助手")
    frgui.start_gui()
