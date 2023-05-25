import copy
from frchat.gui import *
from frchat.bot_palletize import FRChatBotPalletize
from frchat.init_prompt_palletize import MSG_PALLETIZE_INTRO, WELCOME_TEXT


class FRChatGUIPalletize(FRChatGUI):
    """
        A GUI to use the FR ChatBot to generate palletization programs

        Author: wangyan
        Data: 2023/05/23
    """
    
    def __init__(self, title, width=1024, height=768, font=('Times New Roman', 10)) -> None:
        super().__init__(title, width, height, font)
        self.bot = FRChatBotPalletize(messages=MSG_PALLETIZE_INTRO,temperature=0.1)
        self.init_prompt =  copy.deepcopy(MSG_PALLETIZE_INTRO)
        # 文件保存相关
        self.yaml_name = None
        self.yaml_content = None
        self.python_name = None
        self.python_content = None
        # 图形绘制相关
        self.box_length = None
        self.box_width = None
        self.pallet_length = None
        self.pallet_width = None
        self.box_interval = None
        self.nrow = None
        self.ncol = None
        self.canvas = None


    def create_gui(self):
        """
            Create the GUI
        """
        ## 创建主窗口
        root = self.root
        root.title(self.title)
        root.geometry(f"{self.width}x{self.height}")
        font = self.font

        ## 创建输入历史框和用户输入框
        frame_left = tk.Frame(root)
        frame_left.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        ### 创建输入历史框
        label_input = tk.Label(frame_left, text="输入历史", font=font)
        label_input.grid(row=0, column=0, sticky="w")
        scrollbar_input_history = tk.Scrollbar(frame_left)
        text_input_history = tk.Text(frame_left, 
                                    width=10, 
                                    height=10, 
                                    yscrollcommand=scrollbar_input_history.set,
                                    font=font)
        text_input_history.grid(row=1, column=0, sticky="nsew")
        scrollbar_input_history.config(command=text_input_history.yview)
        scrollbar_input_history.grid(row=1, column=1, sticky="ns")
        ### 创建用户输入框
        label_input = tk.Label(frame_left, text="请输入(回车换行,Ctrl+s发送)", font=font)
        label_input.grid(row=2, column=0, sticky="w")
        scrollbar_input = tk.Scrollbar(frame_left)
        text_input = tk.Text(frame_left, 
                            width=10, 
                            height=10, 
                            yscrollcommand=scrollbar_input.set,
                            font=font)
        text_input.grid(row=3, column=0, sticky="nsew")
        scrollbar_input.config(command=text_input.yview)
        scrollbar_input.grid(row=3, column=1, sticky="ns")
        ## 创建输出框
        frame_right = tk.Frame(root)
        frame_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        label_output = tk.Label(frame_right, text="小助手", font=font)
        label_output.grid(row=0, column=0, sticky="w")
        scrollbar_output = tk.Scrollbar(frame_right)
        text_output = tk.Text(frame_right, 
                            width=10, 
                            height=20, 
                            yscrollcommand=scrollbar_output.set,
                            font=font)
        text_output.grid(row=1, column=0, sticky="nsew")
        scrollbar_output.config(command=text_output.yview)
        scrollbar_output.grid(row=1, column=1, sticky="ns")
        text_output.insert("end", WELCOME_TEXT)
        ## 创建图形绘制框
        #TODO:
        # frame_draw = tk.Frame(root)
        # frame_draw.

        ## 让文本框适应窗口大小
        frame_left.rowconfigure(1, weight=1)
        frame_left.rowconfigure(3, weight=1)
        frame_left.columnconfigure(0, weight=1)
        frame_left.columnconfigure(1, weight=0)
        frame_right.rowconfigure(1, weight=1)
        frame_right.columnconfigure(0, weight=1)
        frame_right.columnconfigure(1, weight=0)

        ## 禁止输入历史框和输出框编辑
        text_input_history.config(state="disabled")
        text_output.config(state="disabled")

        ## 菜单栏用于导入yaml配置文件
        ### 创建一个空菜单，用于添加文件选项
        menubar = tk.Menu(root) 
        filemenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="配置文件", menu=filemenu)
        ### 将 “打开” 选项添加到菜单中
        filemenu.add_command(label="打开", command=self.open_file)
        ### 将单栏添加到主窗口中
        root.config(menu=menubar)

        ### 让输入框在每次输入后自动滚动到底部
        def on_input_change(*_):
            text_input.yview_moveto(1.0)
        text_input.bind("<KeyPress>", on_input_change)

        return text_input_history, text_input, text_output


    def match_pattern(self, robot_connect=False):
        
        prompt = self.input_content
        response = self.output_content

        # 匹配yaml相关内容
        yaml_name_pattern = re.compile(r"param_([\s\S]*?)\.yaml")
        self.yaml_name = yaml_name_pattern.findall(response)
        yaml_content_pattern = re.compile(r"```yaml\n([\s\S]*?)\n```")
        self.yaml_content = yaml_content_pattern.findall(response)
        # 创建yaml文件
        if self.yaml_name and (self.yaml_name[-1] != "xxx"):
            dir = 'config/palletize/'
            if not os.path.exists(dir):
                os.mkdir(dir)
            yaml_filepath = os.path.join(dir, f'param_{self.yaml_name[-1]}.yaml')
            # 将匹配到的参数配置内容保存到yaml文件中
            if self.yaml_content:
                with open(yaml_filepath, 'w', encoding='utf-8') as f:
                    for match in self.yaml_content:
                        f.write(f"{match}\n")
                        print("[INFO] yaml文件已输出!")
                # 为了防止token超限，使用initial prompt重新初始化
                self.reinit_prompt()

        # 匹配python相关内容
        python_name_pattern = re.compile(r"palletize_([\s\S]*?)\.py")
        self.python_name = python_name_pattern.findall(response)
        python_content_pattern = re.compile(r"```python\n([\s\S]*?)\n```")
        self.python_content = python_content_pattern.findall(response)
        # 保存码垛python程序
        if self.python_name and (self.python_name[-1] != "xxx"):
            dir = 'palletize_program/'
            if not os.path.exists(dir):
                os.mkdir(dir)
            py_filepath = os.path.join(dir, f'palletize_{self.python_name[-1]}.py')
            if self.python_content:
                with open(py_filepath, 'w', encoding='utf-8') as f:
                    for match in self.python_content:
                        f.write(f"{match}\n")
                        print("[INFO] python程序已输出!")
        
        # 匹配图形绘制相关数据
        box_length_match = re.search(r"长度: (\d+.\d+)", self.yaml_content)
        self.box_length = float(box_length_match)
        box_width_match = re.search(r"宽度: (\d+.\d+)", self.yaml_content)
        self.box_width = float(box_width_match)
        pallet_length_match = re.search(r"前边长度: (\d+.\d+)", self.yaml_content)
        self.pallet_length = float(pallet_length_match)
        pallet_width_match = re.search(r"侧边长度: (\d+.\d+)", self.yaml_content)
        self.pallet_width = float(pallet_width_match)
        box_interval = re.search(r"工件间隔: (\d+.\d+)", self.yaml_content)
        self.box_interval = float(box_interval)
        nrow_match = re.search(r"每层行数: (\d+)", self.yaml_content)
        self.nrow = int(nrow_match)
        ncol_match = re.search(r"每层列数: (\d+)", self.yaml_content)
        self.ncol = int(ncol_match)

    
    def start_gui(self):
        self.text_input_history, self.text_input, self.text_output = self.create_gui()
        self.root.bind("<Control-Key-s>", self.process_message)
        self.root.bind("<Control-Key-r>", self.reinit_prompt)
        ## 开始事件循环
        self.root.mainloop()


    def reinit_prompt(self, *args):
        """
            重新初始化prompt
        """
        self.bot.messages.clear()
        self.bot.messages = self.init_prompt
        print("[Reinit] bot_messages", self.bot.messages)


    def update_scale_factor(self, value):
        """
            图形绘制比例尺
        """
        global SCALE_FACTOR
        SCALE_FACTOR = int(value)
        self.draw_rectangle()


    def draw_rectangle(self):
        """
            根据参数配置绘制图形
        """
        # 缩放矩形的长度、宽度和摆放间隔
        scaled_box_length = self.box_length * SCALE_FACTOR
        scaled_box_width = self.box_width * SCALE_FACTOR
        scaled_box_interval = self.box_interval * SCALE_FACTOR

        self.canvas.delete("rectangle")

        for row in range(self.nrow):
            for col in range(self.ncol):
                x1 = 10 + (scaled_box_length + scaled_box_interval) * col
                y1 = 10 + (scaled_box_width + scaled_box_interval) * row
                x2 = x1 + scaled_box_length
                y2 = y1 + scaled_box_width
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="cyan", tags="rectangle")
                        