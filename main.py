import models
import database
import secrets





connection = database.get_db_connection()
cursor = connection.cursor()

while True:
    print("\nSelect an option:")
    print("\n 1. Add Job Application \n 2. Add Pattern \n 3. Add Task \n 4. Add Journal Entry \n 5. Exit")
    choice = input("Enter your choice (1-5): ")
    if choice == "1":
        # Add Job Application
        title = input("Enter title: ")
        scheduled_date = input("Enter scheduled date (YYYY-MM-DD): ")
        notes = input("Enter notes: ")
        company = input("Enter company: ")
        role = input("Enter role: ")
        status = input("Enter status: ")
        job_link = input("Enter job link: ")
        print("Available CV versions:")
        cv_versions = models.CVVersion.get_all(cursor)
        for cv in cv_versions:
            print(f"ID: {cv[0]}, Filename: {cv[1]}")
        cv_id = input("Enter CV version ID from the list above: ")  # something to notice is "input validation topic"
        cv_version_id = int(cv_id) if cv_id else None
        
        
        job_application = models.JobApplication(None, "job_application", title, scheduled_date, notes, company, role, status, job_link, cv_version_id)
        job_application.save(cursor)
        connection.commit()
        print("Job application added successfully.")
   
    elif choice == "2":
        # Add Pattern
        title = input("Enter title: ")
        scheduled_date = input("Enter scheduled date (YYYY-MM-DD): ")
        notes = input("Enter notes: ")
        recurrence_rule = input("Enter recurrence rule (e.g., FREQ=DAILY;INTERVAL=1): ")
        default_duration_min = int(input("Enter default duration in minutes: "))
        
        pattern = models.Pattern(None, "pattern", title, scheduled_date, notes, recurrence_rule, default_duration_min)
        pattern.save(cursor)
        connection.commit()
        print("Pattern added successfully.")
    
    elif choice == "3":
        # Add Task
        title = input("Enter title: ")
        scheduled_date = input("Enter scheduled date (YYYY-MM-DD): ")
        notes = input("Enter notes: ")
        completed = input("Is the task completed? (yes/no): ").lower() == "yes"
        print("Available Patterns:")
        patterns = models.Pattern.get_all(cursor)
        for pattern in patterns:
            print(f"ID: {pattern[0]}, Recurrence Rule: {pattern[1]}, Default Duration: {pattern[2]} minutes")
        pattern_id_input = input("Enter Pattern ID from the list above (or leave blank): ")
        pattern_id = int(pattern_id_input) if pattern_id_input else None
        
        
        task = models.Task(None, "task", title, scheduled_date, notes, completed, pattern_id)
        task.save(cursor)
        connection.commit()
        print("Task added successfully.")

    elif choice == "4":
        # Add Journal Entry
        title = input("Enter title: ")
        scheduled_date = input("Enter scheduled date (YYYY-MM-DD): ")
        notes = input("Enter notes: ")
        content = input("Enter content: ")
        mood = input("Enter mood: ")
        
        journal_entry = models.JournalEntry(None, "journal", title, scheduled_date, notes, content, mood)
        journal_entry.save(cursor)
        connection.commit()
        print("Journal entry added successfully.")
   
    elif choice == "5":
        connection.commit()
        print("Exiting...")
        break


print(secrets.token_hex(32))  # Generates a random 32-byte hex string for API key