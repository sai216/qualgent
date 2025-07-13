store = {
    "jobs": {},  # job_id -> job object
    "queues": {},  # app_version_id -> list of job_ids
    "devices": {   # device_id -> status (available/busy)
        "emulator1": "available",
        "device1": "available",
        "browserstack1": "available",
    },
    "assignments": {},  # job_id -> device_id
}
