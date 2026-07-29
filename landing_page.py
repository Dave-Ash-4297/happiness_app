import streamlit as st
import snowflake.connector
from datetime import datetime
import time

st.set_page_config(
    page_title="Happiness Survey - Addleshaw Goddard",
    page_icon="😊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
    }

    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }

    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    [data-testid="stMainBlockContainer"] {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .container {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        padding: 3rem;
        max-width: 700px;
        margin: 0 auto;
    }

    .header {
        text-align: center;
        margin-bottom: 2rem;
    }

    .header h1 {
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5em;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .header p {
        color: #555;
        font-size: 1.1em;
        margin-bottom: 0.5rem;
    }

    .form-section {
        background: #f8f9ff;
        border-radius: 15px;
        padding: 2rem;
        margin: 1.5rem 0;
        border-left: 5px solid #667eea;
    }

    .form-section h3 {
        color: #667eea;
        margin-bottom: 1rem;
        font-size: 1.3em;
    }

    .form-section p {
        color: #666;
        margin-bottom: 1rem;
        line-height: 1.6;
    }

    .ticker-container {
        background: linear-gradient(135deg, #ffecd2, #fcb69f);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 2rem 0;
        border-left: 5px solid #ff6b6b;
        min-height: 80px;
        display: flex;
        align-items: center;
        overflow: hidden;
    }

    .ticker-text {
        font-size: 1.1em;
        color: #333;
        font-weight: 500;
        font-style: italic;
        animation: scroll 15s linear infinite;
    }

    @keyframes scroll {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }

    .quote-mark {
        color: #ff6b6b;
        font-size: 1.5em;
        margin-right: 0.5rem;
    }

    .progress-bar {
        background: #ddd;
        border-radius: 10px;
        padding: 0.25rem;
        margin: 2rem 0;
        height: 8px;
    }

    .progress-fill {
        background: linear-gradient(90deg, #667eea, #764ba2);
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }

    .button-group {
        display: flex;
        gap: 1rem;
        margin-top: 2rem;
        flex-wrap: wrap;
    }

    .btn {
        flex: 1;
        min-width: 150px;
        padding: 0.75rem 1.5rem;
        border-radius: 10px;
        border: none;
        font-weight: 600;
        font-size: 1em;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .btn-primary {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
    }

    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }

    .btn-secondary {
        background: #f0f0f0;
        color: #333;
        border: 2px solid #ddd;
    }

    .btn-secondary:hover {
        background: #e8e8e8;
    }

    .mood-selector {
        display: flex;
        justify-content: space-around;
        gap: 1rem;
        margin: 1.5rem 0;
        flex-wrap: wrap;
    }

    .mood-option {
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }

    .mood-emoji {
        font-size: 3em;
        margin-bottom: 0.5rem;
        transition: transform 0.3s ease;
    }

    .mood-option:hover .mood-emoji {
        transform: scale(1.2);
    }

    .mood-label {
        color: #666;
        font-weight: 600;
    }

    .success-box {
        background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
    }

    .success-box h2 {
        color: #2d5016;
        margin-bottom: 1rem;
    }

    .success-box p {
        color: #2d5016;
        font-size: 1.1em;
        margin-bottom: 1rem;
    }

    .link-button {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        text-decoration: none;
        font-weight: 600;
        margin: 0.5rem;
        transition: all 0.3s ease;
    }

    .link-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
    }

    .step-indicator {
        color: #667eea;
        font-weight: 700;
        font-size: 1.2em;
        margin-bottom: 1rem;
    }

    .thank-you-text {
        color: #667eea;
        font-weight: 600;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Quotes from "The Happiness Advantage" by Shawn Achor
HAPPINESS_QUOTES = [
    "The greatest competitive advantage is a positive brain.",
    "Success is not the gateway to happiness, happiness is the gateway to success.",
    "Small changes can produce big shifts in the way we experience our work and our lives.",
    "A positive brain is 31% more productive than a negative brain.",
    "When we are positive, our brains become more engaged, creative, motivated, and energetic.",
    "Happiness is not about the absence of challenges, but our ability to overcome them.",
    "Your brain at positive performs better than at negative, neutral or stressed.",
    "Patterns of thinking become physical neural pathways in our brains.",
    "Optimists see the finish line not just the obstacles.",
    "The habits you build now will determine your outcomes in the future.",
]

# Initialize Snowflake connection
@st.cache_resource
def init_snowflake():
    try:
        return snowflake.connector.connect(
            user=st.secrets.get("snowflake_user"),
            password=st.secrets.get("snowflake_password"),
            account=st.secrets.get("snowflake_account"),
            warehouse=st.secrets.get("snowflake_warehouse"),
            database=st.secrets.get("snowflake_database"),
            schema=st.secrets.get("snowflake_schema")
        )
    except Exception as e:
        st.warning(f"Snowflake connection not configured. Data will not be saved. Error: {e}")
        return None

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.mood = None
    st.session_state.works_at_ag = None
    st.session_state.how_got_code = None
    st.session_state.in_red = None
    st.session_state.wish = None
    st.session_state.knowledge_lawyer = None
    st.session_state.team_name = None
    st.session_state.stress_wish = None
    st.session_state.happiness_interest = None
    st.session_state.survey_complete = False

# Display rotating quote ticker
quote_index = int(time.time() / 5) % len(HAPPINESS_QUOTES)
st.markdown(f"""
<div class="ticker-container">
    <span class="quote-mark">"</span>
    <div class="ticker-text">{HAPPINESS_QUOTES[quote_index]}</div>
    <span class="quote-mark">"</span>
</div>
""", unsafe_allow_html=True)

# Main container
st.markdown('<div class="container">', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h1>😊 How Are You Today?</h1>
    <p>Thank you for scanning the QR code!</p>
    <p style="font-size: 0.95em; color: #888; margin-top: 1rem;">
        We're gathering insights on what would make your job easier and happier.
        Your feedback matters to us.
    </p>
</div>
""", unsafe_allow_html=True)

# Progress indicator
progress_percent = (st.session_state.step - 1) / 7
st.markdown(f"""
<div class="progress-bar">
    <div class="progress-fill" style="width: {progress_percent * 100}%"></div>
</div>
<p style="text-align: center; color: #667eea; font-weight: 600;">Step {st.session_state.step} of 7</p>
""", unsafe_allow_html=True)

# Step 1: Mood Selection
if st.session_state.step == 1:
    st.markdown("""
    <div class="form-section">
        <h3>How are you feeling today?</h3>
        <p>Select the emoji that best represents your current mood.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    moods = [
        ("😞", "Not Great"),
        ("😐", "Okay"),
        ("🙂", "Good"),
        ("😊", "Great"),
        ("🤩", "Amazing")
    ]

    cols = [col1, col2, col3, col4, col5]
    for col, (emoji, label) in zip(cols, moods):
        with col:
            if st.button(f"{emoji}\n{label}", key=f"mood_{label}", use_container_width=True):
                st.session_state.mood = label
                st.session_state.step = 2
                st.rerun()

# Step 2: Organization Check
elif st.session_state.step == 2:
    st.markdown("""
    <div class="form-section">
        <h3>Do you work at Addleshaw Goddard?</h3>
        <p>If not, how did you receive the lollipop with the QR code?</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Yes, I work at Addleshaw Goddard", use_container_width=True, key="ag_yes"):
            st.session_state.works_at_ag = True
            st.session_state.step = 3
            st.rerun()

    with col2:
        if st.button("No, I received it from...", use_container_width=True, key="ag_no"):
            st.session_state.works_at_ag = False
            st.session_state.step = 2.5
            st.rerun()

# Step 2.5: How got the code
elif st.session_state.step == 2.5:
    st.markdown("""
    <div class="form-section">
        <h3>How did you receive the lollipop with the QR code?</h3>
        <p>Please tell us how you came across this survey.</p>
    </div>
    """, unsafe_allow_html=True)

    how_got = st.text_input(
        "Please describe how you got the QR code:",
        placeholder="e.g., A colleague gave it to me, found it at an event, etc.",
        key="how_got_input"
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("← Back", use_container_width=True, key="back_2_5"):
            st.session_state.step = 2
            st.rerun()

    with col2:
        if st.button("Next →", use_container_width=True, key="next_2_5"):
            if how_got.strip():
                st.session_state.how_got_code = how_got
                st.session_state.step = 4
                st.rerun()
            else:
                st.error("Please tell us how you received the QR code.")

# Step 3: Real Estate Disputes Check
elif st.session_state.step == 3:
    st.markdown("""
    <div class="form-section">
        <h3>Are you in the Real Estate Disputes team?</h3>
        <p>This helps us tailor our insights to your specific role.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("← Back", use_container_width=True, key="back_3"):
            st.session_state.step = 2
            st.rerun()

    with col2:
        if st.button("Yes", use_container_width=True, key="red_yes"):
            st.session_state.in_red = True
            st.session_state.step = 5
            st.rerun()

    with col3:
        if st.button("No", use_container_width=True, key="red_no"):
            st.session_state.in_red = False
            st.session_state.step = 3.5
            st.rerun()

# Step 3.5: Team name if not RED
elif st.session_state.step == 3.5:
    st.markdown("""
    <div class="form-section">
        <h3>What team are you in?</h3>
        <p>Please tell us your team name so we can better understand your needs.</p>
    </div>
    """, unsafe_allow_html=True)

    team = st.text_input(
        "Your team name:",
        placeholder="e.g., Corporate, Employment, M&A, etc.",
        key="team_input"
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("← Back", use_container_width=True, key="back_3_5"):
            st.session_state.step = 3
            st.rerun()

    with col2:
        if st.button("Next →", use_container_width=True, key="next_3_5"):
            if team.strip():
                st.session_state.team_name = team
                st.session_state.step = 4.5
                st.rerun()
            else:
                st.error("Please enter your team name.")

# Step 4.5: Stress/Job improvement for non-RED
elif st.session_state.step == 4.5:
    st.markdown("""
    <div class="form-section">
        <h3>What would make your job easier, better, or less stressful?</h3>
        <p>Tell us your wishes - what would you change if you could?</p>
    </div>
    """, unsafe_allow_html=True)

    stress_wish = st.text_area(
        "Your answer:",
        placeholder="Share your thoughts on what would improve your work experience...",
        height=150,
        key="stress_wish_input"
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("← Back", use_container_width=True, key="back_4_5"):
            st.session_state.step = 3.5
            st.rerun()

    with col2:
        if st.button("Next →", use_container_width=True, key="next_4_5"):
            if stress_wish.strip():
                st.session_state.stress_wish = stress_wish
                st.session_state.step = 6
                st.rerun()
            else:
                st.error("Please share your thoughts.")

# Step 4: RED - Job improvement wish
elif st.session_state.step == 4:
    st.markdown("""
    <div class="form-section">
        <h3>If you could make one wish to improve your job...</h3>
        <p>What would make your role easier or more fulfilling?</p>
    </div>
    """, unsafe_allow_html=True)

    wish = st.text_area(
        "Your wish:",
        placeholder="Tell us what you'd change if you could wave a magic wand...",
        height=150,
        key="wish_input"
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("← Back", use_container_width=True, key="back_4"):
            st.session_state.step = 3
            st.rerun()

    with col2:
        if st.button("Next →", use_container_width=True, key="next_4"):
            if wish.strip():
                st.session_state.wish = wish
                st.session_state.step = 5
                st.rerun()
            else:
                st.error("Please share your wish.")

# Step 5: Knowledge Lawyer support
elif st.session_state.step == 5:
    st.markdown("""
    <div class="form-section">
        <h3>What would help you be more successful as a team?</h3>
        <p>What do you need from a knowledge lawyer or what support would benefit your team?</p>
    </div>
    """, unsafe_allow_html=True)

    kl_support = st.text_area(
        "Your answer:",
        placeholder="Tell us how a knowledge lawyer or additional support could help your team succeed...",
        height=150,
        key="kl_input"
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("← Back", use_container_width=True, key="back_5"):
            if st.session_state.in_red:
                st.session_state.step = 4
            else:
                st.session_state.step = 4.5
            st.rerun()

    with col2:
        if st.button("Next →", use_container_width=True, key="next_5"):
            if kl_support.strip():
                st.session_state.knowledge_lawyer = kl_support
                st.session_state.step = 6
                st.rerun()
            else:
                st.error("Please share your thoughts.")

# Step 6: Happiness Interest
elif st.session_state.step == 6:
    st.markdown("""
    <div class="form-section">
        <h3>Are you interested in being happier at work?</h3>
        <p>We offer resources and tools to help build a happiness advantage in your career.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        if st.button("← Back", use_container_width=True, key="back_6"):
            st.session_state.step = 5
            st.rerun()

    with col2:
        if st.button("Yes, I'm interested!", use_container_width=True, key="happy_yes"):
            st.session_state.happiness_interest = True
            st.session_state.step = 7
            st.rerun()

    with col3:
        if st.button("No, thanks", use_container_width=True, key="happy_no"):
            st.session_state.happiness_interest = False
            st.session_state.step = 7
            st.rerun()

# Step 7: Thank you & Resources
elif st.session_state.step == 7:
    st.markdown("""
    <div class="success-box">
        <h2>✨ Thank You! ✨</h2>
        <p>Your feedback has been recorded and will help us create a happier workplace.</p>
    </div>
    """, unsafe_allow_html=True)

    # Save to Snowflake
    conn = init_snowflake()
    if conn:
        try:
            cursor = conn.cursor()
            insert_query = """
            INSERT INTO HAPPINESS_SURVEY (
                TIMESTAMP,
                MOOD,
                WORKS_AT_AG,
                HOW_GOT_CODE,
                IN_RED_TEAM,
                TEAM_NAME,
                JOB_WISH,
                STRESS_WISH,
                KNOWLEDGE_LAWYER_NEED,
                HAPPINESS_INTEREST
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, (
                datetime.now(),
                st.session_state.mood,
                st.session_state.works_at_ag,
                st.session_state.how_got_code,
                st.session_state.in_red,
                st.session_state.team_name,
                st.session_state.wish,
                st.session_state.stress_wish,
                st.session_state.knowledge_lawyer,
                st.session_state.happiness_interest
            ))
            conn.commit()
        except Exception as e:
            st.warning(f"Could not save to database: {e}")
        finally:
            conn.close()

    if st.session_state.happiness_interest:
        st.markdown("""
        <div class="form-section">
            <h3>🚀 Your Happiness Journey Starts Here</h3>
            <p>Shawn Achor's research shows that happiness is a skill we can develop.
            In his groundbreaking TED talk, he reveals the science behind the happiness advantage
            and how you can apply it to your career and life.</p>
            <p><strong>The 28-Day Happiness Advantage Program:</strong></p>
            <p>Build lasting habits that rewire your brain for positivity, resilience, and success.
            Our app guides you through daily practices based on Shawn Achor's proven research.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <a href="https://www.ted.com/talks/shawn_achor_the_happy_secret_to_better_work"
               target="_blank" class="link-button">Watch Shawn Achor's TED Talk</a>
            <a href="https://www.youtube.com/watch?v=fLJsdUxdkG0"
               target="_blank" class="link-button">View on YouTube</a>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="form-section">
            <h3>Start Your 21-Day Challenge</h3>
            <p>Ready to develop your happiness advantage? Our companion app offers:</p>
            <ul style="margin-left: 1.5rem; color: #666; line-height: 1.8;">
                <li><strong>Daily Insights</strong> from Shawn Achor's "The Happiness Advantage" & "Big Potential"</li>
                <li><strong>Guided Prompts</strong> to deepen your reflection</li>
                <li><strong>Progress Tracking</strong> to see how you're growing</li>
                <li><strong>Email Reminders</strong> at your preferred time</li>
                <li><strong>Community Support</strong> from colleagues on the same journey</li>
            </ul>
            <p style="margin-top: 1rem; color: #667eea; font-weight: 600;">
                "Success does not lead to happiness. Happiness leads to success." - Shawn Achor
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <a href="http://localhost:8501" target="_blank" class="link-button">Start 21-Day Journal</a>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="form-section">
            <h3>Thank you for your honest feedback</h3>
            <p>Even if happiness practices aren't for you right now, your insights about
            what would improve your work experience are invaluable. We'll use your feedback
            to make positive changes in our workplace.</p>
            <p style="margin-top: 1rem; color: #667eea; font-weight: 600;">
                If you change your mind, you're always welcome to explore our resources.
            </p>
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("← Go Back", use_container_width=True, key="back_7"):
            st.session_state.step = 6
            st.rerun()

    with col2:
        if st.button("Start Over", use_container_width=True, key="restart"):
            for key in st.session_state.keys():
                if key != "step":
                    del st.session_state[key]
            st.session_state.step = 1
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding: 2rem; color: #aaa; font-size: 0.9em;">
    <p>Made with ❤️ by Addleshaw Goddard | Powered by Shawn Achor's Happiness Research</p>
</div>
""", unsafe_allow_html=True)
