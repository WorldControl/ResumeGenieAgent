# agents/graph.py
from langgraph.graph import StateGraph, START, END
from .data_collect_agent import data_agent_node
from .analysis_agent import job_analysis_agent_node
from .match_agent import match_agent_node
from .report_agent import report_agent_node


def create_agent_graph():
    workflow = StateGraph(dict)

    # 定义节点
    workflow.add_node("data", data_agent_node)
    workflow.add_node("analysis", job_analysis_agent_node)
    workflow.add_node("match", match_agent_node)
    workflow.add_node("report", report_agent_node)

    # 构建图流程
    workflow.add_edge(START, "data")
    workflow.add_edge("data", "analysis")
    workflow.add_edge("analysis", "match")
    workflow.add_edge("match", "report")
    workflow.add_edge("report", END)

    # 编译图
    app = workflow.compile()
    return app