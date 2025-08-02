import streamlit as st
import sqlite3
import hashlib
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
import random
import os

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('happiness_app.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 email TEXT PRIMARY KEY,
                 password TEXT,
                 journal_time TEXT
                 )''')
    c.execute('''CREATE TABLE IF NOT EXISTS journals (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 email TEXT,
                 date TEXT,
                 entry TEXT,
                 FOREIGN KEY(email) REFERENCES users(email)
                 )''')
    conn.commit()
    conn.close()

# Hash password for secure storage
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Send email reminder with Achor-inspired prompt
def send_reminder_email(email, journal_time):
    achor_prompts = [
        # Happiness Advantage Prompts
        "Write 3 things you're grateful for today to practice the Positive Tetris Effect.",
        "Reflect on a small, manageable goal you accomplished today (Zorro Circle).",
        "Describe an act of kindness you performed or received to boost social investment.",
        "How did you reframe a challenge today as an opportunity (Falling Up)?",
        "What positive habit did you practice today to lower activation energy (20-Second Rule)?",
        # Big Potential Prompts
        "How did you connect with someone in your 'Star System' today to amplify success?",
        "Write about a moment you empowered someone else to lead (Expand Your Power).",
        "Share a moment of authentic praise you gave or received (Enhance Your Resources).",
        "How did you protect your positivity from negativity today (Defend Against Negative)?",
        "Reflect on a win you celebrated today to sustain momentum (Sustain the Gains)."
    ]
    
    prompt = random.choice(achor_prompts)
    subject = "Daily Happiness Journal Reminder"
    body = f"Hi! It's time to journal at {journal_time}. Today's prompt inspired by Shawn Achor:\n\n{prompt}\n\nLog in to your Happiness App to write your entry!"
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = os.getenv('EMAIL_SENDER')
    msg['To'] = email
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(os.getenv('EMAIL_SENDER'), os.getenv('EMAIL_PASSWORD'))
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Failed to send email: {e}")
        return False

# Check if reminder should be sent
def check_reminders():
    conn = sqlite3.connect('happiness_app.db')
    c = conn.cursor()
    c.execute("SELECT email, journal_time FROM users")
    users = c.fetchall()
    conn.close()
    
    current_time = datetime.now().strftime("%H:%M")
    for email, journal_time in users:
        if current_time == journal_time:
            send_reminder_email(email, journal_time)

# Streamlit app
st.title("Happiness Journal App")
st.write("Inspired by Shawn Achor's *The Happiness Advantage* and *Big Potential*")

init_db()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.email = ""

# Login/Signup
if not st.session_state.logged_in:
    st.subheader("Login or Sign Up")
    choice = st.radio("Select an option:", ("Login", "Sign Up"))
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if choice == "Sign Up":
        journal_time = st.time_input("Preferred Journaling Time")
        if st.button("Sign Up"):
            if email and password and journal_time:
                conn = sqlite3.connect('happiness_app.db')
                c = conn.cursor()
                try:
                    c.execute("INSERT INTO users (email, password, journal_time) VALUES (?, ?, ?)",
                              (email, hash_password(password), journal_time.strftime("%H:%M")))
                    conn.commit()
                    st.success("Sign-up successful! Please log in.")
                except sqlite3.IntegrityError:
                    st.error("Email already exists!")
                conn.close()
            else:
                st.error("Please fill in all fields.")
    
    if choice == "Login":
        if st.button("Login"):
            conn = sqlite3.connect('happiness_app.db')
            c = conn.cursor()
            c.execute("SELECT password FROM users WHERE email = ?", (email,))
            result = c.fetchone()
            conn.close()
            if result and result[0] == hash_password(password):
                st.session_state.logged_in = True
                st.session_state.email = email
                st.success("Logged in successfully!")
            else:
                st.error("Invalid email or password.")

# Journaling Interface
if st.session_state.logged_in:
    st.subheader(f"Welcome, {st.session_state.email}!")
    journal_entry = st.text_area("Today's Journal Entry", height=200)
    if st.button("Save Entry"):
        if journal_entry:
            conn = sqlite3.connect('happiness_app.db')
            c = conn.cursor()
            c.execute("INSERT INTO journals (email, date, entry) VALUES (?, ?, ?)",
                      (st.session_state.email, datetime.now().strftime("%Y-%m-%d"), journal_entry))
            conn.commit()
            conn.close()
            st.success("Journal entry saved!")
        else:
            st.error("Please write something in your journal.")
    
    # Display past entries
    st.subheader("Your Past Entries")
    conn = sqlite3.connect('happiness_app.db')
    c = conn.cursor()
    c.execute("SELECT date, entry FROM journals WHERE email = ? ORDER BY date DESC",
              (st.session_state.email,))
    entries = c.fetchall()
    conn.close()
    
    for date, entry in entries[:21]:  # Limit to 21 days
        st.write(f"**{date}**: {entry}")
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.email = ""
        st.success("Logged out successfully!")

# Check for reminders (runs on app refresh, ideally use a scheduler in production)
check_reminders()
