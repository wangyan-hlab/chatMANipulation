from frchat.gui import *
from frchat.init_prompt_palletize import MSG_PALLETIZE_INTRO

class FRChatGUIPalletize(FRChatGUI):
    """
        A GUI to use the FR ChatBot to generate palletization programs

        Author: wangyan
        Data: 2023/05/23
    """
    
    def __init__(self, bot, title, width=1024, height=512, font=('Times New Roman', 10)) -> None:
        super().__init__(bot, title, width, height, font)
        self.yaml_name = None
        self.palletize_params = None
        self.palletize_program_name = None

    def match_pattern(self, robot_connect=False):
        
        prompt = self.input_content
        response = self.output_content
        yaml_name_pattern = re.compile(r"param_([\s\S]*?)\.yaml")
        self.yaml_name = yaml_name_pattern.findall(response)
        yaml_content_pattern = re.compile(r"```yaml\n([\s\S]*?)\n```")
        self.palletize_params = yaml_content_pattern.findall(response)
        # 创建yaml文件
        if self.yaml_name and (self.yaml_name != "xxx"):
            dir = 'config/palletize/'
            if not os.path.exists(dir):
                os.mkdir(dir)
            yaml_filepath = os.path.join(dir, f'param_{self.yaml_name[-1]}.yaml')
            # 将匹配到的参数配置内容保存到yaml文件中
            if self.palletize_params:
                with open(yaml_filepath, 'w', encoding='utf-8') as f:
                    for match in self.palletize_params:
                        f.write(f"{match}\n")
                self.bot.messages = MSG_PALLETIZE_INTRO #TODO:创建还原点不成功
                print("[INFO] 参数设置完成,利用创建的还原点减少context length")
                print(">>>>><<<<<<<", len(self.bot.messages), self.bot.messages)

        palletize_program_name_pattern = re.compile(r"palletize_([\s\S]*?)\.py")
        self.palletize_program_name = palletize_program_name_pattern.findall(response)
        # 保存码垛python程序
        if self.palletize_program_name and (self.palletize_program_name != "xxx"):
            palletize_program_content = self.bot.gen_program('placeholder')
            print(">>>>>> py_content:", palletize_program_content)
            dir = 'palletize_program/'
            if not os.path.exists(dir):
                os.mkdir(dir)
            py_filepath = os.path.join(dir, f'palletize_{self.palletize_program_name[-1]}.py')
            with open(py_filepath, 'w', encoding='utf-8') as f:
                for match in palletize_program_content:
                    f.write(f"{match}\n")


