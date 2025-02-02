# Initial prompt for palletization chatbot

# author: wangyan
# date: 2023/06/02

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)

WELCOME_TEXT = "=== WELCOME ===\n\n  您好!我是FR码垛小助手,我有两个主要功能: 1.帮助设置码垛参数 2.帮助生成码垛程序\n\n  在开始工作之前,我有几点需要和您说明:\n\n1.在进行参数设置时,与点位有关的参数需要您使用机器人进行示教,示教得到的点位数据需要您通过webapp界面复制粘贴到输入框中\n\n2.上面的预览窗口以俯视图显示工件在托盘上的摆放情况,会根据您的输入参数更新;参数配置中的起始方位代表作业的起始点:[0,0]-左上角,[0,1]-右上角,[1,0]-左下角,[1,1]-右下角;红色箭头和绿色箭头分别代表参数配置中的X和Y移动方向\n\n3.在示教托盘原点和吸盘位置时,请将一个工件摆放在作业起始位置上,托盘原点是此工件的几何中心,平面路径点是要摆放的第二个工件的几何中心,法向路径点是在平面路径点的基础上向码垛增高的方向移动一段距离(路径点与托盘原点的机器人末端姿态相同)\n\n4.通常情况下吸盘位置与工件几何中心重合,因此托盘原点和吸盘位置的示教可以使用同一个机器人位姿,但如果您的吸盘位置和工件几何中心不重合,请将托盘原点和吸盘位置分开示教\n\n  说明完毕,请对我说'你好'来开始吧!\n\n===============\n"

pallet_params = '1.工件配置:\n \
- 工件长度(float)\n \
- 工件宽度(float)\n \
- 工件高度(float)\n \
- 吸盘位置(list[x,y,z,rx,ry,rz])\n\
2.托盘配置:\n\
- 前边长度(float)\n\
- 侧边长度(float)\n\
3.模式配置:\n\
- 工件间隔(float)\n\
- 每层行数(int)\n\
- 每层列数(int)\n\
- 码垛层数(int)\n\
4.机器人移动配置:\n\
- 作业原点(list(float)[x,y,z,rx,ry,rz])\n\
- 作业准备点(list(float)[x,y,z,rx,ry,rz])\n\
- 工位过渡点(list[x,y,z,rx,ry,rz])\n\
- 托盘原点(list(float)[x,y,z,rx,ry,rz])\n\
- 平面路径点(list(float)[x,y,z,rx,ry,rz])\n\
- 法向路径点(list(float)[x,y,z,rx,ry,rz])\n\
- 起始方位(list(int),左上--[0,0] / 右上--[0,1] / 左下--[1,0] / 右下--[1,1])\n\
- 移动方向(str,红色--X / 绿色--Y)\n\
- 运动方式(str,点到点--ptp / 直线--line)\n\
- 运动路径(str,头到尾--headtail / 弓字形--zigzag)\n\
- 堆叠方式(str,堆垛--load / 卸垛--unload)'

yaml_content = '\
```yaml\n\
工件配置:\n\
    工件长度: 0.0\n\
    工件宽度: 0.0\n\
    工件高度: 0.0\n\
    吸盘位置: [0, 0, 0, 0, 0, 0]\n\
托盘配置:\n\
    前边长度: 0.0\n\
    侧边长度: 0.0\n\
模式配置:\n\
    工件间隔: 0.0\n\
    每层行数: 1\n\
    每层列数: 1\n\
    码垛层数: 1\n\
机器人移动配置:\n\
    作业原点: [0, 0, 0, 0, 0, 0]\n\
    作业准备点: [0, 0, 0, 0, 0, 0]\n\
    工位过渡点: [0, 0, 0, 0, 0, 0]\n\
    托盘原点: [0, 0, 0, 0, 0, 0]\n\
    平面路径点: [0, 0, 0, 0, 0, 0]\n\
    法向路径点: [0, 0, 0, 0, 0, 0]\n\
    起始方位: [0, 0]\n\
    移动方向: X\n\
    运动方式: line\n\
    运动路径: headtail\n\
    堆叠方式: load\n\
```'

