# Installation
安装[chatgpt-wrapper](https://github.com/mmabrouk/chatgpt-wrapper):
```bash
pip install git+https://github.com/mmabrouk/chatgpt-wrapper
```

# ChatGPT Prompts 技巧

## Clear Communication (CC) 原则

### Prompts要清晰明确
1. 定义对话的**目的**和**重心**
2. 语言要**具体**，内容要**相关**
3. 避免**开放**、**宽泛**的prompts
4. 避免对话**离题**

### 术语和歧义的处理
1. 对术语进行定义
2. 避免使用带有歧义的语言
3. 使用清晰、明确的语言

#### Bad Example
> "Hey there! Can you give me some intel on the latest happenings in the interwebz? I'm trying to get a handle on the zeitgeist."
#### Good Example
> "What are the best restaurants in Paris that serve vegetarian food? I'm planning a trip to Paris and I'm looking for some good places to eat that cater to my dietary needs."

## 创建 Prompts 的一般步骤
1. 明确**目的**和**重心**
2. 使用**具体**、**相关**的语言
3. 避免**开放**、**宽泛**的prompts
4. 按照CC原则**检查**、**修改**prompts

## 如何掌控对话的走向
1. 用清晰明确的prompt开启对话
2. 鼓励ChatGPT完善回答
3. 注意说话的语气，忌过度随意、轻蔑
4. 时刻注意对话的走向，并做出必要的调整

## :star: “Act as ...” 魔法
### 作用
创建沉浸式的对话情景，模拟真实世界的场景
### An Example
- I want you to **act as** a javascript console. 
- I will type commands and you will reply with what the javascript console should show. 
- I want you to only reply with the terminal output inside one unique code block, and nothing else. 
- Do not write explanations. 
- Do not type commands unless I instruct you to do so. 
- When I need to tell you something in english, i will do so by putting text inside curly brackets {like this}. 
- My first command is console.log("Hello World");
