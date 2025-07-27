import os

from core.src.graphlonger import State
from core.src.graphlonger import (planner_node, 
                   reporter_node,
                   PPTAgent_team_node,
                   PPTAgent_node)
from langgraph.graph import StateGraph, END, START
from core.config.LLMConfig import VLMConfig
import json
VLMConfig = json.dumps(VLMConfig)
os.environ["VLMConfig"] = VLMConfig
from core.utils import current_dir
log_dir = os.path.join(current_dir, "log")
import argparse


def build_graph():
    builder = StateGraph(State)
    builder.add_edge(START, "planner")
    builder.add_node("planner", planner_node)
    builder.add_node("reporter", reporter_node)
    builder.add_node("PPTAgent_team", PPTAgent_team_node)
    builder.add_node("PPTAgent", PPTAgent_node)
    builder.add_edge("reporter", END)
    graph = builder.compile()
    return graph


def main(query, outfile):
    log_floder = os.path.join(log_dir, outfile)
    if not os.path.exists(log_floder):
        os.makedirs(log_floder)
    Initial_state = {
        "locale": "zh-CN",
        "query": query,
        "min_sections": 3,
        "max_sections": 7,
        "section_plan": [],
        "section_content": [],
        "final_content": "",
        "executed_sections": 0,
        "current_section_state": {},
        "log_floder": log_floder
    }
    print("Initial State: ", Initial_state)
    with open(os.path.join(log_floder, "initial_state.json"), "w", encoding="utf-8") as f:
        json.dump(Initial_state, f, indent=4, ensure_ascii=False)
    graph = build_graph()
    ret = graph.invoke(Initial_state)
    print(ret)
    with open(f"{current_dir}/output/{outfile}.md", "w", encoding="utf-8") as f:
        f.write(ret["final_report"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str, default="请为我生成一份初中语文将进酒”为主题的PPT大纲")
    args = parser.parse_args()
    main(args.query, args.query)