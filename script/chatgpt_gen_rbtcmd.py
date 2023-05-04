# Instead of the terminal mode, you can also try ChatGPT in a python script
# Here is an example.
#%% 
# Importing libs
import os
from frchat.frchatbot import FRChatBot
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv("dev.env"))  # read local .env file

#%% 
# Providing a context to start a conversation
messages = [
    {'role':'system', 'content':'你是一个机器人用户助手,帮助用户控制一个6关节机器人运动,你需要组合使用一些机器人控制函数来完成特定任务,只使用用户提供的函数,不要自行引入其他第三方库(如RoboDK)'},
    {'role':'user', 'content':'你好，我们开始编写机器人控制指令吧'},
    {'role':'assistant', 'content':'好的，请告诉我能够使用哪些机器人控制函数'},
]

#%% 
# Defining a ChatBot and claiming the CONFIG_DIR
frcb = FRChatBot(messages, temperature=0.1)
config_dir = os.path.join(os.path.dirname(os.path.split(__file__)[0]), "config/fr_robot/")

#%% 
# Providing some functions
file = config_dir+'robot_movement/jog.yaml'
output = frcb.generate_function_list(file)
prompt = f"""
    以下是可使用的函数:
    ```{output}```
"""
frcb.chat(prompt)

#%% 
# Describing a task
prompt = f"""
    任务1:请开始点动,1关节旋转,单次最大旋转5度,旋转到正30度,可使用循环
    请生成该任务的python指令
"""
frcb.chat(prompt)

#%% 
# Providing more functions
file = config_dir+'robot_statusinquiry.yaml'
output = frcb.generate_function_list(file)
prompt = f"""
    新增可使用的函数:
    ```{output}```
    请重写之前的指令，可使用关节角度获取函数获取关节位置
"""
frcb.chat(prompt)
#%% 
# Expanding the task
prompt = f"""
    任务2:关节配置1-[0,0,0,0,0,0],关节配置2-[30,-60,90,20,-10,30], \
    关节点动从配置1运动到配置2,请帮我生成python指令,注意不要使用用户未提供的函数
"""
frcb.chat(prompt)

# %%
