import typer
from cli.client import submit_job, get_status
import time

app = typer.Typer()

@app.command()
def submit(
    org_id: str = typer.Argument(..., help="Organization ID"),
    app_version_id: str = typer.Argument(..., help="App Version ID"),
    test: str = typer.Argument(..., help="Path to test file"),
    priority: int = typer.Option(1, help="Job priority"),
    target: str = typer.Option("emulator", help="Target: emulator/device/browserstack")
):
    payload = {
        "org_id": org_id,
        "app_version_id": app_version_id,
        "test_path": test,
        "priority": priority,
        "target": target
    }
    result = submit_job(payload)
    typer.echo(f"📝 Job submitted: ID = {result['job_id']}, Status = {result['status']}")

@app.command()
def status(job_id: str):
    result = get_status(job_id)
    typer.echo(f"🔍 Status for job {job_id}: {result['status']}")

@app.command()
def poll(job_id: str, interval: int = 2):
    typer.echo(f"⏳ Polling for job {job_id} every {interval} seconds...")
    while True:
        result = get_status(job_id)
        typer.echo(f"📌 Status: {result['status']}")
        if result['status'] in ["completed", "failed"]:
            break
        time.sleep(interval)
    typer.echo("✅ Done.")

if __name__ == "__main__":
    app()