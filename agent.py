import anthropic
import config


client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

def get_weather(city):
    return f"It's sunny and 25°C in {city}."

weather_tool = {
    "name": "get_weather",
    "description": "Get the current weather for a given city.",
    "input_schema": {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "The name of the city to get the weather for."}
        },
        "required": ["city"]
    }
}


messages = [
    {"role": "user", "content": "What's the weather like in Tel Aviv?"}
]

round_num = 1
while True:
    print(f"\n--- Round {round_num}: sending {len(messages)} message(s) to the model ---")

    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        tools=[weather_tool],
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
            result = get_weather(**block.input)
            print(f"Real function returned: {result}")
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result
            })

    messages.append({"role": "user", "content": tool_results})
    round_num += 1


