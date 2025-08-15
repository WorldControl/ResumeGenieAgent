# main.py

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import time
from .schemas import JobSearchRequest, ReportResponse, JobSearchResponse
from .agents.graph import create_agent_graph
from .utils.resume_parser import parse_resume
import json

app = FastAPI(title="AI简历智能助手")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建Agent图
agent_graph = create_agent_graph()

@app.post("/search_jobs", response_model=JobSearchResponse)
async def search_jobs(request: JobSearchRequest):
    start_time = time.time()
    
    # 初始化状态
    state = {
        "job_title": request.job_title,
        "processing_details": []
    }
    
    # 执行Agent流程
    result = agent_graph.invoke(state)
    
    # 计算总处理时间
    total_time = time.time() - start_time
    
    return JobSearchResponse(
        jobs=result.get("analyzed_jobs", []),
        total_count=len(result.get("analyzed_jobs", [])),
        processing_details=result.get("processing_details", []),
        total_processing_time=total_time
    )

@app.post("/upload_resume", response_model=ReportResponse)
async def upload_resume(job_title: str, file: UploadFile = File(...)):
    start_time = time.time()
    
    # 解析简历
    resume_text = parse_resume(file)
    
    # 构建状态
    state = {
        "job_title": job_title,
        "resume_text": resume_text,
        "processing_details": []
    }
    
    # 执行多Agent流程
    result = agent_graph.invoke(state)
    final_report = result.get("final_report", {})
    
    # 计算总处理时间
    total_time = time.time() - start_time
    
    return ReportResponse(
        match_score=final_report.get("match_score", 50),
        strengths=final_report.get("strengths", []),
        gaps=final_report.get("gaps", []),
        suggestions=final_report.get("suggestions", []),
        detailed_report=final_report.get("detailed_report", "生成报告失败"),
        processing_details=result.get("processing_details", []),
        total_processing_time=total_time
    )

@app.get("/health")
async def health():
    return {"status": "ok", "message": "AI简历智能助手运行正常"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)