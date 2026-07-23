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

#get all job applications
@app.get("/job-applications")
def get_job_applications():
    connection = database.get_db_connection()
    cursor = connection.cursor()

    job_applications = models.JobApplication.get_all(cursor)

    cursor.close()
    connection.close()

    return {"job_applications": [{"entry_id": job[0], "company": job[1], "role": job[2], "status": job[3], "job_link": job[4], "cv_version_id": job[5]} for job in job_applications]}


#get all cv versions
@app.get("/cv-versions")
def get_cv_versions():
    connection = database.get_db_connection()
    cursor = connection.cursor()

    cv_versions = models.CVVersion.get_all(cursor)

    cursor.close()
    connection.close()

    return {"cv_versions": [{"id": cv[0], "filename": cv[1]} for cv in cv_versions]}



#schema for pattern request
class PatternRequest(BaseModel):
    title: str
    scheduled_date: str
    notes: str
    recurrence_rule: str
    default_duration_min: int

#create a new pattern
@app.post("/patterns")
def create_pattern(request: PatternRequest):
    connection = database.get_db_connection()
    cursor = connection.cursor()

    pattern = models.Pattern(
        None,
        "pattern",
        request.title,
        request.scheduled_date,
        request.notes,
        request.recurrence_rule,
        request.default_duration_min    
    )
    pattern.save(cursor)
    connection.commit()

    cursor.close()
    connection.close()

    return {"message": "Pattern added successfully.", "id": pattern.id}

#get all patterns
@app.get("/patterns")
def get_patterns():
    connection = database.get_db_connection()
    cursor = connection.cursor()

    patterns = models.Pattern.get_all(cursor)

    cursor.close()
    connection.close()

    return {"patterns": [{"entry_id": pattern[0], "recurrence_rule": pattern[1], "default_duration_min": pattern[2]} for pattern in patterns]}



#schema for task request
class TaskRequest(BaseModel):
    title: str
    scheduled_date: str
    notes: str
    completed: bool
    pattern_id: int | None = None

#create a new task
@app.post("/tasks")
def create_task(request: TaskRequest):
    connection = database.get_db_connection()
    cursor = connection.cursor()

    task = models.Task(
        None,
        "task",
        request.title,
        request.scheduled_date,
        request.notes,
        request.completed,
        request.pattern_id
    )
    task.save(cursor)
    connection.commit()

    cursor.close()
    connection.close()

    return {"message": "Task added successfully.", "id": task.id}

#get all tasks
@app.get("/tasks")
def get_tasks():
    connection = database.get_db_connection()
    cursor = connection.cursor()

    tasks = models.Task.get_all(cursor)

    cursor.close()
    connection.close()

    return {"tasks": [{"entry_id": task[0], "completed": task[1], "pattern_id": task[2]} for task in tasks]}


#schema for journal entry request
class JournalEntryRequest(BaseModel):
    title: str
    scheduled_date: str
    notes: str
    content: str
    mood: str

#create a new journal entry
@app.post("/journal-entries")
def create_journal_entry(request: JournalEntryRequest):
    connection = database.get_db_connection()
    cursor = connection.cursor()

    journal_entry = models.JournalEntry(
        None,
        "journal",
        request.title,
        request.scheduled_date,
        request.notes,
        request.content,
        request.mood
    )
    journal_entry.save(cursor)
    connection.commit()

    cursor.close()
    connection.close()

    return {"message": "Journal entry added successfully.", "id": journal_entry.id}

#get all journal entries
@app.get("/journal-entries")
def get_journal_entries():
    connection = database.get_db_connection()
    cursor = connection.cursor()

    journal_entries = models.JournalEntry.get_all(cursor)

    cursor.close()
    connection.close()

    return {"journal_entries": [{"entry_id": entry[0], "content": entry[1], "mood": entry[2]} for entry in journal_entries]}
