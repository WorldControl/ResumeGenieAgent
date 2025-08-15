# agents/match_agent.py
from ..utils import llm_adapter
from ..utils.prompt import match_agent_prompt
import json
import time


def match_agent_node(state):
    start_time = time.time()
    
    # 记录开始状态
    state["processing_details"].append({
        "step_name": "简历匹配",
        "status": "matching_resume",
        "message": "开始匹配简历与岗位",
        "details": {
            "resume_length": len(state.get("resume_text", "")),
            "target_jobs_count": len(state.get("analyzed_jobs", []))
        },
        "execution_time": None
    })
    
    resume_text = state.get("resume_text", "")
    target_job = state.get("analyzed_jobs", [{}])[0]  # 取第一个匹配岗位
    
    # 正确处理 skills 字典结构
    analyzed = target_job.get("analyzed", {})
    skills = analyzed.get("skills", {})
    
    # 将 skills 字典扁平化为列表
    technical_skills = skills.get("technical", [])
    soft_skills = skills.get("soft", [])
    experience = analyzed.get("experience", "")
    
    # 合并所有要求
    requirements = technical_skills + soft_skills + [experience]
    
    # 记录技能分析
    state["processing_details"].append({
        "step_name": "简历匹配",
        "status": "matching_resume",
        "message": "分析岗位技能要求",
        "details": {
            "technical_skills_count": len(technical_skills),
            "soft_skills_count": len(soft_skills),
            "total_requirements": len(requirements),
            "target_job_title": target_job.get("title", "未知")
        },
        "execution_time": None
    })
    
    formatted_prompt = match_agent_prompt.format(resume_text=resume_text, job_requirements=requirements)
    result_text = llm_adapter.call_llm(formatted_prompt)
    
    try:
        match_result = json.loads(result_text)
        match_status = "success"
        match_message = f"匹配完成，找到 {len(match_result.get('matched', []))} 项匹配"
    except Exception as e:
        match_result = {
            "matched": ["分析失败"],
            "gaps": ["无法识别"],
            "issues": ["表述不清"],
            "suggestions": ["请补充量化成果"]
        }
        match_status = "fallback"
        match_message = "匹配分析完成（使用备用数据）"
    
    # 记录匹配结果
    execution_time = time.time() - start_time
    state["processing_details"].append({
        "step_name": "简历匹配",
        "status": "completed",
        "message": match_message,
        "details": {
            "match_status": match_status,
            "matched_count": len(match_result.get("matched", [])),
            "gaps_count": len(match_result.get("gaps", [])),
            "suggestions_count": len(match_result.get("suggestions", [])),
            "resume_skills_matched": len(match_result.get("matched", []))
        },
        "execution_time": execution_time
    })
    
    state["match_result"] = match_result
    return state