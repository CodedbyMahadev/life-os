import sqlite3

conn = sqlite3.connect("life_os.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS daily_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mood TEXT,
    study_hours INTEGER,
    sleep_hours INTEGER,
    water_intake INTEGER
)
""")

conn.commit()

def add_entry():
    mood = input("Enter mood: ")
    study = int(input("Study hours: "))
    sleep = int(input("Sleep hours: "))
    water = int(input("Water intake (glasses): "))

    cursor.execute("INSERT INTO daily_logs (mood, study_hours, sleep_hours, water_intake) VALUES (?, ?, ?, ?)",
                   (mood, study, sleep, water))
    conn.commit()
    print("Entry added successfully!")

def view_entries():
    cursor.execute("SELECT * FROM daily_logs")
    data = cursor.fetchall()

    if data:
        for row in data:
            print(row)
    else:
        print("No data found.")

def calculate_score():
    cursor.execute("SELECT study_hours, sleep_hours, water_intake FROM daily_logs ORDER BY id DESC LIMIT 1")
    data = cursor.fetchone()

    if data:
        study, sleep, water = data
        score = (study * 10) + (sleep * 5) + (water * 2)
        print(f"Your productivity score: {score}")
    else:
        print("No data found.")

print("🔥 LIFE OS STARTED 🔥")

while True:
    print("\n1. Add Daily Entry")
    print("2. View Entries")
    print("3. Show Score")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == '1':
        add_entry()
    elif choice == '2':
        view_entries()
    elif choice == '3':
        calculate_score()
    elif choice == '4':
        print("Exiting...")
        break
    else:
        print("Invalid choice")