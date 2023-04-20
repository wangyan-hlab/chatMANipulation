from chatgpt_wrapper import OpenAIAPI

bot = OpenAIAPI()
success, response, message = bot.ask("Hello, world.")
if success:
    print(response)
else:
    raise RuntimeError(message)
