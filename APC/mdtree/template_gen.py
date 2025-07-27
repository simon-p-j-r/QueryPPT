from openai import OpenAI
from APC.config_parser import get_args_parser


def template_generation(prompt, content, layer):
    prompt1_filled = prompt.format(markdown=content, layer=layer)

    config = get_args_parser()
    client=OpenAI(
        api_key =config.OPENAI_API_KEY,
        base_url = config.OPENAI_BASE_URL
    )
    model = config.model

    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt1_filled}
        ],
        response_format={"type": "json_object"},
        temperature=0.2
    )
    raw_content = completion.choices[0].message.content
    if "</think>" in raw_content.strip():
        raw_content = raw_content.strip().split("</think>", 1)[1]
    if "```json" in raw_content.strip():
        raw_content = raw_content.strip().split("```json", 1)[1]
        if "```" in raw_content:
            raw_content = raw_content.rsplit("```", 1)[0]
    response_content = raw_content.strip()
    response_content = eval(response_content)
    return response_content
