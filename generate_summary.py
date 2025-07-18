import json
import openai
import os

# Make sure you set your OpenAI API key as an environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Step 1: Load the reflections
with open("daily_log.json", "r") as file:
    log = json.load(file)

reflections = log.get("2025-07-17", {}).get("reflection", [])

if not reflections:
    print("No reflections found for 2025-07-17.")
    print("Reflections:", reflections)
    exit()

# Step 2: Build prompt
prompt = (
    "Summarize the following reflections into a single concise sentence:\n\n"
    + "\n".join(f"- {item}" for item in reflections)
)

# Step 3: Call OpenAI
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.7,
    max_tokens=50,
)

# Step 4: Extract and show the result
summary = response["choices"][0]["message"]["content"]
print("\n📝 Daily Summary for 2025-07-17:\n" + summary)
# Step 5: Save the summary back to the log
log["2025-07-17"]["summary"] = summary

# Step 6: Save the updated log back to the file
with open("daily_log.json", "w") as file:
    json.dump(log, file, indent=4)