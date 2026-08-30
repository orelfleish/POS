import anthropic
import config
import database
import models
from bs4 import BeautifulSoup
import requests
import json
from abc import ABC, abstractmethod


client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

saved_count = 0


class JobSource(ABC):
    @abstractmethod
    def search(self, keywords, location=""):
        pass

class JoobleJobSource(JobSource):
    def search(self, keywords, location=""):
        response = requests.post(
            f"https://jooble.org/api/{config.JOOBLE_API_KEY}",
            json={"keywords": keywords, "location": location}
        )
        jobs = response.json().get("jobs", [])
        remote_jobs = filter_remote(jobs)
        slimmed = slim_jobs(remote_jobs)
        return slimmed[:10]  # Return only the first 10 results


# save_suggestion function to save a job suggestion to the database
def save_suggestion(company, role, description, requirements, level, match_score, job_link=None, reasoning=None, source=None, connection=None):
    global saved_count
    if saved_count >= 5:
        return "Maximum number of suggestions saved in this session (5) has been reached. Not saved."
    
    own_connection = connection is None
    if own_connection:       
        connection = database.get_db_connection()
    cursor = connection.cursor()

    try:
        suggestion = models.SuggestedJob(
            None, company, role, description, requirements, level, "unreviewed", match_score, job_link, reasoning, source
        )

        if models.SuggestedJob.already_suggested(cursor, company, role):
            return f"Suggestion for {role} at {company} already exists. Not saved."

        if match_score < 7:
            return f"Suggestion for {role} at {company} has a match score of {match_score}, which is below the threshold. Not saved."
        

        suggestion.save(cursor)
        connection.commit()
        
        saved_count += 1

        return f"Saved suggestion: {role} at {company}"

    finally:
        cursor.close()
        if own_connection:
            connection.close()

    
   
# filter_remote function to filter out non-remote jobs from a list of job postings
def filter_remote(jobs):
    return [job for job in jobs if "remote" in job.get("location", "").lower()]   

# clean_snippet function to clean HTML snippets from job postings
def clean_snippet(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text(separator=" ", strip=True)

# slim_jobs function to return a simplified list of job postings with only relevant fields
def slim_jobs(jobs):
    return [
        {
            "title": job.get("title"),
            "company": job.get("company"),
            "location": job.get("location"),
            "snippet": clean_snippet(job.get("snippet", "")),
            "link": job.get("link"),
        }
        for job in jobs
    ]




USER_PROFILE = """
Looking for: Backend / Software Engineer / AI Engineer roles, entry / junior level.
Skills: Python, SQL, MySQL, REST API design (FastAPI), OOP, LLM agent developement.
Preferences: Remote or Israel-based, backend-focused over full-stack.
Background: HIT Computer Science graduate.
"""

save_suggestion_tool = {
    "name": "save_suggestion",
    "description": "Save a job suggestion to the database.",
    "input_schema": {
        "type": "object",
        "properties": {
            "company": {"type": "string", "description": "The name of the company."},
            "role": {"type": "string", "description": "The role/title of the job."},
            "description": {"type": "string", "description": "A brief description of the job."},
            "requirements": {"type": "string", "description": "The requirements for the job."},
            "level": {"type": "string", 
                      "enum": ["entry", "junior", "mid", "senior"], 
                      "description": "The experience level for the job."},
            "match_score": {"type": "number", 
                            "description": "How well this job matches the user's profile, from 1 (poor fit) to 10 (excellent fit)."},        
            "job_link": {"type": ["string", "null"], 
                         "description": "(Optional) A link to the job posting."},
            "reasoning": {"type": ["string", "null"], 
                          "description": "(Optional) The reasoning behind why this job is suggested."},
            "source": {"type": ["string", "null"], 
                       "description": "(Optional) The source from where this job suggestion was found."}
        },
        "required": ["company", "role", "description", 
                     "requirements", "level", "match_score"]
    }
}

search_jobs_jooble_tool = {
    "name": "search_jobs_jooble",
    "description": "Search for jobs using the Jooble API.",
    "input_schema": {
        "type": "object",
        "properties": {
            "keywords": {"type": "string", "description": "Keywords to search for."},
            "location": {"type": ["string", "null"], 
                         "description": "(Optional) Location to filter jobs by."}
        },
        "required": ["keywords"]
    }
}

jooble_source = JoobleJobSource()

tool_functions = {
    "save_suggestion": save_suggestion,
    "search_jobs_jooble": jooble_source.search
}



if __name__ == "__main__":
    messages = [
        {"role": "user", "content": "Search for jobs that match my profile using search_jobs_jooble, then evaluate each result and save the strong matches."}
    ]

    round_num = 1
    while True:
        print(f"\n--- Round {round_num}: sending {len(messages)} message(s) to the model ---")

        response = client.messages.create(
            model="claude-sonnet-5",
            max_tokens=4096,
            system=f"You are an AI agent that helps a user find job opportunities. Evaluate job postings against this profile, and call save_suggestion only for strong matches, always including your reasoning. Only consider fully remote positions. Run at most one or two searches per session, and evaluate each batch of results concisely before deciding what to save:\n{USER_PROFILE}",
            tools=[save_suggestion_tool, search_jobs_jooble_tool],
            messages=messages
        )

        print(f"Model's stop_reason: {response.stop_reason}")
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            print("Model gave a final answer. Loop ends here.")
            for block in response.content:
                if block.type == "text":
                    print("\nFINAL ANSWER:", block.text)
            break

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                print(f"Model wants to call: {block.name}({block.input})")
                function_to_call = tool_functions.get(block.name)
                result = function_to_call(**block.input)

                print(f"Real function returned: {result}")
                content = result if isinstance(result, str) else json.dumps(result)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": content
                })

        messages.append({"role": "user", "content": tool_results})
        round_num += 1