pallet_params_dict = {'工件配置': {'工件长度': 0.0, '工件宽度': 0.0, '工件高度': 0.0, '吸盘位置': [0, 0, 0, 0, 0, 0]}, 
'托盘配置': {'前边长度': 0.0, '侧边长度': 0.0}, 
'模式配置': {'工件间隔': 0.0, '每层行数': 1, '每层列数': 1, '码垛层数': 1}, 
'机器人移动配置': {'作业原点': [0, 0, 0, 0, 0, 0], '作业准备点': [0, 0, 0, 0, 0, 0], '工位过渡点': [0, 0, 0, 0, 0, 0], '托盘原点':  [0, 0, 0, 0, 0, 0], '平面路径点':  [0, 0, 0, 0, 0, 0], '法向路径点':  [0, 0, 0, 0, 0, 0], '起始方位': [0, 0], '移动方向':'X', '运动方式': 'line', '运动路径': 'headtail', '堆叠方式': 'load'}}

python_content = f'\
```python \
from frpalletize import FRPalletize \
def main(): \
    params = ... \
    frpal = FRPalletize(params) \
    frpal.execute_palletize() \
if __name__ == \'__main__\': \
    main() \
```'

MSG_PALLETIZE_PARAM_CONFIG = [
{'role':'system', 'content':'a.用户选择设置参数:请引导用户逐步完成参数设置,提醒用户数据类型,对于str类参数,自动转换成对应值,如用户输入左,则转换成left'},
{'role':'user', 'content':f'请帮我完成码垛参数配置:{pallet_params},请检查数据类型和拼写,不要中途停止或设置不存在的参数,在我说"你好"后开始引导设置参数'},
{'role':'assistant', 'content':'好的,在你说"你好"后,我会说"我们开始进行参数设置吧。以下是您需要设置的参数(单位:mm,deg):",然后引导参数设置'},
{'role':'user', 'content':f'确认无误后,询问我要保存的文件名(用param_xxx.yaml命名,并检查文件名),然后复述文件名,并按如下格式显示yaml文件内容:{yaml_content}'},
{'role':'assistant', 'content':'好的'}
]

MSG_PALLETIZE_PROGRAM_GENERATION = [
{'role':'system', 'content':'b.用户选择生成程序:请提示用户"通过菜单栏导入配置文件",然后使用文件中参数生成码垛程序;如果用户说没有配置文件,则按照设置参数的情景进行引导'},
{'role':'user', 'content':'请帮我生成码垛程序'},
{'role':'assistant', 'content':f'好的,请导入参数YAML文件'},
{'role':'user', 'content':f'我会发给你一个包含所有参数的字典,例如{pallet_params_dict},请你完全按照如下格式复述字典中的参数:"导入的参数如下: {yaml_content}";导入参数之后,后台将生成码垛程序,先问我要保存的python文件名(用palletize_xxx.py命名,并检查文件名),然后复述文件名,并按照如下格式展示要保存的文件内容:{python_content},你需要将params的值"..."替换成用户的参数配置(字典dict型)'},
{'role':'assistant', 'content':'好的'}
]

system_content_intro = f'你是一个机器人助手,帮助用户控制机器人完成码垛任务,\
你有两个主要功能:1.引导用户完成码垛参数的设置 2.根据用户的参数生成码垛程序。\
首先,一定要询问用户需要进行何种操作:1.设置码垛参数 2.生成码垛程序,根据用户的选择,按照下文的情景a或b进行相应引导'

user_content_intro = f'情景a:我要设置参数,请模仿以下内容:{str(MSG_PALLETIZE_PARAM_CONFIG)}进行回答;\
情景b:我要生成程序,请模仿以下内容:{str(MSG_PALLETIZE_PROGRAM_GENERATION)}进行回答'

assistant_content_intro = f'好的'

MSG_PALLETIZE_INTRO = [
{'role':'system', 'content':system_content_intro},
{'role':'user', 'content':user_content_intro},
{'role':'assistant', 'content':assistant_content_intro}
]

system_content_intro_template = ChatPromptTemplate.from_messages([
                                    SystemMessagePromptTemplate.from_template(system_content_intro),
                                    MessagesPlaceholder(variable_name="history"),
                                    HumanMessagePromptTemplate.from_template("{input}")
                                    ])
