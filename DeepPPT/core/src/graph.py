from langgraph.graph import MessagesState, START, END
from langgraph.types import Command, interrupt
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage, HumanMessage
from typing import Annotated, Literal
from utils import get_llm_resp, extract_json_from_response, _create_llm_use_conf, extract_markdown_from_response
from ..config.LLMConfig import LLMConfig
import json
from tools import (
    crawl_tool,
    web_search_tool
)


class State(MessagesState):
    """State for the agent system, extends MessagesState with next field."""
    locale: str = "en-US"
    query: str = ""
    purpose: str = ""
    target: str = ""
    language_style: str = ""
    min_sections: int = 3
    max_sections: int = 7
    section_plan: list = []
    section_content: list = []
    final_report: str = ""
    executed_sections: int = 0
    current_section_state: dict = {}


def create_agent(agent_name, tools, messages, LLMConfig):
    return create_react_agent(
        name=agent_name,
        model=_create_llm_use_conf(LLMConfig),
        tools=tools,
        prompt=messages
    )


def planner_node(state: State) -> Command[Literal["PPTAgent_team"]]:
    print("===============Planner node running!===============")
    print("Planner received state: ", state)
    planner_prompt = open("../prompts/planner.md", "r").read()
    planner_prompt = planner_prompt.format(min_sections=state["min_sections"], max_sections=state["max_sections"])
    messages = [{"role": "system", "content": planner_prompt}, {"role": "user", "content": state["query"]}] + state["messages"]
    response = get_llm_resp(**LLMConfig, messages=messages)
    plan = extract_json_from_response(response)
    print("Plan: ", json.dumps(plan, indent=4, ensure_ascii=False))
    return Command(
        update={
            "locale": plan["language"],
            "purpose": plan["purpose"],
            "target": plan["target"],
            "language_style": plan["language_style"],
            "section_plan": plan["sections"],
        },
        goto="PPTAgent_team",
    )


def PPTAgent_team_node(state: State) -> Command[Literal["PPTAgent", "reporter"]]:
    print("===============PPTAgent_team node running!===============")
    # print("PPTAgent_team received state: ", state)
    plan = state["section_plan"]
    if state["current_section_state"]:
        state["section_content"].append(state["current_section_state"])
    if state["executed_sections"] == len(plan):
        return Command(
            update={},
            goto="reporter",
        )
    else:
        current_section_state = {
            "purpose": state["purpose"],
            "target": state["target"],
            "language_style": state["language_style"],
            "section_title": plan[state["executed_sections"]]["sub_title"],
            "section_description": plan[state["executed_sections"]]["description"],
            "section_pages": plan[state["executed_sections"]]["pages"],
            "section_content": "",
        }
        return Command(
            update={
                "executed_sections": state["executed_sections"] + 1,
                "current_section_state": current_section_state,
            },
            goto="PPTAgent",
        )


def PPTAgent_node(state: State) -> Command[Literal["PPTAgent_team"]]:
    print("===============PPTAgent node running!===============")
    # print("PPTAgent received state: ", state)
    current_section_state = state["current_section_state"]
    print(current_section_state)
    PPTAgent_prompt = open("../prompts/PPTAgent.md", "r").read()
    PPTAgent_prompt = PPTAgent_prompt.format(locale=state["locale"])
    
    tools = [web_search_tool, crawl_tool]
    PPTAgent = create_agent("PPTAgent", tools, PPTAgent_prompt, LLMConfig)
    agent_input = {
        "messages": [
            HumanMessage(
                content=json.dumps(current_section_state, ensure_ascii=False, indent=4)
            )
        ]
    }
    result = PPTAgent.invoke(input=agent_input)
    response_content = result["messages"][-1].content
    response_content = extract_markdown_from_response(response_content)
    # current_section_state.update({"section_content": response_content})

    return Command(
        update={
            "current_section_state": response_content,
        },
        goto="PPTAgent_team",
    )


def reporter_node(state: State):
    print("===============Reporter node running!===============")
    # print("Reporter received state: ", state)
    raw_content = "\n\n\n".join(state["section_content"])
    reporter_prompt = open("../prompts/reporter.md", "r").read()
    reporter_prompt = reporter_prompt.format(raw_content=raw_content)
    messages = [{"role": "system", "content": reporter_prompt}, {"role": "user", "content": raw_content}]
    response = get_llm_resp(**LLMConfig, messages=messages)
    response_content = extract_markdown_from_response(response)
    state["final_report"] = response_content
    return {"final_report": response_content}