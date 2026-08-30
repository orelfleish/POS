import models
import agent
from conftest import get_test_db_connection



def test_filter_remote():
    jobs = [
        {"title": "Backend Dev", "location": "Remote"},
        {"title": "Office Job", "location": "Tel Aviv"},
        {"title": "Hybrid Role", "location": "Remote (Hybrid)"},
    ]
    assert len(agent.filter_remote(jobs)) == 2

def test_clean_snippet():
    html_snippet = "<p>This is a <strong>test</strong> snippet.</p>"
    assert agent.clean_snippet(html_snippet) == "This is a test snippet."


def test_slim_jobs():
    jobs = [
        {
            "title": "Backend Dev",
            "company": "Tech Co",
            "location": "Remote",
            "snippet": "<p>Great opportunity!</p>",
            "link": "http://example.com/job1"
        },
        {
            "title": "Frontend Dev",
            "company": "Web Co",
            "location": "Tel Aviv",
            "snippet": "<p>Exciting role!</p>",
            "link": "http://example.com/job2"
        }
    ]
    slimmed_jobs = agent.slim_jobs(jobs)
    assert len(slimmed_jobs) == 2
    assert slimmed_jobs[0]["title"] == "Backend Dev"
    assert slimmed_jobs[0]["company"] == "Tech Co"
    assert slimmed_jobs[0]["location"] == "Remote"
    assert slimmed_jobs[0]["snippet"] == "Great opportunity!"
    assert slimmed_jobs[0]["link"] == "http://example.com/job1"



def test_save_suggestion_reuses_caller_connection():
    agent.saved_count = 0
    connection = get_test_db_connection()

    result = agent.save_suggestion(
        "ProofCo", "Proof Role", "desc", "reqs", "junior", 8,
        connection=connection
    )
    assert "Saved suggestion" in result

    # if save_suggestion had closed OUR connection, this next line would crash
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM suggested_jobs WHERE company = %s", ("ProofCo",))
    row = cursor.fetchone()
    assert row is not None

    # cleanup — this test owns the connection, so it's responsible for closing it
    cursor.execute("DELETE FROM suggested_jobs WHERE company = %s", ("ProofCo",))
    connection.commit()
    cursor.close()
    connection.close()