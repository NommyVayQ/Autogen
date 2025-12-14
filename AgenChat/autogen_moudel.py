import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import UserMessage, SystemMessage, ModelFamily
from dotenv import load_dotenv


load_dotenv()#读取env文件

openai_model_client = OpenAIChatCompletionClient(
    model=os.getenv("MODEL", "deepseek-chat"),#若未设置MODEL环境变量，默认使用deepseek-chat
    base_url=os.getenv("BASE_URL", "https://api.deepseek.com/v1"),#若未设置BASE_URL环境变量，默认使用https://api.deepseek.com/v1
    api_key=os.getenv("API_KEY"),
    model_info={
        "vision": False,
        "function_calling": True,
        "json_output": True,
        "family": ModelFamily.UNKNOWN,
        #结构化输出
        "structured_output": True,
        "multiple_system_messages": True,
    }
)

from autogen_core.models import UserMessage
#定义一个协程函数
async def main():
    result = await openai_model_client.create([UserMessage(content="解释一下冒泡排序", source="user"),
                                            SystemMessage(content="你是一个编程高手")]) 
    print(result)
    await openai_model_client.close()

# 运行主函数
asyncio.run(main())
