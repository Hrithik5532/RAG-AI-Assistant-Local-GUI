import sqlite3

def init_db():
    conn = sqlite3.connect('ai_assistant.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS profile
                 (id INTEGER PRIMARY KEY, name TEXT, fireworks_key TEXT, groq_key TEXT)''')
    conn.commit()
    conn.close()

def save_profile(name, fireworks_key, groq_key):
    conn = sqlite3.connect('ai_assistant.db')
    c = conn.cursor()
    c.execute("INSERT INTO profile (name, fireworks_key, groq_key) VALUES (?, ?, ?)",
              (name, fireworks_key, groq_key))
    conn.commit()
    conn.close()

def get_profile():
    conn = sqlite3.connect('ai_assistant.db')
    c = conn.cursor()
    c.execute("SELECT name, fireworks_key, groq_key FROM profile ORDER BY id DESC LIMIT 1")
    profile = c.fetchone()
    conn.close()
    return profile
