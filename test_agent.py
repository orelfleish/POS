from agent import filter_remote


def test_filter_remote():
    jobs = [
        {"title": "Backend Dev", "location": "Remote"},
        {"title": "Office Job", "location": "Tel Aviv"},
        {"title": "Hybrid Role", "location": "Remote (Hybrid)"},
    ]
    assert len(filter_remote(jobs)) == 2