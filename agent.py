import anthropic
import config
import database
import models

client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)


def save_suggestion(company, role, description, requirements, level, job_link=None, reasoning=None, source=None):
    connection = database.get_db_connection()
    cursor = connection.cursor()

    suggestion = models.SuggestedJob(
        None, company, role, description, requirements, level, "unreviewed", job_link, reasoning, source
    )
    suggestion.save(cursor)
    connection.commit()

    cursor.close()
    connection.close()

    return f"Saved suggestion: {role} at {company}"
   
   



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
            "job_link": {"type": ["string", "null"], 
                         "description": "(Optional) A link to the job posting."},
            "reasoning": {"type": ["string", "null"], 
                          "description": "(Optional) The reasoning behind why this job is suggested."},
            "source": {"type": ["string", "null"], 
                       "description": "(Optional) The source from where this job suggestion was found."}
        },
        "required": ["company", "role", "description", 
                     "requirements", "level"]
    }
}




messages = [
    {"role": "user", "content": """Here's a job posting — evaluate it:

    Company: Wix
    Role: Junior Backend Engineer
    Description: Join our platform team building scalable APIs used by millions.
    Requirements: Python, SQL, REST API experience, understanding of OOP. 0-2 years experience welcome."""}
]




round_num = 1
while True:
    print(f"\n--- Round {round_num}: sending {len(messages)} message(s) to the model ---")

    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        system=f"You are an AI agent that helps a user find job opportunities. Evaluate job postings against this profile, and call save_suggestion only for strong matches, always including your reasoning:\n{USER_PROFILE}",
        tools=[save_suggestion_tool],
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
            result = save_suggestion(**block.input)
            print(f"Real function returned: {result}")
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result
            })

    messages.append({"role": "user", "content": tool_results})
    round_num += 1

