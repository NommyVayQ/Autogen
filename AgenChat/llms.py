from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelFamily
import os
from dotenv import load_dotenv
from pathlib import Path

root_dir = Path(__file__).resolve().parents[1]
load_dotenv(dotenv_path=root_dir / ".env", override=True)

def get_model_client():
    model = os.getenv("MODEL_NAME") or os.getenv("MODEL") or "deepseek-chat"
    base_url = os.getenv("API_BASE_URL") or os.getenv("BASE_URL") or "https://api.deepseek.com/v1"
    api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY") or os.getenv("API_KEY") or ""
    if not api_key:
        raise RuntimeError("Missing API key: set DEEPSEEK_API_KEY or OPENAI_API_KEY")

    return OpenAIChatCompletionClient(
        model=model,
        base_url=base_url,
        api_key=api_key,
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": ModelFamily.UNKNOWN,
            "structured_output": True,
            "multiple_system_messages": True,
        },
    )

# 单例默认为不初始化，避免缺少密钥时报错
# 如需在其他模块使用，请在运行时调用 get_model_client()
