import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console # 引入官方的控制台打印工具，专门处理流式
from llms import model_client  


agent = AssistantAgent(
        name="report_agent",
        model_client=model_client,
        system_message="你是一个善于写古诗的助手",
        model_client_stream=True
    )

async def main():
    result = await agent.run(task="编写一首四言古诗")#等待run方法执行完成，返回结果
    print(result)

async def main_stream():
    #获取协程对象
    result = agent.run_stream(task="编写一首四言古诗")#当前代码不会执行，直接返回一个协程对象
    async for item in result:
        if isinstance(item,ModelClientStreamingChunkEvent):
            stream += item.content
        print(item)
async def main_console():
    await Console(agent.run_stream(task="编写一首四言古诗"))

asyncio.run(main_console())
