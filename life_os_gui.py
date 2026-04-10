import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt

conn = sqlite3.connect("life_os.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    mood TEXT,
    study INTEGER,
    sleep INTEGER,
    water INTEGER
)
""")

conn.commit()

def add_entry():
    mood = mood_entry.get()
    try:
        study = int(study_entry.get())
        sleep = int(sleep_entry.get())
        water = int(water_entry.get())
    except:
        messagebox.showerror("Error", "Enter valid numbers")
        return

    date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("INSERT INTO logs (date, mood, study, sleep, water) VALUES (?, ?, ?, ?, ?)",
                   (date, mood, study, sleep, water))
    conn.commit()

    messagebox.showinfo("Success", "Entry Added 🔥")
    update_table()

def calculate_score():
    cursor.execute("SELECT study, sleep, water FROM logs ORDER BY id DESC LIMIT 1")
    data = cursor.fetchone()

    if not data:
        return 0

    return data[0]*10 + data[1]*5 + data[2]*2

def show_ai():
    cursor.execute("SELECT study, sleep, water, mood FROM logs ORDER BY id DESC LIMIT 7")
    data = cursor.fetchall()

    if not data:
        messagebox.showinfo("AI", "No data available")
        return

    study = [d[0] for d in data]
    sleep = [d[1] for d in data]
    water = [d[2] for d in data]
    mood = [d[3] for d in data]

    avg_study = sum(study)/len(study)
    avg_sleep = sum(sleep)/len(sleep)
    avg_water = sum(water)/len(water)

    trend = study[0] - study[-1]

    msg = "🧠 LIFE ANALYZER\n\n"

    msg += "📊 Score: " + str(int(avg_study*10 + avg_sleep*5 + avg_water*2)) + "\n\n"

    if trend < 0:
        msg += "📉 You are losing consistency\n"
    else:
        msg += "📈 You are improving\n"

    if avg_study < 4:
        msg += "⚠️ Low study time\n"
    else:
        msg += "🔥 Good focus\n"

    if avg_sleep < 6:
        msg += "😴 Sleep is low\n"
    else:
        msg += "🌙 Sleep balanced\n"

    if avg_water < 5:
        msg += "💧 Drink more water\n"

    if "sad" in mood or "angry" in mood:
        msg += "🧠 Mood unstable\n"

    msg += "\n🎯 Stay consistent"

    messagebox.showinfo("AI Coach", msg)

def show_graph():
    cursor.execute("SELECT date, study FROM logs")
    data = cursor.fetchall()

    if not data:
        return

    dates = [d[0] for d in data]
    study = [d[1] for d in data]

    plt.plot(dates, study)
    plt.title("Study Trend")
    plt.xticks(rotation=45)
    plt.show()

def best_day():
    cursor.execute("SELECT date, study+sleep+water FROM logs ORDER BY (study+sleep+water) DESC LIMIT 1")
    data = cursor.fetchone()

    if data:
        messagebox.showinfo("Best Day", f"🏆 {data[0]} was your best day")

def streak():
    cursor.execute("SELECT date FROM logs ORDER BY date DESC")
    data = cursor.fetchall()

    if not data:
        return 0

    count = 1
    for i in range(1, len(data)):
        d1 = datetime.strptime(data[i-1][0], "%Y-%m-%d")
        d2 = datetime.strptime(data[i][0], "%Y-%m-%d")

        if (d1 - d2).days == 1:
            count += 1
        else:
            break

    return count

def update_table():
    for i in table.get_children():
        table.delete(i)

    cursor.execute("SELECT date, study, sleep, water FROM logs")
    for row in cursor.fetchall():
        table.insert("", "end", values=row)

root = tk.Tk()
root.title("Life OS")
root.geometry("900x500")
root.configure(bg="#0f172a")

left = tk.Frame(root, bg="#111827", width=250)
left.pack(side="left", fill="y")

right = tk.Frame(root, bg="#0f172a")
right.pack(side="right", expand=True, fill="both")

def label(text):
    tk.Label(left, text=text, bg="#111827", fg="white").pack(pady=5)

def entry():
    e = tk.Entry(left)
    e.pack()
    return e

def btn(text, cmd, color):
    tk.Button(left, text=text, command=cmd, bg=color, fg="white", width=20).pack(pady=5)

tk.Label(left, text="Life OS", bg="#111827", fg="#22d3ee", font=("Arial", 16)).pack(pady=10)

label("Mood")
mood_entry = entry()

label("Study Hours")
study_entry = entry()

label("Sleep Hours")
sleep_entry = entry()

label("Water Intake")
water_entry = entry()

btn("Add Entry", add_entry, "#22c55e")
btn("AI Analysis", show_ai, "#a855f7")
btn("Show Graph", show_graph, "#3b82f6")
btn("Best Day", best_day, "#f59e0b")

score_label = tk.Label(right, text="Score: 0", bg="#0f172a", fg="white", font=("Arial", 14))
score_label.pack()

streak_label = tk.Label(right, text="Streak: 0", bg="#0f172a", fg="white")
streak_label.pack()

from tkinter import ttk

table = ttk.Treeview(right, columns=("Date","Study","Sleep","Water"), show="headings")
for col in ("Date","Study","Sleep","Water"):
    table.heading(col, text=col)
table.pack(expand=True, fill="both")

def refresh():
    score_label.config(text="Score: " + str(calculate_score()))
    streak_label.config(text="Streak: " + str(streak()))
    update_table()
    root.after(2000, refresh)

refresh()
root.mainloop()