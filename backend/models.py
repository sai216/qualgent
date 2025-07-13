# File: backend/models.py
from pydantic import BaseModel, Field
from typing import Optional

class JobCreate(BaseModel):
    org_id: str
    app_version_id: str
    test_path: str
    priority: int = 1
    target: str  # emulator | device | browserstack
    retries: int = Field(0, description="Number of retries attempted")

class Job(JobCreate):
    job_id: str
    status: str = "queued"
