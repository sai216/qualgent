import requests

API_URL = "http://localhost:8000"

def submit_job(payload):
    res = requests.post(f"{API_URL}/jobs", json=payload)
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception(f"Failed to submit job: {res.status_code} {res.text}")

def get_status(job_id):
    res = requests.get(f"{API_URL}/jobs/{job_id}")
    if res.status_code == 200:
        return res.json()
    else:
        raise Exception(f"Failed to get status: {res.status_code} {res.text}")
