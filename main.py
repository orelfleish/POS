import models
import database





# cv_version = models.CVVersion(None, "cv_v1.pdf", "Initial version of my CV.", "2024-06-01 08:00:00")
# cv_version.save(cursor)

# job = models.JobApplication(None,"job_application", "Software Engineer", "2024-06-01", "Applied for a software engineer position.", "2024-06-01 10:00:00", "Tech Company", "Software Engineer", "2024-06-01", "applied", "https://techcompany.com/jobs/12345", cv_version.id)
# job.save(cursor)

# pattern = models.Pattern(None, "pattern", "Daily Standup", "2024-06-01", "Daily team standup meeting.", "2024-06-01 09:00:00", "FREQ=DAILY;INTERVAL=1", 15)
# pattern.save(cursor)

# task = models.Task(None, "task", "Submit weekly report", "2024-06-03", "Don't forget attachments", "2024-06-01", "2024-06-03", False, pattern.id)
# task.save(cursor)

# journal = models.JournalEntry(None, "journal", "Reflections", "2024-06-01", None, "2024-06-01", "Good focus today, finished two interviews.", "productive")
# journal.save(cursor)    





connection = database.get_db_connection()
cursor = connection.cursor()

while True:
    print("\nSelect an option:")
    print("\n 1. Add Job Application \n 2. Add Pattern \n 3. Add Task \n 4. Add Journal Entry \n 5. Exit")
    choice = input("Enter your choice (1-5): ")
    if choice == "1":
        # Add Job Application
        title = input("Enter title: ")
        date = input("Enter date (YYYY-MM-DD): ")
        notes = input("Enter notes: ")
        company = input("Enter company: ")
        role = input("Enter role: ")
        date_applied = input("Enter date applied (YYYY-MM-DD): ")
        status = input("Enter status: ")
        job_link = input("Enter job link: ")
        
        
        job_application = models.JobApplication(None, "job_application", title, date, notes, "2024-06-01 10:00:00", company, role, date_applied, status, job_link, cv_version_id = None)
        job_application.save(cursor)
        connection.commit()
        print("Job application added successfully.")
   
    elif choice == "2":
        # Add Pattern
        title = input("Enter title: ")
        date = input("Enter date (YYYY-MM-DD): ")
        notes = input("Enter notes: ")
        recurrence_rule = input("Enter recurrence rule (e.g., FREQ=DAILY;INTERVAL=1): ")
        default_duration_min = int(input("Enter default duration in minutes: "))
        
        pattern = models.Pattern(None, "pattern", title, date, notes, "2024-06-01 09:00:00", recurrence_rule, default_duration_min)
        pattern.save(cursor)
        connection.commit()
        print("Pattern added successfully.")
        
   
    elif choice == "5":
        connection.commit()
        print("Exiting...")
        break





