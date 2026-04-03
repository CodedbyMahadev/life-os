import sqlite3
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# DB setup
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

# -------- FUNCTIONS --------

def add_entry():
    try:
        mood = mood_entry.get()
        study = int(study_entry.get())
        sleep = int(sleep_entry.get())
        water = int(water_entry.get())

        cursor.execute("INSERT INTO daily_logs (mood, study_hours, sleep_hours, water_intake) VALUES (?, ?, ?, ?)",
                       (mood, study, sleep, water))
        conn.commit()

        messagebox.showinfo("Success", "Entry Added 🚀")
        clear_fields()

    except:
        messagebox.showerror("Error", "Enter valid data!")

def clear_fields():
    mood_entry.delete(0, tk.END)
    study_entry.delete(0, tk.END)
    sleep_entry.delete(0, tk.END)
    water_entry.delete(0, tk.END)

def show_history():
    cursor.execute("SELECT * FROM daily_logs")
    data = cursor.fetchall()

    history_window = tk.Toplevel(root)
    history_window.title("History")

    text = tk.Text(history_window, width=60, height=20)
    text.pack()

    if data:
        for row in data:
            text.insert(tk.END, f"{row}\n")
    else:
        text.insert(tk.END, "No data found.")

def show_graph():
    cursor.execute("SELECT study_hours, sleep_hours, water_intake FROM daily_logs")
    data = cursor.fetchall()

    if not data:
        messagebox.showerror("Error", "No data!")
        return

    study = [i[0] for i in data]
    sleep = [i[1] for i in data]
    water = [i[2] for i in data]
    days = list(range(1, len(data)+1))

    plt.plot(days, study, label="Study")
    plt.plot(days, sleep, label="Sleep")
    plt.plot(days, water, label="Water")

    plt.legend()
    plt.title("Life OS Analytics 📊")
    plt.xlabel("Days")
    plt.ylabel("Values")
    plt.show()

def show_score():
    cursor.execute("SELECT study_hours, sleep_hours, water_intake FROM daily_logs ORDER BY id DESC LIMIT 1")
    data = cursor.fetchone()

    if data:
        study, sleep, water = data
        score = (study*10) + (sleep*5) + (water*2)

        msg = f"🔥 Productivity Score: {score}\n\n"

        if score > 100:
            msg += "Excellent 🚀"
        elif score > 60:
            msg += "Good 👍"
        else:
            msg += "Needs Improvement ⚡"

        messagebox.showinfo("Score", msg)
    else:
        messagebox.showerror("Error", "No data!")

def ai_suggestions():
    cursor.execute("SELECT study_hours, sleep_hours, water_intake FROM daily_logs ORDER BY id DESC LIMIT 1")
    data = cursor.fetchone()

    if not data:
        messagebox.showerror("Error", "No data!")
        return

    study, sleep, water = data
    msg = "🤖 Smart Suggestions:\n\n"

    if study < 4:
        msg += "📚 Increase study time\n"
    else:
        msg += "✅ Study is good\n"

    if sleep < 6:
        msg += "😴 Sleep more\n"
    else:
        msg += "✅ Sleep is balanced\n"

    if water < 5:
        msg += "💧 Drink more water\n"
    else:
        msg += "✅ Hydration good\n"

    messagebox.showinfo("AI Coach", msg)

def best_day():
    cursor.execute("SELECT study_hours, sleep_hours, water_intake FROM daily_logs")
    data = cursor.fetchall()

    if not data:
        messagebox.showerror("Error", "No data!")
        return

    scores = [(i[0]*10 + i[1]*5 + i[2]*2) for i in data]
    best = max(scores)
    day = scores.index(best) + 1

    messagebox.showinfo("Best Day", f"🏆 Your best day is Day {day} with score {best}")

# -------- UI --------

root = tk.Tk()
root.title("🔥 LIFE OS PRO")
root.geometry("400x500")

title = tk.Label(root, text="LIFE OS DASHBOARD", font=("Arial", 16, "bold"))
title.pack(pady=10)

tk.Label(root, text="Mood").pack()
mood_entry = tk.Entry(root)
mood_entry.pack()

tk.Label(root, text="Study Hours").pack()
study_entry = tk.Entry(root)
study_entry.pack()

tk.Label(root, text="Sleep Hours").pack()
sleep_entry = tk.Entry(root)
sleep_entry.pack()

tk.Label(root, text="Water Intake").pack()
water_entry = tk.Entry(root)
water_entry.pack()

tk.Button(root, text="Add Entry", command=add_entry).pack(pady=5)
tk.Button(root, text="Show Score", command=show_score).pack(pady=5)
tk.Button(root, text="AI Suggestions", command=ai_suggestions).pack(pady=5)
tk.Button(root, text="Show Graph", command=show_graph).pack(pady=5)
tk.Button(root, text="View History", command=show_history).pack(pady=5)
tk.Button(root, text="Best Day", command=best_day).pack(pady=5)

root.mainloop()