# QualGent Job Orchestrator

## Overview
CLI and backend to queue and run AppWright tests across devices. Jobs are grouped by app version and scheduled efficiently.

## Architecture
- `backend/`: FastAPI app with in-memory store
- `cli/`: Typer-based CLI client
- Queues jobs by `app_version_id`
- Schedules based on available devices and priorities

![Architecture Diagram](./docs/architecture.png)  # Optional

## Features
- Submit jobs with org/app/test
- Track job status
- Simulate retry/failure
- Prioritize jobs
- GitHub Actions integration

## Run Locally

```bash
uvicorn backend.main:app --reload
python -m cli.qgjob submit qualgent xyz123 tests/onboarding.spec.js
