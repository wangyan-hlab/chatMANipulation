from frchat.gui_palletize_langchain import FRChatGUIPalletize

if __name__ == "__main__":
    
    frgui = FRChatGUIPalletize(width=1024, height=512, title="Fairy码垛小助手", robot_connect=True)
    frgui.start_gui()
