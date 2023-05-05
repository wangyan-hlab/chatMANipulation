# Here is a script to run a simple GUI to use the ChatBot
# Written with the help of ChatGPT

import tkinter as tk
from tkinter import filedialog
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

## Creating the GUI
# 创建主窗口
root = tk.Tk()
root.title("Fairy小助手")

# 创建输入框和输出框
font=('Comic Sans MS', 12)
frame = tk.Frame(root)
frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)
# 输入历史框
label_input = tk.Label(frame, text="输入历史:", font=font)
label_input.grid(row=0, column=0, sticky="w")
scrollbar_input_history = tk.Scrollbar(frame)
text_input_history = tk.Text(frame, height=5, 
                             yscrollcommand=scrollbar_input_history.set,
                             font=font)
text_input_history.grid(row=1, column=0, sticky="nsew")
scrollbar_input_history.config(command=text_input_history.yview)
scrollbar_input_history.grid(row=1, column=1, sticky="ns")
# 用户输入框
label_input = tk.Label(frame, text="请输入:", font=font)
label_input.grid(row=2, column=0, sticky="w")
scrollbar_input = tk.Scrollbar(frame)
text_input = tk.Text(frame, height=10, 
                     yscrollcommand=scrollbar_input.set,
                     font=font)
text_input.grid(row=3, column=0, sticky="nsew")
scrollbar_input.config(command=text_input.yview)
scrollbar_input.grid(row=3, column=1, sticky="ns")
# 输出框
label_output = tk.Label(frame, text="小助手:", font=font)
label_output.grid(row=0, column=2, sticky="w")
scrollbar_output = tk.Scrollbar(frame)
text_output = tk.Text(frame, height=15, 
                      yscrollcommand=scrollbar_output.set,
                      font=font)
text_output.grid(row=1, column=2, sticky="nsew")
scrollbar_output.config(command=text_output.yview)
scrollbar_output.grid(row=1, column=3, sticky="ns")

# 文本框适应窗口
frame.rowconfigure(1, weight=1)
frame.rowconfigure(3, weight=1)
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=0)
frame.columnconfigure(2, weight=1)
frame.columnconfigure(3, weight=0)
frame.rowconfigure(1, minsize=200)
frame.rowconfigure(3, minsize=200)

# 禁止输入历史框编辑
text_input_history.config(state="disabled")
# 禁止输出框编辑
text_output.config(state="disabled")

# 让下面的输入框在每次输入后自动滚动到底部
def on_input_change(*_):
    text_input.yview_moveto(1.0)
text_input.bind("<KeyPress>", on_input_change)

# 创建菜单栏
menubar = tk.Menu(root)
# 创建一个空菜单，用于添加文件选项
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="配置文件", menu=filemenu)

# 定义打开文件方法
def open_file():
    filename = filedialog.askopenfilename(filetypes=[("yaml files", "*.yaml")])
    if filename:
        READFILE = True
        print(f"选择的配置文件: {filename}")
        # 在这里添加你的代码，使用选择的文件进行一些操作。
        output = frcb.generate_function_list(filename)
        text_input.insert("end", str(output))

# 将 “打开” 选项添加到菜单中
filemenu.add_command(label="打开", command=open_file)

# 将单栏添加到主窗口中
root.config(menu=menubar)

# 添加时间戳到历史消息
def add_timestamp(message):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text_input_history.configure(state="normal")
    text_input_history.insert("end", f"\n{now}\n{message}\n")
    text_input_history.configure(state="disabled")
    text_input_history.see('end')

# 处理用户输入并返回消息
def process_message():
    prompt= text_input.get("end-2l linestart", "end-1c")
    # print(prompt)
    if prompt:            
        text_input.delete("end-2l linestart", "end")
        add_timestamp(prompt)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = frcb.chat(prompt)
        output_content = response
        text_output.configure(state="normal")
        text_output.insert("end", f"\n{now}\n{output_content}\n")
        text_output.configure(state="disabled")
        text_output.see('end')

# 定义发送消息的函数
def send_message(event):
    process_message()

# 绑定回车键事件，发送消息
root.bind("<Return>", send_message)

# 开始事件循环
root.mainloop()