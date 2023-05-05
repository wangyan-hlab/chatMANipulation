# Here is a script to run a simple GUI to use the ChatBot
# Written with the help of ChatGPT

import tkinter as tk
import datetime

## Setting up the ChatBot
# Importing libs
from frchat.frchatbot import FRChatBot
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv("dev.env"))  # read local .env file
# Providing a context to start a conversation
messages = [
    {'role':'system', 'content':'你是一个机器人用户助手,帮助用户控制一个6关节机器人运动,你需要组合使用一些机器人控制函数来完成特定任务,只使用用户提供的函数,不要自行引入其他第三方库(如RoboDK)'},
    {'role':'user', 'content':'你好，我们开始编写机器人控制指令吧'},
    {'role':'assistant', 'content':'好的，请告诉我能够使用哪些机器人控制函数'},
]
# Defining a ChatBot and claiming the CONFIG_DIR
frcb = FRChatBot(messages, temperature=0.1)
config_dir = "../config/fr_robot/"

## Creating the GUI
# 创建主窗口
root = tk.Tk()
root.title("聊天室")

# 创建输入框和输出框
font=('Comic Sans MS', 12)
frame = tk.Frame(root)
frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

label_input = tk.Label(frame, text="输入消息:", font=font)
label_input.grid(row=0, column=0, sticky="w")

scrollbar_input = tk.Scrollbar(frame)

text_input = tk.Text(frame, height=10, 
                     yscrollcommand=scrollbar_input.set,
                     font=font)
text_input.grid(row=1, column=0, sticky="nsew")


scrollbar_input.config(command=text_input.yview)
scrollbar_input.grid(row=1, column=1, sticky="ns")

label_output = tk.Label(frame, text="输出消息:", font=font)
label_output.grid(row=0, column=2, sticky="w")

scrollbar_output = tk.Scrollbar(frame)

text_output = tk.Text(frame, height=10, 
                      yscrollcommand=scrollbar_output.set,
                      font=font)
text_output.grid(row=1, column=2, sticky="nsew")

scrollbar_output.config(command=text_output.yview)
scrollbar_output.grid(row=1, column=3, sticky="ns")

frame.rowconfigure(1, weight=1)
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=0)
frame.columnconfigure(2, weight=1)
frame.columnconfigure(3, weight=0)

# 添加时间戳到历史消息
def add_timestamp(message):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # message = text_input.get("end-2l linestart", "end-1c")
    text_input.insert("end", f"\n{now}:\n{message}\n")
    text_input.see('end')

# 处理用户输入并返回消息
def process_message():
    prompt= text_input.get("end-2l linestart", "end-1c")
    # print(prompt)
    if prompt:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = frcb.chat(prompt)
        output_content = response
        text_output.insert("end", f"\n{now}:\n{output_content}\n")
        text_output.see('end')
        text_input.delete("end-2l linestart", "end")
        add_timestamp(prompt)
        

# 定义发送消息的函数
def send_message(event):
    process_message()

# 绑定回车键事件，发送消息
root.bind("<Return>", send_message)


# 让文本框自动适应窗口大小
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

text_input.grid(sticky="nsew")
text_output.grid(sticky="nsew")

# 开始事件循环
root.mainloop()