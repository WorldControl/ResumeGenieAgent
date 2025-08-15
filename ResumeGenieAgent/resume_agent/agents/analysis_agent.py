import json
import time
from typing import Dict, Any, List

from ..utils import llm_adapter
from ..utils.prompt import analysis_agent_prompt


def _extract_json_text(text: str) -> str:
    if not text:
        return ""
    cleaned = text.strip()
    # Remove Markdown code fences if present
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`").strip()
        # After stripping backticks, remove optional language tag at start
        if cleaned.lower().startswith("json\n"):
            cleaned = cleaned[5:]
    # Heuristic: take substring from first '{' to last '}'
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        return cleaned[start:end + 1].strip()
    return cleaned


def job_analysis_agent_node(state):
    start_time = time.time()
    
    # 记录开始状态
    state["processing_details"].append({
        "step_name": "岗位分析",
        "status": "analyzing_jobs",
        "message": "开始分析岗位要求",
        "details": {"jobs_count": len(state.get("raw_jobs", []))},
        "execution_time": None
    })
    
    jobs = state.get("raw_jobs", [])
    analyzed_jobs = []
    
    for i, job in enumerate(jobs):
        # 记录单个岗位分析
        job_start = time.time()
        
        job_description = f"职位：{job.get('title','')}\n要求：{job.get('requirements','')}\n职责：{job.get('responsibilities','')}"
        formatted_prompt = analysis_agent_prompt.format(job_description=job_description)
        result_text = llm_adapter.call_llm(formatted_prompt)
        json_text = _extract_json_text(result_text)
        try:
            analyzed = json.loads(json_text)
            analysis_status = "success"
        except Exception as e:
            analyzed = {"skills": {"technical": [], "soft": []}, "experience": "", "education": "", "preparation": {"learning": [], "projects": [], "certificates": []}}
            analysis_status = "fallback"
        
        job["analyzed"] = analyzed
        analyzed_jobs.append(job)
        
        # 记录单个岗位分析结果
        job_time = time.time() - job_start
        state["processing_details"].append({
            "step_name": "岗位分析",
            "status": "completed",
            "message": f"完成岗位分析：{job.get('title', '未知')}",
            "details": {
                "job_title": job.get('title', '未知'),
                "analysis_status": analysis_status,
                "skills_count": len(analyzed.get("skills", {}).get("technical", []) + analyzed.get("skills", {}).get("soft", [])),
                "job_index": i + 1,
                "total_jobs": len(jobs)
            },
            "execution_time": job_time
        })
    
    # 记录整体完成状态
    total_time = time.time() - start_time
    state["processing_details"].append({
        "step_name": "岗位分析",
        "status": "completed",
        "message": f"完成所有岗位分析，共 {len(analyzed_jobs)} 个岗位",
        "details": {
            "total_analyzed": len(analyzed_jobs),
            "success_count": len([j for j in analyzed_jobs if j.get("analyzed")]),
            "total_skills_found": sum(len(j.get("analyzed", {}).get("skills", {}).get("technical", []) + j.get("analyzed", {}).get("skills", {}).get("soft", [])) for j in analyzed_jobs)
        },
        "execution_time": total_time
    })
    
    state["analyzed_jobs"] = analyzed_jobs
    return state


if __name__ == "__main__":
    state = {
        "raw_jobs": [
            {
                "title": "数据分析师",
                "requirements": "本科及以上，熟练使用SQL、Python，熟悉Tableau，有数据分析项目经验",
                "responsibilities": "负责用户行为数据分析，产出周报月报，支持业务决策"
            }
        ]
    }
    job_analysis_agent_node(state)
    print(state)