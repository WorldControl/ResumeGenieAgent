# agents/data_agent.py
import time

# 模拟岗位数据库
JOB_DB = [
    {
        "title": "数据分析师",
        "company": "某科技公司",
        "salary": "15-25k",
        "requirements": "本科及以上，熟练使用SQL、Python，熟悉Tableau，有数据分析项目经验",
        "responsibilities": "负责用户行为数据分析，产出周报月报，支持业务决策"
    },
    {
        "title": "高级数据分析师",
        "company": "某电商平台",
        "salary": "20-35k",
        "requirements": "3年以上经验，精通SQL和Python，熟悉A/B测试，有电商背景",
        "responsibilities": "构建数据看板，进行转化率分析，支持营销策略"
    }
]

def data_agent_node(state):
    start_time = time.time()
    
    # 初始化处理详情列表
    if "processing_details" not in state:
        state["processing_details"] = []
    
    # 记录开始状态
    state["processing_details"].append({
        "step_name": "数据收集",
        "status": "collecting_data",
        "message": "开始收集岗位数据",
        "details": {"job_title": state.get("job_title", "未知")},
        "execution_time": None
    })
    
    job_title = state.get("job_title")
    # 模拟匹配
    results = [job for job in JOB_DB if job_title.lower() in job["title"].lower()]
    
    # 记录完成状态
    execution_time = time.time() - start_time
    state["processing_details"].append({
        "step_name": "数据收集",
        "status": "completed",
        "message": f"找到 {len(results)} 个匹配岗位",
        "details": {
            "found_jobs": len(results),
            "job_titles": [job["title"] for job in results],
            "search_query": job_title
        },
        "execution_time": execution_time
    })
    
    state["raw_jobs"] = results
    return state