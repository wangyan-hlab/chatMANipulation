# 在终端运行chatgpt之前执行，用于设置ChatGPT密钥
# 密钥文件需要自行导入

export OPENAI_API_KEY=$(cat chatgpt_key.txt)
echo "OPENAI_API_KEY read."
