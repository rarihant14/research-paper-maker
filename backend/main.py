
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
import uuid

from .workflow import run_workflow
from .Jobs import JOBS


app = FastAPI(title="Research Paper Maker API")

class GenerateRequest(BaseModel):
    topic: str
    style: str = "academic"
    words: int = 1000

@app.post("/research/generate")
async def generate(req: GenerateRequest, background_tasks: BackgroundTasks):
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {"status": "queued"}
    background_tasks.add_task(run_workflow, job_id, req.topic, req.style, req.words)
    return {"job_id": job_id, "status": "queued"}

@app.get("/research/status/{job_id}")
def status(job_id: str):
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/research/download/{job_id}")
def download(job_id: str):
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.get("status") != "completed":
        raise HTTPException(status_code=400, detail="Job not completed")
    return {"paper": job.get("output_plain", "")}
