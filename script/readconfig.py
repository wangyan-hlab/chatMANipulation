import argparse
import os
import yaml

# 可选flag:
# cwd - 配置文件所在目录
# file - 配置文件名
# 示例: python script/readconfig.py --cwd=./config/fr_robot/ --file=robot_movement
parser = argparse.ArgumentParser()
parser.add_argument("--cwd", type=str, default="")
parser.add_argument("--file", type=str, default="")
args = parser.parse_args()

if args.cwd:
    os.chdir(args.cwd)

# 读取yaml配置文件
with open(args.file+".yaml", "r") as f:
    functions = yaml.safe_load(f)

# 定义一个函数，用来生成输出列表中的每个子列表
def generate_function_list(func):
    func_name = func['name']
    args = ", ".join(arg['name'] for arg in func['arguments'])
    desc = func['description']
    arg_desc = ", ".join(f"{arg['name']}:{arg['description']}({arg['type']}型变量)" for arg in func['arguments'])
    ret = func['return']
    return [f"{func_name}", f"功能:'{desc}'", f"参数:'{arg_desc}'", f"返回值:'{ret}'"]

# 生成输出列表
output = [generate_function_list(func['function']) for func in functions]

# 打印输出列表
print(output)
