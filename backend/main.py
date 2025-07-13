from fastapi import FastAPI, HTTPException, BackgroundTasks
from backend.models import JobCreate, Job
from backend.scheduler import queue_job, get_job, update_job_status
import asyncio
import random

app = FastAPI()

async def simulate_job(job_id: str):
    await asyncio.sleep(2)
    update_job_status(job_id, "running")
    await asyncio.sleep(random.randint(3, 7))
    final_status = random.choices(["completed", "failed"], weights=[0.85, 0.15])[0]
    update_job_status(job_id, final_status)

@app.post("/jobs", response_model=Job)
async def submit_job(job: JobCreate, background_tasks: BackgroundTasks):
    job_obj = queue_job(job)
    background_tasks.add_task(simulate_job, job_obj.job_id)
    return job_obj

@app.get("/jobs/{job_id}", response_model=Job)
def check_status(job_id: str):
    job = get_job(job_id)
    if job:
        return job
    raise HTTPException(status_code=404, detail="Job not found")
