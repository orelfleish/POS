class Entry:
    def __init__(self, id, entry_type, title, date, notes, created_at):
        self.id = id
        self.entry_type = entry_type
        self.title = title
        self.date = date
        self.notes = notes
        self.created_at = created_at
    
    def __repr__(self):
        return f"Entry(id={self.id}, entry_type={self.entry_type}, title={self.title}, date={self.date})"
    
    def save(self, cursor):
        cursor.execute(
            "INSERT INTO entries (entry_type, title,date, notes, created_at)  VALUES (%s, %s, %s, %s, %s)",
            (self.entry_type, self.title, self.date, self.notes, self.created_at)
        )
        new_id = cursor.lastrowid
        self.id = new_id


class JobApplication(Entry):
    def __init__(self, id, entry_type, title, date, notes, created_at, company, role, date_applied, status, job_link, cv_version_id):
        super().__init__(id, entry_type, title, date, notes, created_at)
        self.company = company
        self.role = role
        self.date_applied = date_applied
        self.status = status
        self.job_link = job_link
        self.cv_version_id = cv_version_id

    def __repr__(self):
        return f"JobApplication(id={self.id}, entry_type={self.entry_type}, title={self.title}, date={self.date}, company={self.company}, role={self.role}, date_applied={self.date_applied}, status={self.status}, job_link={self.job_link}, cv_version_id={self.cv_version_id})"

    def save(self, cursor):
        super().save(cursor=cursor)  
        cursor.execute(
            "INSERT INTO job_applications (entry_id, company, role, date_applied, status, job_link, cv_version_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (self.id, self.company, self.role, self.date_applied, self.status, self.job_link, self.cv_version_id)
        )

class Pattern(Entry):
    def __init__(self, id, entry_type, title, date, notes, created_at, recurrence_rule, default_duration_min):
        super().__init__(id, entry_type, title, date, notes, created_at)
        self.recurrence_rule = recurrence_rule
        self.default_duration_min = default_duration_min
    
    def __repr__(self):
        return f"Pattern(id={self.id}, entry_type={self.entry_type}, title={self.title}, date={self.date}, recurrence_rule={self.recurrence_rule}, default_duration_min={self.default_duration_min})"
    
    def save(self, cursor):
        super().save(cursor=cursor)  
        cursor.execute(
            "INSERT INTO patterns (entry_id , recurrence_rule, default_duration_min) VALUES (%s, %s, %s)",
            (self.id, self.recurrence_rule, self.default_duration_min)  
        )

class Task(Entry):
    def __init__(self, id, entry_type, title, date, notes, created_at, day, completed, pattern_id):
        super().__init__(id, entry_type, title, date, notes, created_at)
        self.day = day
        self.completed = completed
        self.pattern_id = pattern_id

    def __repr__(self):
        return f"Task(id={self.id}, entry_type={self.entry_type}, title={self.title}, date={self.date}, day={self.day}, completed={self.completed}, pattern_id={self.pattern_id})"
    
    def save(self, cursor):
        super().save(cursor=cursor)  
        cursor.execute(
            "INSERT INTO tasks (entry_id, day, completed, pattern_id) VALUES (%s, %s, %s, %s)",
            (self.id, self.day, self.completed, self.pattern_id)    
        )

class JournalEntry(Entry):
    def __init__(self, id, entry_type, title, date, notes, created_at, content, mood):
        super().__init__(id, entry_type, title, date, notes, created_at)
        self.content = content
        self.mood = mood
       
    def __repr__(self):
        return f"JournalEntry(id={self.id}, entry_type={self.entry_type}, title={self.title}, date={self.date}, content={self.content}, mood={self.mood})"

    def save(self, cursor):
        super().save(cursor=cursor)  
        cursor.execute(
            "INSERT INTO journal_entries (entry_id, content, mood) VALUES (%s, %s, %s)",
            (self.id, self.content, self.mood)    
        )
        
class CVVersion:
    def __init__(self, id, filename, notes,created_at):
        self.id = id
        self.filename = filename
        self.notes = notes
        self.created_at = created_at
    
    def __repr__(self):
        return f"CVVersion(id={self.id}, filename={self.filename}, notes={self.notes}, created_at={self.created_at})"

    def save(self, cursor):
        cursor.execute(
            "INSERT INTO cv_versions (filename, notes, created_at) VALUES (%s, %s, %s)",
            (self.filename, self.notes, self.created_at)
        )
        new_id = cursor.lastrowid
        self.id = new_id






