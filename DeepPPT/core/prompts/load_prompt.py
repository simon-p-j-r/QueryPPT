from core.utils import current_dir

def load_prompt(agent_name: str) -> str:
    return open(f"{current_dir}/prompts/{agent_name}.md", "r", encoding="utf-8").read()