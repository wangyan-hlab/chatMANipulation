from frchat.bot_palletize import FRChatBotPalletize
from frchat.gui_palletize import FRChatGUIPalletize
from frchat.init_prompt_palletize import MSG_PALLETIZE_INTRO


if __name__ == "__main__":
    # 设置ChatBot
    messages = MSG_PALLETIZE_INTRO
    frcb = FRChatBotPalletize(messages, temperature=0.1)
    # GUI
    frgui = FRChatGUIPalletize(frcb, title="Fairy码垛小助手")
    frgui.start_gui()
