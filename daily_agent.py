import os
import json
from datetime import datetime
import openai

# ====== CONFIGURATION ======
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set this in your shell before running
DATA_FILE = "daily_log.json"

# ====== UTILS ======
def get_today():
    return datetime.now().strftime("%Y-%m-%d")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# ====== MORNING FLOW ======
def morning_flow():
    print("\n🌞 Morning Check-In:")
    goals = input("1. What are your top 1–2 goals for today?\n> ")
    blockers = input("2. Any potential distractions or blockers?\n> ")

    return {
        "goals": goals,
        "blockers": blockers
    }

# ====== EVENING FLOW ======
def evening_flow():
    print("\n🌙 Evening Wrap-Up:")
    completed = input("1. What did you actually complete today?\n> ")
    deviations = input("2. What went differently than expected?\n> ")
    improvements = input("3. What’s one thing you’d change for tomorrow?\n> ")

    return {
        "completed": completed,
        "deviations": deviations,
        "improvements": improvements
    }

# ====== OPTIONAL LLM REFLECTION ======
def generate_reflection(morning, evening):
    prompt = f"""
You are a leadership coach helping a Meta engineering manager reflect on their day.

This morning they said:
- Goals: {morning['goals']}
- Blockers: {morning['blockers']}

This evening they said:
- Completed: {evening['completed']}
- Deviations: {evening['deviations']}
- Improvements: {evening['improvements']}

Write a short reflective summary and suggest 1 improvement for tomorrow.
"""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a concise leadership coach."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

# ====== MAIN ======
def main():
    print("📘 Daily Impact Co-Pilot\n")
    data = load_data()
    today = get_today()
    if today not in data:
        data[today] = {}

    while True:
        mode = input("\nWhat do you want to do?\n[M] Morning Check-In\n[E] Evening Wrap-Up\n[Q] Quit\n> ").lower()
        if mode == "m":
            data[today]["morning"] = morning_flow()
            save_data(data)
            print("✅ Morning check-in saved.")
        elif mode == "e":
            data[today]["evening"] = evening_flow()
            save_data(data)
            print("✅ Evening wrap-up saved.")
            if "morning" in data[today]:
                reflection = generate_reflection(data[today]["morning"], data[today]["evening"])
                print("\n🧠 Reflection Summary:\n" + reflection)
        elif mode == "q":
            break
        else:
            print("Please choose M, E, or Q.")

if __name__ == "__main__":
    main()