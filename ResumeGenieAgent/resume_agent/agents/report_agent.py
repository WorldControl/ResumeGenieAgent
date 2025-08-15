# agents/report_agent.py
from ..utils import llm_adapter
from ..utils.prompt import report_agent_prompt
import json
import time


def report_agent_node(state):
    start_time = time.time()
    
    # 记录开始状态
    state["processing_details"].append({
        "step_name": "报告生成",
        "status": "generating_report",
        "message": "开始生成分析报告",
        "details": {
            "match_result_summary": {
                "matched_count": len(state.get("match_result", {}).get("matched", [])),
                "gaps_count": len(state.get("match_result", {}).get("gaps", [])),
                "suggestions_count": len(state.get("match_result", {}).get("suggestions", []))
            }
        },
        "execution_time": None
    })
    
    match = state.get("match_result", {})
    formatted_prompt = report_agent_prompt.format(matched=match.get("matched", []), gaps=match.get("gaps", []), issues=match.get("issues", []))
    
    try:
        content = llm_adapter.call_llm(formatted_prompt)
        report_status = "success"
        report_message = "报告生成完成"
    except Exception as e:
        content = f"报告生成失败：{str(e)}"
        report_status = "fallback"
        report_message = "报告生成完成（使用备用内容）"
    
    # 记录报告生成结果
    report_time = time.time() - start_time
    state["processing_details"].append({
        "step_name": "报告生成",
        "status": "completed",
        "message": report_message,
        "details": {
            "report_status": report_status,
            "report_length": len(content),
            "content_preview": content[:100] + "..." if len(content) > 100 else content
        },
        "execution_time": report_time
    })
    
    score = 60  # 默认
    if "80" in content: score = 80
    elif "70" in content: score = 70
    elif "90" in content: score = 90

    state["final_report"] = {
        "match_score": score,
        "strengths": [s.strip() for s in match.get("matched", [])[:3]],
        "gaps": [g.strip() for g in match.get("gaps", [])[:3]],
        "suggestions": [s.strip() for s in match.get("suggestions", [])[:5]],
        "detailed_report": content
    }
    
    # 记录最终完成状态
    total_time = time.time() - start_time
    state["processing_details"].append({
        "step_name": "报告生成",
        "status": "completed",
        "message": "所有分析完成！",
        "details": {
            "final_score": score,
            "total_processing_time": total_time,
            "summary": {
                "strengths_count": len(state["final_report"]["strengths"]),
                "gaps_count": len(state["final_report"]["gaps"]),
                "suggestions_count": len(state["final_report"]["suggestions"])
            }
        },
        "execution_time": total_time
    })
    
    return state