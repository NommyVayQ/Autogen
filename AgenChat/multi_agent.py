import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.base import TaskResult
from autogen_agentchat.conditions import ExternalTermination, SourceMatchTermination, TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
from llms import get_model_client

# Create the primary agent.
primary_agent = AssistantAgent(
    "primary",
    model_client=get_model_client(),
    system_message="你是一个擅长编写古诗的助手",
)

# Create the critic agent.
critic_agent = AssistantAgent(
    "critic",
    model_client=get_model_client(),
    system_message="你是一位擅长批评的助手。针对给出的古诗写改进意见.如果你认为古诗很好，请回答APPROVE",
)
source_termination = SourceMatchTermination("critic")
# text_termination = TextMentionTermination("APPROVE")

team = RoundRobinGroupChat([primary_agent, critic_agent], termination_condition=source_termination)

async def main():
    stream = team.run_stream(task="Write a short poem about the fall season.")
    async for event in stream:
        print(event)

asyncio.run(main())