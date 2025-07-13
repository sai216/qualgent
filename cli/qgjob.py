import typer
import json
import time
import sys
from cli.client import submit_job, get_status

app = typer.Typer()

@app.command()
def submit(
    org_id: str = typer.Argument(..., help="Organization ID"),
    app_version_id: str = typer.Argument(..., help="App Version ID"),
    test: str = typer.Argument(..., help="Path to test file"),
    priority: int = typer.Option(1, help="Job priority"),
    target: str = typer.Option("emulator", help="Target device: emulator, device, or browserstack")
):
    """
    Submit a test job to the backend service.
    """
    payload = {
        "org_id": org_id,
        "app_version_id": app_version_id,
        "test_path": test,
        "priority": priority,
        "target": target
    }
    result = submit_job(payload)
    typer.echo(json.dumps(result))


@app.command()
def status(job_id: str):
    """
    Check status of a submitted job by job_id.
    """
    result = get_status(job_id)
    typer.echo(f"🔍 Status for job {job_id}: {result['status']}")


@app.command()
def poll(job_id: str, interval: int = 2):
    """
    Poll the job status repeatedly until it is completed or failed.
    If job fails, exit with status code 1 to fail the CI pipeline.
    """
    typer.echo(f"⏳ Polling for job {job_id} every {interval} seconds...")
    while True:
        result = get_status(job_id)
        typer.echo(f"📌 Status: {result['status']}")
        if result['status'] in ["completed", "failed"]:
            break
        time.sleep(interval)

    if result['status'] == "failed":
        typer.echo("❌ Job failed.")
        sys.exit(1)

    typer.echo("✅ Job completed successfully.")

if __name__ == "__main__":
    app()
