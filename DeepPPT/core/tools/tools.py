# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

import logging
import sys
from typing import Annotated, Callable, Any
import functools
from langchain_core.tools import tool
import re
from urllib.parse import urljoin
from markdownify import markdownify as md
import os
import json
from core.utils import current_dir
if os.environ.get("TAVILY_API_KEY") is None:
    os.environ["TAVILY_API_KEY"] = ""
# current_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.append(current_dir)
import requests
from readabilipy import simple_json_from_html_string
import enum
# from core.tools.search.search import tavily_search_tool, duckduckgo_search_tool, brave_search_tool, arxiv_search_tool

logger = logging.getLogger(__name__)


# These are codes from deerflow
class Article:
    url: str
    def __init__(self, title: str, html_content: str):
        self.title = title
        self.html_content = html_content

    def to_markdown(self, including_title: bool = True) -> str:
        markdown = ""
        if including_title:
            markdown += f"# {self.title}\n\n"
        markdown += md(self.html_content)
        return markdown

    def to_message(self) -> list[dict]:
        image_pattern = r"!\[.*?\]\((.*?)\)"
        content: list[dict[str, str]] = []
        parts = re.split(image_pattern, self.to_markdown())
        for i, part in enumerate(parts):
            if i % 2 == 1:
                image_url = urljoin(self.url, part.strip())
                content.append({"type": "image_url", "image_url": {"url": image_url}})
            else:
                content.append({"type": "text", "text": part.strip()})

        return content


class JinaClient:
    def crawl(self, url: str, return_format: str = "html") -> str:
        headers = {
            "Content-Type": "application/json",
            "X-Return-Format": return_format,
        }
        if os.getenv("JINA_API_KEY"):
            headers["Authorization"] = f"Bearer {os.getenv('JINA_API_KEY')}"
        else:
            logger.warning(
                "Jina API key is not set. Provide your own key to access a higher rate limit. See https://jina.ai/reader for more information."
            )
        data = {"url": url}
        response = requests.post("https://r.jina.ai/", headers=headers, json=data)
        return response.text


class ReadabilityExtractor:
    def extract_article(self, html: str) -> Article:
        article = simple_json_from_html_string(html, use_readability=True)
        return Article(
            title=article.get("title"),
            html_content=article.get("content"),
        )


class Crawler:
    def crawl(self, url: str) -> Article:
        jina_client = JinaClient()
        html = jina_client.crawl(url, return_format="html")
        extractor = ReadabilityExtractor()
        article = extractor.extract_article(html)
        article.url = url
        return article


def log_io(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        func_name = func.__name__
        params = ", ".join(
            [*(str(arg) for arg in args), *(f"{k}={v}" for k, v in kwargs.items())]
        )
        logger.info(f"Tool {func_name} called with parameters: {params}")
        result = func(*args, **kwargs)
        logger.info(f"Tool {func_name} returned: {result}")
        return result
    return wrapper


@tool
@log_io
def crawl_tool(
    url: Annotated[str, "The url to crawl."],
) -> str:
    """Use this to crawl a url and get a readable content in markdown format."""
    try:
        crawler = Crawler()
        article = crawler.crawl(url)
        ret = {"url": url, "crawled_content": article.to_markdown()[:1000]}
        if not os.path.exists(f"{current_dir}/data/{url.replace('/', '_')}"):
            os.makedirs(f"{current_dir}/data/{url.replace('/', '_')}")
        with open(f"{current_dir}/data/{url.replace('/', '_')}/crawl_result.txt", "w") as f:
            f.write(ret["crawled_content"])
        return ret
    except BaseException as e:
        error_msg = f"Failed to crawl. Error: {repr(e)}"
        logger.error(error_msg)
        return error_msg



class SearchEngine(enum.Enum):
    TAVILY = "tavily"
    DUCKDUCKGO = "duckduckgo"
    BRAVE_SEARCH = "brave_search"
    ARXIV = "arxiv"

# search_tool_mappings = {
#     SearchEngine.TAVILY.value: tavily_search_tool,
#     SearchEngine.DUCKDUCKGO.value: duckduckgo_search_tool,
#     SearchEngine.BRAVE_SEARCH.value: brave_search_tool,
#     SearchEngine.ARXIV.value: arxiv_search_tool,
# }

# SELECTED_SEARCH_ENGINE = SearchEngine.TAVILY.value
# SEARCH_MAX_RESULTS = 3
# web_search_tool = search_tool_mappings.get(SELECTED_SEARCH_ENGINE, tavily_search_tool)


# our own search tool
from core.tools.search.baidu_search.baidu_search import baidu_search
from core.tools.search.baidu_search.baidu_images import search_images_with_description
@tool
@log_io
def baidu_image_search_tool(
    query: Annotated[str, "The keyword to search."],
) -> list[tuple[str, str]]:
    """Use this to search images from baidu.
    Args:
        query: The keyword to search.
    Returns:
        A list of (image path, image description).
    """
    logger.info(f"==baidu_image_search_tool: {query}")
    existed_querys = os.listdir(f"{current_dir}/data")
    if query in existed_querys:
        with open(f"{current_dir}/data/{query}/search_images.json", "r", encoding="utf-8") as f:
            images = json.load(f)
            return images
    else:
        images = search_images_with_description(query)
        return images



@tool
@log_io
def baidu_search_tool(
    query: Annotated[str, "The keyword to search."],
) -> list[dict[str, str, str, str]]:
    """Use this to search knowledge from baidu.
    Args:
        query: The keyword to search.
    Returns:
        A list of {title, link, abstract, source}.
    """
    logger.info(f"==baidu_search_tool: {query}")
    ret = baidu_search(query)
    if not os.path.exists(f"{current_dir}/data/{query}"):
        os.makedirs(f"{current_dir}/data/{query}")
    with open(f"{current_dir}/data/{query}/baidu_search.json", "w") as f:
        json.dump(ret, f, indent=4, ensure_ascii=False)
    return ret


if __name__ == "__main__":
    with open(f"{current_dir}/data/胡桃/000000.jpg", "rb") as f:
        image_data = f.read()
    print(image_data)