import matplotlib.pyplot as plt 
import sqlite3
from datetime import datetime

conn = sqlite3.connect("life_os.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS daily_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    mood TEXT,
    study_hours REAL,
    sleep_hours REAL,
    water_intake REAL
)
""")

conn.commit()

# ---------------- ADD ENTRY ----------------
def add_entry():
    date = datetime.now().strftime("%Y-%m-%d")
    mood = input("Enter mood: ")
    study = float(input("Study hours: "))
    sleep = float(input("Sleep hours: "))
    water = float(input("Water intake (glasses): "))

    cursor.execute("""
    INSERT INTO daily_logs (date, mood, study_hours, sleep_hours, water_intake)
    VALUES (?, ?, ?, ?, ?)
    """, (date, mood, study, sleep, water))

    conn.commit()
    print("✅ Entry added successfully!")

# ---------------- VIEW ENTRIES ----------------
def view_entries():
    cursor.execute("SELECT * FROM daily_logs")
    data = cursor.fetchall()

    if data:
        print("\n--- Your Logs ---")
        for row in data:
            print(row)
    else:
        print("❌ No data found.")

# ---------------- SCORE ----------------
def calculate_score():
    cursor.execute("SELECT study_hours, sleep_hours, water_intake FROM daily_logs")
    data = cursor.fetchall()

    if not data:
        print("❌ No data found.")
        return

    total_score = 0

    for study, sleep, water in data:
        score = (study * 10) + (sleep * 5) + (water * 2)
        total_score += score

    avg_score = total_score / len(data)

    print(f"🔥 Your Average Productivity Score: {round(avg_score, 2)}")

# ---------------- SMART AI SUGGESTIONS ----------------
def give_suggestions():
    cursor.execute("""
    SELECT study_hours, sleep_hours, water_intake, mood 
    FROM daily_logs ORDER BY id DESC LIMIT 1
    """)
    data = cursor.fetchone()

    if not data:
        print("❌ No data found.")
        return

    study, sleep, water, mood = data

    print("\n🧠 --- Smart AI Suggestions ---")

    if study < 4:
        print("📚 Study is low → Increase focus time.")
    else:
        print("✅ Great study consistency!")

    if sleep < 6:
        print("😴 Sleep is low → Your brain needs rest.")
    else:
        print("✅ Sleep cycle is healthy!")

    if water < 5:
        print("💧 Drink more water → Stay hydrated.")
    else:
        print("✅ Hydration level is good!")

    if mood.lower() in ["sad", "tired", "angry"]:
        print("💙 Mood is low → Take a break, go for a walk.")
    else:
        print("😊 Mood looks positive!")

# ---------------- STREAK TRACKER ----------------
def show_streak():
    cursor.execute("SELECT COUNT(*) FROM daily_logs")
    count = cursor.fetchone()[0]

    print(f"🔥 Your Total Logged Days: {count}")

# ---------------- BEST DAY ----------------
def best_day():
    cursor.execute("""
    SELECT date, (study_hours*10 + sleep_hours*5 + water_intake*2) as score
    FROM daily_logs
    ORDER BY score DESC LIMIT 1
    """)
    data = cursor.fetchone()

    if data:
        print(f"🏆 Your Best Day: {data[0]} with score {round(data[1],2)}")
    else:
        print("❌ No data found.")

print("🚀 LIFE OS PRO STARTED 🚀")
def best_day():
    # your code
    pass

import matplotlib.pyplot as plt

def show_graph():
    cursor.execute("SELECT study_hours, sleep_hours, water_intake FROM daily_logs")
    data = cursor.fetchall()

    if not data:
        print("No data to display.")
        return

    study = [row[0] for row in data]
    sleep = [row[1] for row in data]
    water = [row[2] for row in data]

    days = list(range(1, len(data)+1))

    plt.plot(days, study, label="Study Hours")
    plt.plot(days, sleep, label="Sleep Hours")
    plt.plot(days, water, label="Water Intake")

    plt.xlabel("Days")
    plt.ylabel("Values")
    plt.title("Life OS Progress")
    plt.legend()
    plt.show()

while True:
    print("\n===== MENU =====")
    print("1. Add Entry")
    print("2. View Entries")
    print("3. Show Score")
    print("4. AI Suggestions")
    print("5. Show Streak")
    print("6. Best Day")
    print("7. Show Graph")
    print("8. Exit")

    choice = input("Enter choice: ")

    if choice == '1':
        add_entry()
    elif choice == '2':
        view_entries()
    elif choice == '3':
        calculate_score()
    elif choice == '4':
        give_suggestions()
    elif choice == '5':
        show_streak()
    elif choice == '6':
        best_day()
    elif choice == '7':
        show_graph()
    elif choice == '8':
        break
    else:
        print("❌ Invalid choice")

conn.close()
