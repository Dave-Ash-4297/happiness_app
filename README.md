# Happiness App - Addleshaw Goddard

A comprehensive happiness and workplace wellness suite featuring a data collection landing page and 21-day journaling program, all powered by Shawn Achor's happiness research.

## 📱 What's Included

### 1. **Landing Page Survey** (`landing_page.py`)
A Streamlit app hosted on Snowflake that collects employee feedback:
- Captures mood and workplace satisfaction
- Conditional survey flow (different paths for AG vs. non-AG employees)
- Identifies which teams want happiness support
- Stores all responses in Snowflake for analytics
- Displays rotating motivational quotes
- Links to Shawn Achor's TED talk and 21-day program

**Perfect for:** Employee engagement surveys, QR code campaigns, workplace wellness initiatives

### 2. **21-Day Happiness Journal** (`happiness.py`)
A Streamlit app for personal development:
- Provides reminders to journal every day for 21 days
- Asks for preferred journal time and email address
- Securely stores journal entries in SQLite
- Sends daily email reminders with Shawn Achor insights
- Tracks progress through the Happiness Advantage principles
- Shows celebration stats upon completion

**Perfect for:** Individual transformation, building happiness habits, personal journaling

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Streamlit
- Snowflake account (for landing page)

### Installation

```bash
pip install -r requirements.txt
```

### Run Locally

**Landing Page (Survey):**
```bash
streamlit run landing_page.py
```

**21-Day Journal:**
```bash
streamlit run happiness.py
```

## 📊 Landing Page Features

- ✅ Multi-step conditional survey with branching logic
- ✅ Real-time data collection to Snowflake
- ✅ Mobile-optimized for QR code scanning
- ✅ Beautiful gradient UI with mood selectors
- ✅ Rotating quote ticker from "The Happiness Advantage"
- ✅ Analytics-ready data structure with pre-built views
- ✅ Seamless integration with 21-day journal program
- ✅ Sentiment analysis ready (mood tracking)

### Survey Questions Include:
1. How are you feeling today?
2. Do you work at Addleshaw Goddard?
3. Are you in the Real Estate Disputes team? (if AG)
4. What would make your job easier? (wish fulfillment)
5. What support does your team need?
6. Interested in developing happiness skills?

## 📖 21-Day Journal Features

- Daily insights from Shawn Achor's books
- Journaling prompts based on happiness principles
- Email reminders at your preferred time
- Progress tracking and statistics
- Session storage for daily continuity
- Celebration milestone (day 21 completion)

## 🎯 Deployment Options

### Option 1: Streamlit Cloud (Fastest)
See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for step-by-step instructions

### Option 2: Local Development
Perfect for testing and customization

### Option 3: Snowflake Native App
For enterprise deployments

## 🔧 Configuration

### Landing Page (Snowflake)
Create `.streamlit/secrets.toml`:
```toml
snowflake_user = "your_username"
snowflake_password = "your_password"
snowflake_account = "xy12345.us-east-1"
snowflake_warehouse = "COMPUTE_WH"
snowflake_database = "HAPPINESS_DB"
snowflake_schema = "PUBLIC"
```

### 21-Day Journal (Email)
Set environment variables for email reminders:
```bash
export EMAIL_SENDER="your-email@company.com"
export EMAIL_PASSWORD="your-app-password"
export APP_URL="http://localhost:8501"
```

## 📈 Analytics

The landing page creates three Snowflake views automatically:

### SURVEY_ANALYTICS
Daily aggregate metrics including:
- Response counts by mood
- Positive sentiment percentage
- Program interest rates

### TEAM_ANALYTICS
Team-level insights:
- Team happiness scores
- Interest by department
- Response patterns

### MOOD_TRENDS
Overall mood distribution and correlations

Query examples in [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## 📚 Data Structure

### Landing Page Data (Snowflake)
- Timestamp, mood, organization info
- Team assignment and role
- Job improvement wishes
- Knowledge lawyer needs
- Happiness program interest

### Journal Data (SQLite)
- Email address
- Password (hashed)
- Journal entries
- Dates and progress
- Preferred journal time

## 🎨 Customization

### Add More Quotes
Edit `HAPPINESS_QUOTES` in `landing_page.py` with quotes from:
- The Happiness Advantage
- Big Potential
- Before Happiness

### Change Colors
Modify CSS gradients in the style sections

### Customize Questions
Edit the step sections in `landing_page.py`

### Update Resources
Change TED talk links and journal app URLs

## 🔒 Security

✅ Snowflake credentials stored in secrets (never committed)
✅ Journal passwords hashed with SHA-256
✅ Dedicated Snowflake user with minimal permissions
✅ No sensitive data in client-side code

## 📊 Use Cases

### Company-Wide Wellness Initiative
- Deploy landing page to all employees
- Collect baseline happiness metrics
- Identify teams needing support
- Measure impact over time

### Team Development Program
- Use team wishes as agenda for team meetings
- Identify common pain points
- Track improvements across sprints

### Onboarding Enhancement
- Add survey link to new employee onboarding
- Measure initial engagement and satisfaction
- Personalize support based on responses

### Event/Conference
- Generate QR codes for lollipops or materials
- Collect real-time feedback from attendees
- Build happiness program interest list

## 📖 About Shawn Achor

All content is based on research from:
- **The Happiness Advantage** - How success follows happiness
- **Big Potential** - Amplifying your impact on others
- **Before Happiness** - Building the foundation for success

Resources:
- [TED Talk: The Happy Secret to Better Work](https://www.ted.com/talks/shawn_achor_the_happy_secret_to_better_work)
- [Official Website](https://www.shawnachor.com/)

## 🤝 Contributing

To improve or extend the apps:

1. Create a branch for your feature
2. Make changes and test locally
3. Submit a pull request with description
4. Include any new dependencies in requirements.txt

## 📝 File Structure

```
happiness_app/
├── landing_page.py           # Snowflake-hosted survey app
├── happiness.py              # 21-day journal app
├── snowflake_setup.sql       # Snowflake table initialization
├── DEPLOYMENT_GUIDE.md       # Complete deployment instructions
├── requirements.txt          # Python dependencies
├── .streamlit/
│   ├── config.toml          # Streamlit configuration
│   └── secrets.toml.example  # Example secrets template
└── README.md                 # This file
```

## 🚨 Troubleshooting

**Snowflake connection fails:**
- Verify credentials in `.streamlit/secrets.toml`
- Check account ID format: `xy12345.us-east-1`
- Confirm warehouse is active
- Check user permissions

**Email reminders not sending:**
- Verify EMAIL_SENDER and EMAIL_PASSWORD
- Use app-specific password for Gmail
- Check spam folder

**App runs slowly:**
- Ensure Snowflake warehouse is running
- Check network connectivity
- Verify table indexes are created

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for more solutions.

## 📞 Support

For questions about implementation or customization, refer to:
- Streamlit docs: [streamlit.io](https://streamlit.io/)
- Snowflake docs: [docs.snowflake.com](https://docs.snowflake.com/)
- Shawn Achor research: [shawnachor.com](https://www.shawnachor.com/)

---

**Made with ❤️ by Addleshaw Goddard**

Transforming workplace happiness through science-backed practices and data-driven insights.
