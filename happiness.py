import streamlit as st
import sqlite3
import hashlib
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
import random
import os

# Custom CSS for styling inspired by the HTML ode
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 20px;
    }
    .container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        padding: 40px;
        max-width: 600px;
        margin: auto;
    }
    .header h1 {
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        color: transparent;
        font-size: 2.5em;
        font-weight: 700;
        text-align: center;
    }
    .insight-card {
        background: linear-gradient(135deg, #ffecd2, #fcb69f);
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 25px;
        border-left: 5px solid #ff6b6b;
    }
    .prompt-section {
        background: linear-gradient(135deg, #a8edea, #fed6e3);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .btn {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 10px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
        text-align: center;
    }
    .btn-secondary {
        background: linear-gradient(135deg, #f093fb, #f5576c);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('happiness_app.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 email TEXT PRIMARY KEY,
                 password TEXT,
                 journal_time TEXT,
                 start_date TEXT,
                 current_day INTEGER
                 )''')
    c.execute('''CREATE TABLE IF NOT EXISTS journals (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 email TEXT,
                 date TEXT,
                 entry TEXT,
                 day INTEGER,
                 FOREIGN KEY(email) REFERENCES users(email)
                 )''')
    conn.commit()
    conn.close()

# Hash password for secure storage
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Send email reminder with Achor-inspired prompt
def send_reminder_email(email, journal_time, current_day):
    daily_content = [
        {
            "day": 1, "principle": "The Happiness Advantage",
            "insight": "Welcome to your happiness journey! Today we begin with Shawn Achor's core principle: happiness fuels success, not the other way around. When we're positive, our brains become more engaged, creative, motivated, energetic, resilient, and productive.",
            "tip": "Start each day by writing down three things you're grateful for. This simple practice rewires your brain to scan for positives.",
            "prompts": [
                "What are three things you're grateful for today?",
                "How did you feel when you accomplished something recently?",
                "What strength did you use today that made you feel good?"
            ]
        },
        {
            "day": 2, "principle": "The Fulcrum and Lever",
            "insight": "Your mindset is your fulcrum - the point from which you view the world. By adjusting your perspective and believing in your potential, you can enhance your performance dramatically.",
            "tip": "Reframe one challenging situation today as an opportunity for growth.",
            "prompts": [
                "What challenge can you reframe as an opportunity today?",
                "How has your perspective on a past difficulty changed over time?",
                "What belief about your abilities would you like to strengthen?"
            ]
        },
        {
            "day": 3, "principle": "The Tetris Effect",
            "insight": "Just like the Tetris game trains your brain to see falling blocks everywhere, we can train our brains to scan for positives. This creates a 'Positive Tetris Effect' that helps us spot opportunities and solutions.",
            "tip": "Practice the 'Good Things' exercise: write down three good things that happened today and why they were meaningful.",
            "prompts": [
                "What three good things happened today, no matter how small?",
                "What opportunities did you notice today that you might have missed before?",
                "How did focusing on positives change your mood or energy?"
            ]
        },
        {
            "day": 4, "principle": "Falling Up",
            "insight": "Adversity doesn't just build character - it can actually propel us to even greater heights. This is called 'Post-Traumatic Growth.' Every setback contains the seeds of future success.",
            "tip": "When facing challenges, ask yourself: 'What can I learn from this?' and 'How might this make me stronger?'",
            "prompts": [
                "What challenge have you faced that ultimately made you stronger?",
                "What lesson did you learn from a recent setback?",
                "How can you use a current difficulty as fuel for growth?"
            ]
        },
        {
            "day": 5, "principle": "The Zorro Circle",
            "insight": "Focus on small, manageable goals to build confidence and control. Like Zorro mastering a small circle before taking on bigger challenges, start with what you can control and expand from there.",
            "tip": "Identify one small area where you can take immediate positive action today.",
            "prompts": [
                "What's one small goal you can accomplish today?",
                "What area of your life feels most within your control right now?",
                "How did completing a small task recently make you feel more capable?"
            ]
        },
        {
            "day": 6, "principle": "The 20-Second Rule",
            "insight": "Make good habits easier by reducing the 'activation energy' required to start them. Remove barriers to positive behaviors and add friction to negative ones.",
            "tip": "Identify one positive habit you want to build and remove one 20-second barrier to doing it.",
            "prompts": [
                "What positive habit would you like to make easier to start?",
                "What barriers can you remove from your environment today?",
                "How can you set yourself up for success tomorrow?"
            ]
        },
        {
            "day": 7, "principle": "Social Investment",
            "insight": "Strong social connections are the greatest predictor of happiness and success. Relationships release oxytocin, reduce stress, and enhance performance. Your social network is your greatest asset.",
            "tip": "Reach out to someone you care about today - send a text, make a call, or write a note of appreciation.",
            "prompts": [
                "Who in your life deserves recognition or appreciation?",
                "How did a relationship help you through a difficult time?",
                "What can you do to strengthen a meaningful connection today?"
            ]
        },
        {
            "day": 8, "principle": "Big Potential - SURROUND",
            "insight": "Your potential is amplified by surrounding yourself with positive influencers. Build a 'Star System' of supporters, connectors, and growth-pushers who elevate your success.",
            "tip": "Identify the positive influencers in your life and consider how you can spend more time with them.",
            "prompts": [
                "Who are the most positive influences in your life?",
                "How have others helped amplify your potential?",
                "What qualities do you want to cultivate in your social circle?"
            ]
        },
        {
            "day": 9, "principle": "Big Potential - EXPAND",
            "insight": "True leadership means empowering everyone around you to lead, regardless of their role. When we expand power to others, we multiply our own impact and create collective success.",
            "tip": "Look for an opportunity to empower someone else today - give them a chance to lead or make decisions.",
            "prompts": [
                "How can you empower someone else today?",
                "When has someone believed in your leadership potential?",
                "What decision can you involve others in making?"
            ]
        },
        {
            "day": 10, "principle": "Big Potential - ENHANCE",
            "insight": "Use authentic praise to amplify others' potential. When we become a 'Prism of Praise,' we help others see their own strengths and capabilities more clearly.",
            "tip": "Give specific, authentic praise to someone today, focusing on their effort and growth rather than just results.",
            "prompts": [
                "Who deserves specific recognition for their efforts?",
                "How has someone's praise impacted your confidence?",
                "What strength do you see in others that they might not see in themselves?"
            ]
        },
        {
            "day": 11, "principle": "Big Potential - DEFEND",
            "insight": "Protect your ecosystem from negative influences by creating 'moats' against negativity, building mental strongholds of positivity, and practicing 'Mental Aikido' to reframe stress.",
            "tip": "Create one 'defense' against negativity today - limit negative news, practice gratitude, or reframe a stressful situation.",
            "prompts": [
                "What negative influences can you limit in your life?",
                "How can you reframe a current stress as an opportunity?",
                "What positive practices help you stay resilient?"
            ]
        },
        {
            "day": 12, "principle": "Big Potential - SUSTAIN",
            "insight": "Maintain momentum through 'Tours of Meaning' - regularly reconnecting with your purpose, using vivid visualization, and celebrating wins along the way.",
            "tip": "Take a moment to reconnect with your deeper purpose and celebrate a recent win, no matter how small.",
            "prompts": [
                "What gives your life meaning and purpose?",
                "What recent win can you celebrate today?",
                "How do your daily actions connect to your larger goals?"
            ]
        },
        {
            "day": 13, "principle": "Meditation and Mindfulness",
            "insight": "Research shows that just 2 minutes of meditation for 21 days can literally rewire your brain for positivity. Meditation trains your brain to focus on the present moment and find calm in chaos.",
            "tip": "Spend 2 minutes today in quiet meditation or deep breathing. Focus on your breath and let thoughts pass by like clouds.",
            "prompts": [
                "How did taking a moment of stillness affect your mood?",
                "What thoughts or worries can you release today?",
                "When do you feel most present and mindful?"
            ]
        },
        {
            "day": 14, "principle": "Acts of Kindness",
            "insight": "Performing acts of kindness releases serotonin in your brain and creates a 'helper's high.' Kindness is contagious and creates positive ripple effects throughout your community.",
            "tip": "Perform one random act of kindness today - hold a door, send an encouraging message, or help someone with a task.",
            "prompts": [
                "What act of kindness did you perform or witness today?",
                "How did helping someone else make you feel?",
                "What kindness have you received that you're grateful for?"
            ]
        },
        {
            "day": 15, "principle": "Exercise and Energy",
            "insight": "Exercise is as effective as antidepressants in treating depression and anxiety. Physical activity releases endorphins and literally grows new brain cells that enhance learning and memory.",
            "tip": "Move your body for at least 15 minutes today - walk, dance, stretch, or do any activity that gets your heart pumping.",
            "prompts": [
                "How did physical movement affect your energy and mood today?",
                "What type of exercise or movement brings you joy?",
                "How can you incorporate more movement into your daily routine?"
            ]
        },
        {
            "day": 16, "principle": "Optimism and Resilience",
            "insight": "Optimists live longer, have better health, and achieve more success. Optimism isn't about ignoring problems - it’s about believing in your ability to solve them and seeing setbacks as temporary.",
            "tip": "Practice the 'Best Possible Self' exercise - spend 10 minutes writing about your ideal future self and the steps to get there.",
            "prompts": [
                "What are you most optimistic about in your life right now?",
                "How has optimism helped you overcome challenges?",
                "What positive possibilities do you see for your future?"
            ]
        },
        {
            "day": 17, "principle": "Strengths Focus",
            "insight": "People who use their top strengths daily are 6 times more engaged at work and 3 times more likely to report having an excellent quality of life. Focus on what you do best, not just what needs improvement.",
            "tip": "Identify your top strength and find a way to use it in a new or expanded way today.",
            "prompts": [
                "What are your top 3 strengths or talents?",
                "How did you use your strengths today?",
                "How can you develop your strengths further?"
            ]
        },
        {
            "day": 18, "principle": "Positive Communication",
            "insight": "The language we use shapes our reality. Positive communication doesn't mean avoiding difficult topics - it means framing conversations in ways that build solutions and maintain relationships.",
            "tip": "Practice positive communication today by using 'and' instead of 'but' and focusing on possibilities rather than problems.",
            "prompts": [
                "How did positive communication improve an interaction today?",
                "What conversation would benefit from a more positive approach?",
                "How can your words lift others up?"
            ]
        },
        {
            "day": 19, "principle": "Meaning and Purpose",
            "insight": "Having a sense of meaning and purpose is one of the strongest predictors of happiness and resilience. When we connect our daily actions to a larger purpose, even mundane tasks become meaningful.",
            "tip": "Connect one routine task today to your larger purpose or values. How does this task serve something greater?",
            "prompts": [
                "What gives your life meaning and purpose?",
                "How do your daily actions align with your values?",
                "What legacy do you want to leave through your work and relationships?"
            ]
        },
        {
            "day": 20, "principle": "Celebration and Recognition",
            "insight": "Celebrating wins - both big and small - reinforces positive neural pathways and motivates continued growth. Recognition activates the same neural reward circuits as receiving money.",
            "tip": "Celebrate three wins from your day, week, or recent past. Share at least one celebration with someone else.",
            "prompts": [
                "What accomplishments from this week deserve celebration?",
                "How has recognizing your progress motivated you?",
                "Who else's achievements can you celebrate today?"
            ]
        },
        {
            "day": 21, "principle": "The Ripple Effect",
            "insight": "Your positivity creates ripples that extend far beyond what you can see. Every smile, kind word, and positive action influences others, who then influence others. You are more powerful than you know.",
            "tip": "Reflect on your 21-day journey and identify how your positive changes may have influenced others around you.",
            "prompts": [
                "How have you grown over these 21 days?",
                "What positive changes have you noticed in yourself?",
                "How might your journey have influenced others?",
                "What practices will you continue moving forward?"
            ]
        }
    ]
    
    if current_day <= 21:
        content = daily_content[current_day - 1]
        prompt = random.choice(content["prompts"])
        subject = "📝 Daily Happiness Journal Reminder"
        body = f"Hi! It's time to journal at {journal_time}. Today's focus: {content['principle']}\n\nPrompt: {prompt}\n\nLog in to your Happiness App at {os.getenv('APP_URL', 'http://localhost:8501')} to write your entry!"
        
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
    return False

# Initialize database
init_db()

# Streamlit app
st.markdown('<div class="main"><div class="container">', unsafe_allow_html=True)
st.markdown('<div class="header"><h1>✨ 21-Day Happiness Journal ✨</h1></div>', unsafe_allow_html=True)
st.markdown("Transform your life with daily practices based on Shawn Achor's research", unsafe_allow_html=True)

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.email = ""
    st.session_state.current_day = 1

# Login/Signup
if not st.session_state.logged_in:
    st.markdown("<h2>Login or Sign Up</h2>", unsafe_allow_html=True)
    choice = st.radio("Select an option:", ("Login", "Sign Up"))
    
    with st.form("setup_form"):
        email = st.text_input("Email Address", placeholder="your@email.com")
        password = st.text_input("Password", type="password", placeholder="Create a secure password")
        journal_time = st.selectbox("Preferred Journal Time", 
                                   ["Select your preferred time", "07:00", "12:00", "18:00", "21:00"],
                                   format_func=lambda x: {"07:00": "Morning (7:00 AM)", "12:00": "Lunch Time (12:00 PM)", 
                                                        "18:00": "Evening (6:00 PM)", "21:00": "Night (9:00 PM)",
                                                        "Select your preferred time": "Select your preferred time"}[x])
        
        submitted = st.form_submit_button("Submit", use_container_width=True)
        if submitted:
            if choice == "Sign Up":
                if email and password and journal_time != "Select your preferred time":
                    conn = sqlite3.connect('happiness_app.db')
                    c = conn.cursor()
                    try:
                        c.execute("INSERT INTO users (email, password, journal_time, start_date, current_day) VALUES (?, ?, ?, ?, ?)",
                                  (email, hash_password(password), journal_time, datetime.now().strftime("%Y-%m-%d"), 1))
                        conn.commit()
                        st.success("Sign-up successful! Please log in.")
                    except sqlite3.IntegrityError:
                        st.error("Email already exists!")
                    conn.close()
                else:
                    st.error("Please fill in all fields.")
            
            if choice == "Login":
                conn = sqlite3.connect('happiness_app.db')
                c = conn.cursor()
                c.execute("SELECT password, current_day FROM users WHERE email = ?", (email,))
                result = c.fetchone()
                conn.close()
                if result and result[0] == hash_password(password):
                    st.session_state.logged_in = True
                    st.session_state.email = email
                    st.session_state.current_day = result[1]
                    st.success("Logged in successfully!")
                else:
                    st.error("Invalid email or password.")

# Journaling Interface
if st.session_state.logged_in:
    conn = sqlite3.connect('happiness_app.db')
    c = conn.cursor()
    c.execute("SELECT current_day, start_date FROM users WHERE email = ?", (st.session_state.email,))
    user_data = c.fetchone()
    current_day = user_data[0]
    start_date = datetime.strptime(user_data[1], "%Y-%m-%d")
    conn.close()
    
    st.session_state.current_day = current_day
    
    if current_day > 21:
        st.markdown("<div class='celebration'><h2>🎉 Congratulations! 🎉</h2><p>You've completed your 21-day happiness journey!</p></div>", unsafe_allow_html=True)
        
        conn = sqlite3.connect('happiness_app.db')
        c = conn.cursor()
        c.execute("SELECT entry FROM journals WHERE email = ? ORDER BY day", (st.session_state.email,))
        entries = c.fetchall()
        conn.close()
        
        total_words = sum(len(entry[0].split()) for entry in entries)
        avg_words = round(total_words / len(entries)) if entries else 0
        
        st.markdown("<div class='stats'>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("<div class='stat-card'><div class='stat-number'>21</div><div>Days Completed</div></div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"<div class='stat-card'><div class='stat-number'>{len(entries)}</div><div>Journal Entries</div></div>", unsafe_allow_html=True)
        with col3:
            st.markdown(f"<div class='stat-card'><div class='stat-number'>{total_words}</div><div>Total Words</div></div>", unsafe_allow_html=True)
        with col4:
            st.markdown(f"<div class='stat-card'><div class='stat-number'>{avg_words}</div><div>Avg Words/Entry</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("Start Another 21-Day Cycle", key="new_cycle"):
            conn = sqlite3.connect('happiness_app.db')
            c = conn.cursor()
            c.execute("UPDATE users SET current_day = 1, start_date = ? WHERE email = ?",
                      (datetime.now().strftime("%Y-%m-%d"), st.session_state.email))
            c.execute("DELETE FROM journals WHERE email = ?", (st.session_state.email,))
            conn.commit()
            conn.close()
            st.session_state.current_day = 1
            st.rerun()
    else:
        daily_content = [
            {
                "day": 1, "principle": "The Happiness Advantage", "insight": "Welcome to your happiness journey! Today we begin with Shawn Achor's core principle: happiness fuels success, not the other way around. When we're positive, our brains become more engaged, creative, motivated, energetic, resilient, and productive.",
                "tip": "Start each day by writing down three things you're grateful for. This simple practice rewires your brain to scan for positives.", "prompts": ["What are three things you're grateful for today?", "How did you feel when you accomplished something recently?", "What strength did you use today that made you feel good?"]
            },
            {"day": 2, "principle": "The Fulcrum and Lever", "insight": "Your mindset is your fulcrum - the point from which you view the world. By adjusting your perspective and believing in your potential, you can enhance your performance dramatically.", "tip": "Reframe one challenging situation today as an opportunity for growth.", "prompts": ["What challenge can you reframe as an opportunity today?", "How has your perspective on a past difficulty changed over time?", "What belief about your abilities would you like to strengthen?"]},
            {"day": 3, "principle": "The Tetris Effect", "insight": "Just like the Tetris game trains your brain to see falling blocks everywhere, we can train our brains to scan for positives. This creates a 'Positive Tetris Effect' that helps us spot opportunities and solutions.", "tip": "Practice the 'Good Things' exercise: write down three good things that happened today and why they were meaningful.", "prompts": ["What three good things happened today, no matter how small?", "What opportunities did you notice today that you might have missed before?", "How did focusing on positives change your mood or energy?"]},
            {"day": 4, "principle": "Falling Up", "insight": "Adversity doesn't just build character - it can actually propel us to even greater heights. This is called 'Post-Traumatic Growth.' Every setback contains the seeds of future success.", "tip": "When facing challenges, ask yourself: 'What can I learn from this?' and 'How might this make me stronger?'", "prompts": ["What challenge have you faced that ultimately made you stronger?", "What lesson did you learn from a recent setback?", "How can you use a current difficulty as fuel for growth?"]},
            {"day": 5, "principle": "The Zorro Circle", "insight": "Focus on small, manageable goals to build confidence and control. Like Zorro mastering a small circle before taking on bigger challenges, start with what you can control and expand from there.", "tip": "Identify one small area where you can take immediate positive action today.", "prompts": ["What's one small goal you can accomplish today?", "What area of your life feels most within your control right now?", "How did completing a small task recently make you feel more capable?"]},
            {"day": 6, "principle": "The 20-Second Rule", "insight": "Make good habits easier by reducing the 'activation energy' required to start them. Remove barriers to positive behaviors and add friction to negative ones.", "tip": "Identify one positive habit you want to build and remove one 20-second barrier to doing it.", "prompts": ["What positive habit would you like to make easier to start?", "What barriers can you remove from your environment today?", "How can you set yourself up for success tomorrow?"]},
            {"day": 7, "principle": "Social Investment", "insight": "Strong social connections are the greatest predictor of happiness and success. Relationships release oxytocin, reduce stress, and enhance performance. Your social network is your greatest asset.", "tip": "Reach out to someone you care about today - send a text, make a call, or write a note of appreciation.", "prompts": ["Who in your life deserves recognition or appreciation?", "How did a relationship help you through a difficult time?", "What can you do to strengthen a meaningful connection today?"]},
            {"day": 8, "principle": "Big Potential - SURROUND", "insight": "Your potential is amplified by surrounding yourself with positive influencers. Build a 'Star System' of supporters, connectors, and growth-pushers who elevate your success.", "tip": "Identify the positive influencers in your life and consider how you can spend more time with them.", "prompts": ["Who are the most positive influences in your life?", "How have others helped amplify your potential?", "What qualities do you want to cultivate in your social circle?"]},
            {"day": 9, "principle": "Big Potential - EXPAND", "insight": "True leadership means empowering everyone around you to lead, regardless of their role. When we expand power to others, we multiply our own impact and create collective success.", "tip": "Look for an opportunity to empower someone else today - give them a chance to lead or make decisions.", "prompts": ["How can you empower someone else today?", "When has someone believed in your leadership potential?", "What decision can you involve others in making?"]},
            {"day": 10, "principle": "Big Potential - ENHANCE", "insight": "Use authentic praise to amplify others' potential. When we become a 'Prism of Praise,' we help others see their own strengths and capabilities more clearly.", "tip": "Give specific, authentic praise to someone today, focusing on their effort and growth rather than just results.", "prompts": ["Who deserves specific recognition for their efforts?", "How has someone's praise impacted your confidence?", "What strength do you see in others that they might not see in themselves?"]},
            {"day": 11, "principle": "Big Potential - DEFEND", "insight": "Protect your ecosystem from negative influences by creating 'moats' against negativity, building mental strongholds of positivity, and practicing 'Mental Aikido' to reframe stress.", "tip": "Create one 'defense' against negativity today - limit negative news, practice gratitude, or reframe a stressful situation.", "prompts": ["What negative influences can you limit in your life?", "How can you reframe a current stress as an opportunity?", "What positive practices help you stay resilient?"]},
            {"day": 12, "principle": "Big Potential - SUSTAIN", "insight": "Maintain momentum through 'Tours of Meaning' - regularly reconnecting with your purpose, using vivid visualization, and celebrating wins along the way.", "tip": "Take a moment to reconnect with your deeper purpose and celebrate a recent win, no matter how small.", "prompts": ["What gives your life meaning and purpose?", "What recent win can you celebrate today?", "How do your daily actions connect to your larger goals?"]},
            {"day": 13, "principle": "Meditation and Mindfulness", "insight": "Research shows that just 2 minutes of meditation for 21 days can literally rewire your brain for positivity. Meditation trains your brain to focus on the present moment and find calm in chaos.", "tip": "Spend 2 minutes today in quiet meditation or deep breathing. Focus on your breath and let thoughts pass by like clouds.", "prompts": ["How did taking a moment of stillness affect your mood?", "What thoughts or worries can you release today?", "When do you feel most present and mindful?"]},
            {"day": 14, "principle": "Acts of Kindness", "insight": "Performing acts of kindness releases serotonin in your brain and creates a 'helper's high.' Kindness is contagious and creates positive ripple effects throughout your community.", "tip": "Perform one random act of kindness today - hold a door, send an encouraging message, or help someone with a task.", "prompts": ["What act of kindness did you perform or witness today?", "How did helping someone else make you feel?", "What kindness have you received that you're grateful for?"]},
            {"day": 15, "principle": "Exercise and Energy", "insight": "Exercise is as effective as antidepressants in treating depression and anxiety. Physical activity releases endorphins and literally grows new brain cells that enhance learning and memory.", "tip": "Move your body for at least 15 minutes today - walk, dance, stretch, or do any activity that gets your heart pumping.", "prompts": ["How did physical movement affect your energy and mood today?", "What type of exercise or movement brings you joy?", "How can you incorporate more movement into your daily routine?"]},
            {"day": 16, "principle": "Optimism and Resilience", "insight": "Optimists live longer, have better health, and achieve more success. Optimism isn't about ignoring problems - it’s about believing in your ability to solve them and seeing setbacks as temporary.", "tip": "Practice the 'Best Possible Self' exercise - spend 10 minutes writing about your ideal future self and the steps to get there.", "prompts": ["What are you most optimistic about in your life right now?", "How has optimism helped you overcome challenges?", "What positive possibilities do you see for your future?"]},
            {"day": 17, "principle": "Strengths Focus", "insight": "People who use their top strengths daily are 6 times more engaged at work and 3 times more likely to report having an excellent quality of life. Focus on what you do best, not just what needs improvement.", "tip": "Identify your top strength and find a way to use it in a new or expanded way today.", "prompts": ["What are your top 3 strengths or talents?", "How did you use your strengths today?", "How can you develop your strengths further?"]},
            {"day": 18, "principle": "Positive Communication", "insight": "The language we use shapes our reality. Positive communication doesn't mean avoiding difficult topics - it means framing conversations in ways that build solutions and maintain relationships.", "tip": "Practice positive communication today by using 'and' instead of 'but' and focusing on possibilities rather than problems.", "prompts": ["How did positive communication improve an interaction today?", "What conversation would benefit from a more positive approach?", "How can your words lift others up?"]},
            {"day": 19, "principle": "Meaning and Purpose", "insight": "Having a sense of meaning and purpose is one of the strongest predictors of happiness and resilience. When we connect our daily actions to a larger purpose, even mundane tasks become meaningful.", "tip": "Connect one routine task today to your larger purpose or values. How does this task serve something greater?", "prompts": ["What gives your life meaning and purpose?", "How do your daily actions align with your values?", "What legacy do you want to leave through your work and relationships?"]},
            {"day": 20, "principle": "Celebration and Recognition", "insight": "Celebrating wins - both big and small - reinforces positive neural pathways and motivates continued growth. Recognition activates the same neural reward circuits as receiving money.", "tip": "Celebrate three wins from your day, week, or recent past. Share at least one celebration with someone else.", "prompts": ["What accomplishments from this week deserve celebration?", "How has recognizing your progress motivated you?", "Who else's achievements can you celebrate today?"]},
            {"day": 21, "principle": "The Ripple Effect", "insight": "Your positivity creates ripples that extend far beyond what you can see. Every smile, kind word, and positive action influences others, who then influence others. You are more powerful than you know.", "tip": "Reflect on your 21-day journey and identify how your positive changes may have influenced others around you.", "prompts": ["How have you grown over these 21 days?", "What positive changes have you noticed in yourself?", "How might your journey have influenced others?", "What practices will you continue moving forward?"]}
        ]
        
        st.markdown(f"<div class='day-counter'>Day {current_day} of 21</div>", unsafe_allow_html=True)
        st.progress(current_day / 21.0)
        
        tab1, tab2 = st.tabs(["Daily Insight", "Journal"])
        
        with tab1:
            st.markdown(f"""
            <div class='insight-card'>
                <h3>{daily_content[current_day - 1]['principle']}</h3>
                <p><strong>Insight:</strong> {daily_content[current_day - 1]['insight']}</p>
                <p><strong>Today's Tip:</strong> {daily_content[current_day - 1]['tip']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with tab2:
            st.markdown(f"""
            <div class='prompt-section'>
                <h4>Today's Journal Prompts:</h4>
                {"".join([f"<p>• {prompt}</p>" for prompt in daily_content[current_day - 1]['prompts']])}
            </div>
            """, unsafe_allow_html=True)
            
            conn = sqlite3.connect('happiness_app.db')
            c = conn.cursor()
            c.execute("SELECT entry FROM journals WHERE email = ? AND day = ?", 
                     (st.session_state.email, current_day))
            existing_entry = c.fetchone()
            conn.close()
            
            journal_entry = st.text_area("Your Journal Entry", 
                                       value=existing_entry[0] if existing_entry else "",
                                       placeholder="Write your thoughts, reflections, and gratitude here...",
                                       height=200)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Save Today's Entry", key="save_entry"):
                    if journal_entry.strip():
                        conn = sqlite3.connect('happiness_app.db')
                        c = conn.cursor()
                        c.execute("DELETE FROM journals WHERE email = ? AND day = ?", 
                                 (st.session_state.email, current_day))
                        c.execute("INSERT INTO journals (email, date, entry, day) VALUES (?, ?, ?, ?)",
                                 (st.session_state.email, datetime.now().strftime("%Y-%m-%d"), 
                                  journal_entry, current_day))
                        if current_day < 21:
                            c.execute("UPDATE users SET current_day = ? WHERE email = ?",
                                     (current_day + 1, st.session_state.email))
                        conn.commit()
                        conn.close()
                        st.session_state.current_day = min(current_day + 1, 22)
                        st.success(f"Great job! Your entry for Day {current_day} has been saved. {'See you tomorrow for Day ' + str(current_day + 1) + '!' if current_day < 21 else 'You’ve completed the journey!'}")
                        st.rerun()
                    else:
                        st.error("Please write something in your journal.")
            with col2:
                if st.button("View Today's Insight Again", key="view_insight"):
                    st.rerun()
        
        st.markdown("<h2>Your Past Entries</h2>", unsafe_allow_html=True)
        conn = sqlite3.connect('happiness_app.db')
        c = conn.cursor()
        c.execute("SELECT day, date, entry FROM journals WHERE email = ? ORDER BY day DESC",
                 (st.session_state.email,))
        entries = c.fetchall()
        conn.close()
        
        for day, date, entry in entries:
            st.markdown(f"**Day {day} ({date})**: {entry}")
    
    if st.button("Logout", key="logout"):
        st.session_state.logged_in = False
        st.session_state.email = ""
        st.session_state.current_day = 1
        st.success("Logged out successfully!")
        st.rerun()

st.markdown("</div></div>", unsafe_allow_html=True)
