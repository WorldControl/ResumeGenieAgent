from dotenv import load_dotenv
import os
from openai import OpenAI
from pathlib import Path

# 获取项目根目录的 .env 文件路径
project_root = Path(__file__).parent.parent.parent
env_path = project_root / ".env"
load_dotenv(env_path)

def call_llm(prompt):
    api_key = os.getenv('MODEL_SCOPE_API_KEY')
    if not api_key:
        raise RuntimeError(
            f"Missing MODEL_SCOPE_API_KEY environment variable. "
            f"Please set it in your .env file at {env_path} or environment."
        )
    
    # 延迟初始化客户端，避免模块导入时检查API key
    client = OpenAI(
        base_url=os.getenv('MODEL_SCOPE_BASE_URL', 'https://api-inference.modelscope.cn/v1'),
        api_key=api_key,
    )
    
    response = client.chat.completions.create(
        model='Qwen/Qwen3-Coder-480B-A35B-Instruct',
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        stream=True,
    )
    content = ""
    for chunk in response:
        delta = chunk.choices[0].delta.content
        if delta:
            content += delta
    return content


