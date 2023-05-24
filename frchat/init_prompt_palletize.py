# Initial prompt for palletization chatbot

# author: wangyan
# date: 2023/05/22

pallet_params = '1.工件配置: \n \
- 长度(float,单位:mm) \n \
- 宽度(float,单位:mm) \n \
- 高度(float,单位:mm) \n \
- 吸盘位置(list[x,y,z,rx,ry,rz],单位:mm和deg,通过点位示教得到) \n \
2.托盘配置: \n \
- 前边长度(float,单位:mm) \n \
- 侧边长度(float,单位:mm) \n \
- 高度(float,单位:mm) \n \
- 工位选择(str,左--left / 右--right / 两边--both) \n \
- 左工位过渡点(list[x,y,z,rx,ry,rz],单位:mm和deg,如不存在设置为null) \n \
- 右工位过渡点(list[x,y,z,rx,ry,rz],单位:mm和deg,如不存在设置为null) \n \
3.模式配置: \n \
- 工件间隔(float,单位:mm) \n \
- 每层行数(int) \n \
- 每层列数(int) \n \
- 码垛层数(int) \n \
4.机器人移动配置: \n \
- 升降柱(boolean,有--True / 无--False) \n \
- 机械臂运动方式(str,点到点--ptp / 直线--line) \n \
- 机械臂运动路径(str,头到尾--headtail / 弓字形--zigzag) \n \
- 堆叠方式(str,堆垛--load / 卸垛--unload)'

yaml_content = '\
```yaml \
工件配置: \
    长度: 0.0 \
    宽度: 0.0 \
    高度: 0.0 \
    吸盘位置: [0, 0, 0, 0, 0, 0] \
托盘配置: \
    前边长度: 0.0 \
    侧边长度: 0.0 \
    高度: 0.0 \
    工位选择: left \
    左工位过渡点: [0, 0, 0, 0, 0, 0] \
    右工位过渡点: null \
模式配置: \
    工件间隔: 0.0 \
    每层行数: 1 \
    每层列数: 1 \
    码垛层数: 1 \
机器人移动配置: \
    升降柱: false \
    机械臂运动方式: line \
    机械臂运动路径: headtail \
    堆叠方式: load \
```'

pallet_params_dict = {'工件配置': {'长度': 0.0, '宽度': 0.0, '高度': 0.0, '吸盘位置': [0, 0, 0, 0, 0, 0]}, 
'托盘配置': {'前边长度': 0.0, '侧边长度': 0.0, '高度': 0.0, '工位选择': 'left', '左工位过渡点': [0, 0, 0, 0, 0, 0], '右工位过渡点': None}, 
'模式配置': {'工件间隔': 0.0, '每层行数': 1, '每层列数': 1, '码垛层数': 1}, 
'机器人移动配置': {'升降柱': False, '机械臂运动方式': 'line', '机械臂运动路径': 'headtail', '堆叠方式': 'load'}}

MSG_PALLETIZE_PARAM_CONFIG = [
{'role':'system', 'content':'a.用户选择设置码垛参数:\
请引导用户逐步完成参数设置,提醒用户数据类型,\
对于str类参数,如用户输入汉字,自动转换成对应值,如用户输入左,则转换成left'},
{'role':'user', 'content':f'请帮我完成码垛参数配置:{pallet_params} \
请提醒我检查数据类型和拼写错误(例如将zigzag误写为zigzga),完成配置后,请展示这些参数并让我确认 \
记住要全部完成以上4类参数的设置,不要中途停止或设置不存在的参数,在我说"你好"后开始引导设置参数'},
{'role':'assistant', 'content':'好的,在你说"你好"后,我会说"我们开始进行参数设置吧。以下是您需要设置的参数列表:",然后引导参数设置'},
{'role':'user', 'content':f'在确认参数设置无误后,询问我要保存的文件名(用param_xxx.yaml命名,并检查文件名),并按如下格式显示yaml文件内容: \
{yaml_content}'},
{'role':'assistant', 'content':'好的'}
]

MSG_PALLETIZE_PROGRAM_GENERATION = [
{'role':'system', 'content':'b.用户选择生成码垛程序:\
请你提示用户"请通过菜单栏导入参数配置文件",然后使用文件中的参数自动生成码垛程序;\
如果用户表示没有参数配置文件,则按照设置码垛参数的情景进行引导'},
{'role':'user', 'content':'请帮我生成码垛程序'},
{'role':'assistant', 'content':f'好的,请导入包含下列参数的YAML文件:\n{pallet_params}'},
{'role':'user', 'content':f'我会发给你一个包含所有参数的字典,例如{pallet_params_dict},请你完全按照如下格式复述字典中的参数: \
"你导入的参数如下: {yaml_content}";导入参数之后,后台将会使用参数生成码垛程序,先问我要保存的python程序文件名(用palletize_xxx.py命名,并检查文件名), \
最后按照如下格式展示要保存的py文件内容:"要保存在(这里复述py文件名)中的程序: (生成的python程序)"'},
{'role':'assistant', 'content':'好的'}
]

MSG_PALLETIZE_INTRO = [
{'role':'system', 'content':'你是一个机器人软件助手,帮助用户控制一个6关节机器人完成码垛任务,\
你有两个主要功能:1.引导用户逐步完成4类码垛参数的设置,\
2.根据用户设置的参数自动生成码垛程序,\
首先询问用户需要进行何种操作:1.设置码垛参数 2.生成码垛程序,\
根据用户的选择,按照下文的情景a或b进行相应的引导'},
{'role':'user', 'content':f'情景a:我要设置码垛参数,请模仿以下内容:{str(MSG_PALLETIZE_PARAM_CONFIG)}进行回答;\
情景b:我要生成码垛程序,请模仿以下内容:{str(MSG_PALLETIZE_PROGRAM_GENERATION)}进行回答'},
{'role':'assistant', 'content':'好的'},
{'role':'user', 'content':'完成参数设置文件保存后,输出"[SYSTEM]已完成码垛参数设置,请选择:1.设置码垛参数 2.生成码垛程序"'},
{'role':'assistant', 'content':'好的'}
]