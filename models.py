from datetime import datetime



class Entry:
    def __init__(self, id, entry_type, title, scheduled_date, notes):
        self.id = id
        self.entry_type = entry_type
        self.title = title
        self.scheduled_date = scheduled_date
        self.notes = notes
        self.created_at = datetime.now()
    
    def __repr__(self):
        return f"Entry(id={self.id}, entry_type={self.entry_type}, title={self.title}, scheduled_date={self.scheduled_date})"
    
    def save(self, cursor):
        cursor.execute(
            "INSERT INTO entries (entry_type, title, scheduled_date, notes, created_at)  VALUES (%s, %s, %s, %s, %s)",
            (self.entry_type, self.title, self.scheduled_date, self.notes, self.created_at)
        )
        new_id = cursor.lastrowid
        self.id = new_id



class JobApplication(Entry):
    def __init__(self, id, entry_type, title, scheduled_date, notes, company, role, status, job_link, cv_version_id):
        super().__init__(id, entry_type, title, scheduled_date, notes)
        self.company = company
        self.role = role
        self.status = status
        self.job_link = job_link
        self.cv_version_id = cv_version_id

    def __repr__(self):
        return f"JobApplication(id={self.id}, entry_type={self.entry_type}, title={self.title}, scheduled_date={self.scheduled_date}, company={self.company}, role={self.role}, status={self.status}, job_link={self.job_link}, cv_version_id={self.cv_version_id})"

    def save(self, cursor):
        super().save(cursor=cursor)  
        cursor.execute(
            "INSERT INTO job_applications (entry_id, company, role, status, job_link, cv_version_id) VALUES (%s, %s, %s, %s, %s, %s)",
            (self.id, self.company, self.role, self.status, self.job_link, self.cv_version_id)
        )

    @staticmethod
    def get_all(cursor):
        cursor.execute("""
                       SELECT
                            j.entry_id,
                            e.title,
                            e.scheduled_date,
                            e.notes,
                            j.company,
                            j.role,
                            j.status,
                            j.job_link,
                            j.cv_version_id
                       FROM job_applications j
                       JOIN entries e
                       ON j.entry_id = e.id
                    """)
        return cursor.fetchall()



class Pattern(Entry):
    def __init__(self, id, entry_type, title, scheduled_date, notes, recurrence_rule, default_duration_min):
        super().__init__(id, entry_type, title, scheduled_date, notes)
        self.recurrence_rule = recurrence_rule
        self.default_duration_min = default_duration_min
    
    def __repr__(self):
        return f"Pattern(id={self.id}, entry_type={self.entry_type}, title={self.title}, scheduled_date={self.scheduled_date}, recurrence_rule={self.recurrence_rule}, default_duration_min={self.default_duration_min})"
    
    def save(self, cursor):
        super().save(cursor=cursor)  
        cursor.execute(
            "INSERT INTO patterns (entry_id , recurrence_rule, default_duration_min) VALUES (%s, %s, %s)",
            (self.id, self.recurrence_rule, self.default_duration_min)  
        )

    @staticmethod
    def get_all(cursor):
        cursor.execute("""
                       SELECT
                          p.entry_id,
                          e.title,
                          e.scheduled_date,
                          e.notes,
                          p.recurrence_rule,
                          p.default_duration_min
                       FROM patterns p
                       JOIN entries e 
                       ON p.entry_id = e.id
                    """)
        return cursor.fetchall()



class Task(Entry):
    def __init__(self, id, entry_type, title, scheduled_date, notes, completed, pattern_id):
        super().__init__(id, entry_type, title, scheduled_date, notes)
        self.completed = completed
        self.pattern_id = pattern_id

    def __repr__(self):
        return f"Task(id={self.id}, entry_type={self.entry_type}, title={self.title}, scheduled_date={self.scheduled_date}, completed={self.completed}, pattern_id={self.pattern_id})"
    
    def save(self, cursor):
        super().save(cursor=cursor)  
        cursor.execute(
            "INSERT INTO tasks (entry_id, completed, pattern_id) VALUES (%s, %s, %s)",
            (self.id, self.completed, self.pattern_id)    
        )
    @staticmethod
    def get_all(cursor):
        cursor.execute("""
                       SELECT
                            t.entry_id,
                            e.title,
                            e.scheduled_date,
                            e.notes,
                            t.completed,
                            t.pattern_id
                       FROM tasks t
                       JOIN entries e
                       ON t.entry_id = e.id
                    """)
        return cursor.fetchall()



class JournalEntry(Entry):
    def __init__(self, id, entry_type, title, scheduled_date, notes, content, mood):
        super().__init__(id, entry_type, title, scheduled_date, notes)
        self.content = content
        self.mood = mood
       
    def __repr__(self):
        return f"JournalEntry(id={self.id}, entry_type={self.entry_type}, title={self.title}, scheduled_date={self.scheduled_date}, content={self.content}, mood={self.mood})"

    def save(self, cursor):
        super().save(cursor=cursor)  
        cursor.execute(
            "INSERT INTO journal_entries (entry_id, content, mood) VALUES (%s, %s, %s)",
            (self.id, self.content, self.mood)    
        )
    
    @staticmethod
    def get_all(cursor):
        cursor.execute("""
                       SELECT
                            j.entry_id,
                            e.title,
                            e.scheduled_date,
                            e.notes,
                            j.content,
                            j.mood
                       FROM journal_entries j
                       JOIN entries e
                       ON j.entry_id = e.id
                    """)
        return cursor.fetchall()



class CVVersion:
    def __init__(self, id, filename, notes):
        self.id = id
        self.filename = filename
        self.notes = notes
        self.created_at = datetime.now()
    
    def __repr__(self):
        return f"CVVersion(id={self.id}, filename={self.filename}, notes={self.notes}, created_at={self.created_at})"

    def save(self, cursor):
        cursor.execute(
            "INSERT INTO cv_versions (filename, notes, created_at) VALUES (%s, %s, %s)",
            (self.filename, self.notes, self.created_at)
        )
        new_id = cursor.lastrowid
        self.id = new_id

    @staticmethod
    def get_all(cursor):
        cursor.execute("SELECT id, filename  FROM cv_versions")
        return cursor.fetchall()




