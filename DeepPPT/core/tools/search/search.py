# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

import json
import logging
import os
from typing import Type, TypeVar, Any

from langchain_community.tools import BraveSearch, DuckDuckGoSearchResults
from langchain_community.tools.arxiv import ArxivQueryRun
from langchain_community.utilities import ArxivAPIWrapper, BraveSearchWrapper

SEARCH_MAX_RESULTS = 3
from core.tools.search.tavily_search.tavily_search_results_with_images import (
    TavilySearchResultsWithImages,
)

logger = logging.getLogger(__name__)

class LoggedToolMixin:
    def _log_operation(self, method_name: str, *args: Any, **kwargs: Any) -> None:
        tool_name = self.__class__.__name__.replace("Logged", "")
        params = ", ".join(
            [*(str(arg) for arg in args), *(f"{k}={v}" for k, v in kwargs.items())]
        )
        logger.debug(f"Tool {tool_name}.{method_name} called with parameters: {params}")

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """Override _run method to add logging."""
        self._log_operation("_run", *args, **kwargs)
        result = super()._run(*args, **kwargs)
        logger.debug(
            f"Tool {self.__class__.__name__.replace('Logged', '')} returned: {result}"
        )
        return result


T = TypeVar("T")
def create_logged_tool(base_tool_class: Type[T]) -> Type[T]:
    class LoggedTool(LoggedToolMixin, base_tool_class):
        pass
    LoggedTool.__name__ = f"Logged{base_tool_class.__name__}"
    return LoggedTool


LoggedTavilySearch = create_logged_tool(TavilySearchResultsWithImages)
tavily_search_tool = LoggedTavilySearch(
    name="web_search",
    max_results=SEARCH_MAX_RESULTS,
    include_raw_content=True,
    include_images=True,
    include_image_descriptions=True,
)

LoggedDuckDuckGoSearch = create_logged_tool(DuckDuckGoSearchResults)
duckduckgo_search_tool = LoggedDuckDuckGoSearch(
    name="web_search", max_results=SEARCH_MAX_RESULTS
)

LoggedBraveSearch = create_logged_tool(BraveSearch)
brave_search_tool = LoggedBraveSearch(
    name="web_search",
    search_wrapper=BraveSearchWrapper(
        api_key=os.getenv("BRAVE_SEARCH_API_KEY", ""),
        search_kwargs={"count": SEARCH_MAX_RESULTS},
    ),
)

LoggedArxivSearch = create_logged_tool(ArxivQueryRun)
arxiv_search_tool = LoggedArxivSearch(
    name="web_search",
    api_wrapper=ArxivAPIWrapper(
        top_k_results=SEARCH_MAX_RESULTS,
        load_max_docs=SEARCH_MAX_RESULTS,
        load_all_available_meta=True,
    ),
)

if __name__ == "__main__":
    results = LoggedDuckDuckGoSearch(
        name="web_search", max_results=SEARCH_MAX_RESULTS, output_format="list"
    ).invoke("cute panda")
    print(json.dumps(results, indent=2, ensure_ascii=False))
