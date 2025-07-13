# File: backend/scheduler.py
from uuid import uuid4
from backend.store import store
from backend.models import Job
import asyncio
import threading
import random

def assign_device(target: str, app_version_id: str):
    """
    Assign a device based on the target type and group jobs by app_version_id.
    Reuse device if app_version_id already has an assigned device.
    """
    for job_id in store["queues"].get(app_version_id, []):
        if job_id in store["assignments"]:
            return store["assignments"][job_id]

    for device_id, status in store["devices"].items():
        if device_id.startswith(target) and status == "available":
            store["devices"][device_id] = "busy"
            return device_id
    return None

def queue_job(job_data):
    """
    Enqueue a job, assign a device if available, and store the job.
    """
    job_id = str(uuid4())
    job = Job(job_id=job_id, **job_data.dict())
    store["jobs"][job_id] = job
    store["queues"].setdefault(job.app_version_id, []).append(job_id)
    assigned_device = assign_device(job.target, job.app_version_id)
    if assigned_device:
        store["assignments"][job_id] = assigned_device
    return job

def get_job(job_id):
    return store["jobs"].get(job_id)

def update_job_status(job_id: str, status: str):
    job = store["jobs"].get(job_id)
    if job:
        job.status = status
        return job
    return None

async def run_job_async(job_id):
    job = store["jobs"][job_id]
    job.status = "running"
    for attempt in range(3):
        await asyncio.sleep(2 + attempt)
        if random.random() < 0.85:
            job.status = "completed"
            break
        else:
            job.retries += 1
            job.status = "retrying"
    else:
        job.status = "failed"

    device_id = store["assignments"].get(job_id)
    if device_id:
        store["devices"][device_id] = "available"

def run_job(job_id):
    asyncio.run(run_job_async(job_id))

def start_job_runner(job_id):
    threading.Thread(target=run_job, args=(job_id,), daemon=True).start()

def process_queue():
    sorted_jobs = sorted(
        [(job_id, job) for job_id, job in store["jobs"].items() if job.status == "queued"],
        key=lambda x: x[1].priority
    )
    for job_id, job in sorted_jobs:
        if job_id in store["assignments"]:
            start_job_runner(job_id)
