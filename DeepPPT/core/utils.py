from openai import OpenAI
import json
import re
from langchain_openai import ChatOpenAI
from typing import Any, Dict
import os
current_dir = os.path.dirname(os.path.abspath(__file__))



def get_llm_resp(base_url, api_key, model, messages):
    """
    Get response from OpenAI API.

    Args:
        base_url (str): Base URL for the OpenAI API.
        api_key (str): API key for authentication.
        model (str): Model to use for generating the response.
        prompt (str): The input prompt for the model.

    Returns:
        str: The response from the model.
    """
    client = OpenAI(base_url=base_url, api_key=api_key)
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        # max_tokens=1000
    )
    return response.choices[0].message.content.strip()


def extract_json_from_response(response):
    # ```json```格式的解析
    json_str = re.search(r"```json\n(.*)\n```", response, re.DOTALL).group(1)
    # 增加异常检测
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in response: {json_str}")
        return {}


def _create_llm_use_conf(llm_conf) -> ChatOpenAI:
    # llm config提供一个dict，包含base_url, api_key, model
    return ChatOpenAI(**llm_conf)


def extract_markdown_from_response(response):
    if "</think>" in response:
        return response.split("</think>")[1]
    else:
        return response
    

def get_VLM_resp(VLMConfig, messages):
    # VLMConfig 是一个dict，包含base_url, api_key, model
    # messages 是一个list，包含role和content
    # 返回response
    client = OpenAI(base_url=VLMConfig["base_url"], api_key=VLMConfig["api_key"])
    response = client.chat.completions.create(
        model=VLMConfig["model"],
        messages=messages
    )
    return response.choices[0].message.content.strip()



if __name__ == "__main__":
    # Example usage
    base_url = "http://222.211.217.49:8188/v1/"
    api_key = "qwenqwenisreallylong"
    model = "Qwen3-32B"
    prompt = "What is the capital of France?"
    messages = [{"role": "user", "content": prompt}]
    llm_conf = {
        "base_url": base_url,
        "api_key": api_key,
        "model": model
    }
    llm = _create_llm_use_conf(llm_conf)
    response = llm.invoke(messages)
    print(response)