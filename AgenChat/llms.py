from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelFamily

def get_model_client():
    openai_model_client = OpenAIChatCompletionClient(
        model="deepseek-chat",
        base_url="https://api.deepseek.com/v1",
        api_key="sk-7bb9a1e265234c76a409e4ea061311bc",
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
    return openai_model_client

    #单例设计模式
model_client = get_model_client()