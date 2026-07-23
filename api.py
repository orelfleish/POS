import models
import database
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#root endpoint to check if the API is running
@app.get("/")
def read_root():
    return {"message": "API is running."}

#schema for job application request
class JobApplicationRequest(BaseModel):
    title: str
    scheduled_date: str
    notes: str
    company: str
    role: str
    status: str
    job_link: str
    cv_version_id: int | None = None


#create a new job application
@app.post("/job-applications")
def create_job_application(request: JobApplicationRequest):
    connection = database.get_db_connection()
    cursor = connection.cursor()

    job = models.JobApplication(
        None,
        "job_application",
        request.title,
        request.scheduled_date,
        request.notes,
        request.company,
        request.role,
        request.status,
        request.job_link,
        request.cv_version_id
    )
    job.save(cursor)
    connection.commit()

    cursor.close()
    connection.close()

    return {"message": "Job application added successfully.", "id": job.id}

@app.get("/cv-versions")
def get_cv_versions():
    connection = database.get_db_connection()
    cursor = connection.cursor()

    cv_versions = models.CVVersion.get_all(cursor)

    cursor.close()
    connection.close()

    return {"cv_versions": [{"id": cv[0], "filename": cv[1]} for cv in cv_versions]}