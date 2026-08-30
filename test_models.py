from datetime import datetime
import models
from conftest import get_test_db_connection


def test_entry_init_sets_fields():
    entry = models.Entry(None, "task", "Gym", "2026-08-25", "leg day")
    assert entry.id is None
    assert entry.entry_type == "task"
    assert entry.title == "Gym"
    assert entry.scheduled_date == "2026-08-25"
    assert entry.notes == "leg day"
    assert isinstance(entry.created_at, datetime)


def test_job_application_inherits_entry_fields():
    job = models.JobApplication(
        None, "job_application", "Backend Dev", "2026-08-25", "notes",
        "Wix", "Backend Engineer", "applied", None, None
    )
    assert job.title == "Backend Dev"
    assert job.company == "Wix"
    assert job.role == "Backend Engineer"
    assert isinstance(job.created_at, datetime)


def test_job_application_save_and_cleanup():
    connection = get_test_db_connection()
    cursor = connection.cursor()

    job = models.JobApplication(
        None, "job_application", "Test Role", "2026-08-25", "notes",
        "TestCo", "Tester", "applied", None, None
    )
    job.save(cursor)
    connection.commit()
    assert job.id is not None

    cursor.execute("SELECT company FROM job_applications WHERE entry_id = %s", (job.id,))
    assert cursor.fetchone()[0] == "TestCo"

    # child table row first, then parent — the foreign key requires this order
    cursor.execute("DELETE FROM job_applications WHERE entry_id = %s", (job.id,))
    cursor.execute("DELETE FROM entries WHERE id = %s", (job.id,))
    connection.commit()
    cursor.close()
    connection.close()


def test_cv_version_save_and_get_all():
    connection = get_test_db_connection()
    cursor = connection.cursor()

    cv = models.CVVersion(None, "test_cv.pdf", "test notes")
    cv.save(cursor)
    connection.commit()

    ids = [c[0] for c in models.CVVersion.get_all(cursor)]
    assert cv.id in ids

    cursor.execute("DELETE FROM cv_versions WHERE id = %s", (cv.id,))
    connection.commit()
    cursor.close()
    connection.close()


def test_suggested_job_save_and_dedup():
    connection = get_test_db_connection()
    cursor = connection.cursor()

    # Save a suggestion to the test database
    suggestion = models.SuggestedJob(
        None, "Test Company", "Test Role", "Test Description", "Test Requirements", "Mid", "unreviewed", 8, None, None, None
    )
    suggestion.save(cursor)
    connection.commit()

    # Check the dedup function correctly finds the saved suggestion
    assert models.SuggestedJob.already_suggested(cursor, "Test Company", "Test Role") == True

    # Check that a different suggestion is not found
    assert models.SuggestedJob.already_suggested(cursor, "Another Company", "Another Role") == False

    # Clean up the test data
    cursor.execute("DELETE FROM suggested_jobs WHERE company = %s AND role = %s", ("Test Company", "Test Role"))
    connection.commit()

    cursor.close()
    connection.close()
