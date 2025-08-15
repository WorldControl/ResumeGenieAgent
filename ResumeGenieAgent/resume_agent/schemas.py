from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from enum import Enum


class ProcessStatus(str, Enum):
    PENDING = "pending"
    COLLECTING_DATA = "collecting_data"
    ANALYZING_JOBS = "analyzing_jobs"
    MATCHING_RESUME = "matching_resume"
    GENERATING_REPORT = "generating_report"
    COMPLETED = "completed"
    FAILED = "failed"


class ProcessingStep(BaseModel):
    step_name: str
    status: ProcessStatus
    message: str
    details: Optional[Dict[str, Any]] = None
    execution_time: Optional[float] = None


class JobSearchRequest(BaseModel):
    job_title: str
    location: Optional[str] = "全国"


class ResumeUploadRequest(BaseModel):
    job_title: str


class JobData(BaseModel):
    title: str
    company: str
    salary: str
    requirements: str
    responsibilities: str


class ResumeData(BaseModel):
    name: str
    education: str
    experience: str
    skills: List[str]
    projects: str


class AnalyzeRequest(BaseModel):
    resume_text: str = Field(..., description="Raw resume text content")
    job_url: Optional[str] = Field(None, description="URL to the job posting")
    job_text: Optional[str] = Field(None, description="Raw job posting text")


class AnalyzeResponse(BaseModel):
    job_data: Dict[str, Any]
    analysis: Dict[str, Any]
    match: Dict[str, Any]
    report: str


class ReportResponse(BaseModel):
    match_score: int
    strengths: List[str]
    gaps: List[str]
    suggestions: List[str]
    detailed_report: str
    processing_details: List[ProcessingStep]
    total_processing_time: float


class JobSearchResponse(BaseModel):
    jobs: List[Dict[str, Any]]
    total_count: int
    processing_details: List[ProcessingStep]
    total_processing_time: float