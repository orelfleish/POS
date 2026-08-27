import models
from agent import filter_remote, clean_snippet
from conftest import get_test_db_connection



def test_filter_remote():
    jobs = [
        {"title": "Backend Dev", "location": "Remote"},
        {"title": "Office Job", "location": "Tel Aviv"},
        {"title": "Hybrid Role", "location": "Remote (Hybrid)"},
    ]
    assert len(filter_remote(jobs)) == 2

def test_clean_snippet():
    html_snippet = "<p>This is a <strong>test</strong> snippet.</p>"
    assert clean_snippet(html_snippet) == "This is a test snippet."

def test_save_suggestion_and_dedup():
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

    # Clean up the test data
    cursor.execute("DELETE FROM suggested_jobs WHERE company = %s AND role = %s", ("Test Company", "Test Role"))
    connection.commit()

    cursor.close()
    connection.close()