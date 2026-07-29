# Happiness Survey Landing Page - Deployment Guide

A Streamlit app for Snowflake that collects employee happiness data and workplace improvement feedback.

## Features

- 🎯 **Multi-step survey flow** with conditional branching
- 📊 **Real-time data collection** to Snowflake
- 💬 **Rotating quote ticker** featuring Shawn Achor's happiness principles
- 🎨 **Modern, responsive UI** optimized for mobile (QR code scanning)
- 🔗 **Integration with TED Talk** and 21-day happiness journal
- 📈 **Snowflake analytics views** for insights

## Survey Flow

1. **Mood Selection** - How are you feeling today?
2. **Organization Check** - Do you work at Addleshaw Goddard?
   - If Yes: Proceed to Real Estate Disputes check
   - If No: Capture how they got the QR code
3. **Team Information** - (Conditional based on AG status)
   - AG employees: Are you in Real Estate Disputes?
   - Non-AG: What team are you in?
4. **Job Improvement Wish** - What would make your role easier?
5. **Team Support** - What would help your team succeed?
6. **Happiness Interest** - Are you interested in learning about happiness advantages?
7. **Thank You** - Display resources based on interest

## Prerequisites

- Snowflake account with warehouse and database
- Python 3.8+
- Streamlit account (for hosting on Streamlit Cloud)
- OR local deployment capability

## Setup Instructions

### 1. Snowflake Configuration

**Step 1: Create Snowflake Objects**

Run the `snowflake_setup.sql` script in your Snowflake warehouse:

```sql
-- Execute all statements in snowflake_setup.sql
-- This creates:
-- - HAPPINESS_DB database
-- - HAPPINESS_SURVEY table
-- - Analytics views (SURVEY_ANALYTICS, TEAM_ANALYTICS, MOOD_TRENDS)
```

**Step 2: Create Snowflake User (Optional but Recommended)**

For security, create a dedicated Snowflake user:

```sql
-- In Snowflake with ACCOUNTADMIN role
CREATE USER STREAMLIT_APP
  PASSWORD = '<SECURE_PASSWORD>'
  DEFAULT_ROLE = HAPPINESS_ROLE;

CREATE ROLE HAPPINESS_ROLE;

-- Grant permissions
GRANT USAGE ON DATABASE HAPPINESS_DB TO ROLE HAPPINESS_ROLE;
GRANT USAGE ON SCHEMA HAPPINESS_DB.PUBLIC TO ROLE HAPPINESS_ROLE;
GRANT INSERT ON TABLE HAPPINESS_DB.PUBLIC.HAPPINESS_SURVEY TO ROLE HAPPINESS_ROLE;
GRANT SELECT ON VIEW HAPPINESS_DB.PUBLIC.SURVEY_ANALYTICS TO ROLE HAPPINESS_ROLE;
GRANT SELECT ON VIEW HAPPINESS_DB.PUBLIC.TEAM_ANALYTICS TO ROLE HAPPINESS_ROLE;
GRANT SELECT ON VIEW HAPPINESS_DB.PUBLIC.MOOD_TRENDS TO ROLE HAPPINESS_ROLE;

-- Grant role to user
GRANT ROLE HAPPINESS_ROLE TO USER STREAMLIT_APP;
```

### 2. Local Development

**Step 1: Clone and Setup**

```bash
cd happiness_app
pip install -r requirements.txt
```

**Step 2: Create `.streamlit/secrets.toml`**

Create `.streamlit/secrets.toml` in the project root:

```toml
snowflake_user = "your_username"
snowflake_password = "your_password"
snowflake_account = "xy12345.us-east-1"
snowflake_warehouse = "COMPUTE_WH"
snowflake_database = "HAPPINESS_DB"
snowflake_schema = "PUBLIC"
```

Find your Snowflake account ID:
- Log into Snowflake
- Check the URL: `https://<account_id>.snowflakecomputing.com`

**Step 3: Run Locally**

```bash
streamlit run landing_page.py
```

Visit `http://localhost:8501` in your browser.

### 3. Streamlit Cloud Deployment

**Step 1: Push to GitHub**

```bash
git add .
git commit -m "Add happiness survey landing page"
git push origin main
```

**Step 2: Deploy on Streamlit Cloud**

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository and branch
4. Set the main file path to `landing_page.py`
5. Click "Deploy"

**Step 3: Add Secrets**

In Streamlit Cloud app settings:
1. Go to App settings → Secrets
2. Add the same content as `.streamlit/secrets.toml`

```toml
snowflake_user = "your_username"
snowflake_password = "your_password"
snowflake_account = "xy12345.us-east-1"
snowflake_warehouse = "COMPUTE_WH"
snowflake_database = "HAPPINESS_DB"
snowflake_schema = "PUBLIC"
```

### 4. Snowflake Native App (Advanced)

For deploying as a Snowflake Native App:

1. Package the Streamlit app following Snowflake's guidelines
2. Create a manifest file
3. Deploy through Snowflake Marketplace or internal catalog

## Data Structure

### HAPPINESS_SURVEY Table

| Column | Type | Description |
|--------|------|-------------|
| ID | INTEGER | Auto-incrementing primary key |
| TIMESTAMP | TIMESTAMP | Survey submission time |
| MOOD | VARCHAR(50) | Current mood selection |
| WORKS_AT_AG | BOOLEAN | Whether respondent works at AG |
| HOW_GOT_CODE | VARCHAR(500) | How non-AG employees got the QR code |
| IN_RED_TEAM | BOOLEAN | Whether in Real Estate Disputes team |
| TEAM_NAME | VARCHAR(100) | Team name for non-RED employees |
| JOB_WISH | VARCHAR(2000) | RED team - job improvement wish |
| STRESS_WISH | VARCHAR(2000) | Non-RED - stress/job improvement wish |
| KNOWLEDGE_LAWYER_NEED | VARCHAR(2000) | Support needed for team success |
| HAPPINESS_INTEREST | BOOLEAN | Interest in 21-day program |
| CREATED_AT | TIMESTAMP | Record creation timestamp |

### Analytics Views

**SURVEY_ANALYTICS** - Daily aggregate metrics
- Response counts by mood
- Positive sentiment percentage
- Happiness program interest

**TEAM_ANALYTICS** - Team-level insights
- Response counts per team
- Team happiness scores
- Interest in happiness program by team

**MOOD_TRENDS** - Mood distribution
- Mood frequency and percentages
- Interest correlation by mood

## Customization

### Add More Quotes

Edit the `HAPPINESS_QUOTES` list in `landing_page.py`:

```python
HAPPINESS_QUOTES = [
    "Your custom quote here",
    "Another quote...",
    # Add more quotes from The Happiness Advantage
]
```

### Customize Colors

Modify the CSS in the `st.markdown()` style block:

```css
/* Primary gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Secondary gradient */
background: linear-gradient(135deg, #ffecd2, #fcb69f);
```

### Change Survey Questions

Edit the appropriate step sections to modify questions or add new fields.

### Connect to 21-Day Journal

Update the link in Step 7:

```python
<a href="YOUR_JOURNAL_URL" target="_blank" class="link-button">Start 21-Day Journal</a>
```

## Analytics Queries

### Get All Survey Responses

```sql
SELECT * FROM HAPPINESS_DB.PUBLIC.HAPPINESS_SURVEY
ORDER BY TIMESTAMP DESC;
```

### Happiness Score by Team

```sql
SELECT * FROM HAPPINESS_DB.PUBLIC.TEAM_ANALYTICS
ORDER BY TEAM_RESPONSES DESC;
```

### Daily Trends

```sql
SELECT * FROM HAPPINESS_DB.PUBLIC.SURVEY_ANALYTICS
ORDER BY SURVEY_DATE DESC;
```

### Employees Interested in Happiness Program

```sql
SELECT * FROM HAPPINESS_DB.PUBLIC.HAPPINESS_SURVEY
WHERE HAPPINESS_INTEREST = TRUE
ORDER BY TIMESTAMP DESC;
```

### Wishlist for Real Estate Disputes Team

```sql
SELECT TIMESTAMP, JOB_WISH, KNOWLEDGE_LAWYER_NEED
FROM HAPPINESS_DB.PUBLIC.HAPPINESS_SURVEY
WHERE IN_RED_TEAM = TRUE
ORDER BY TIMESTAMP DESC;
```

## Troubleshooting

### Snowflake Connection Fails

- Verify credentials in secrets file
- Check Snowflake account ID format (should be like `xy12345.us-east-1`)
- Confirm warehouse is active
- Ensure user has necessary permissions

### QR Code Integration

To generate QR codes pointing to your deployed app:

```python
pip install qrcode[pil]

import qrcode

qr = qrcode.QRCode()
qr.add_data("https://your-app-url.streamlit.app/")
qr.make()
img = qr.make_image()
img.save("happiness_qr.png")
```

Print and add to lollipops or materials!

## Performance Optimization

- The app caches Snowflake connection using `@st.cache_resource`
- Views pre-aggregate data for faster analytics queries
- Sessions are isolated - no performance impact from concurrent users

## Security Best Practices

✅ **Do:**
- Use secrets file for credentials (never hardcode)
- Create dedicated Snowflake user with limited permissions
- Use environment-specific credentials
- Rotate passwords regularly
- Monitor Snowflake query history

❌ **Don't:**
- Store passwords in code
- Use ACCOUNTADMIN role for app
- Share secrets files
- Commit `.streamlit/secrets.toml` to version control

## Support & Resources

- **Shawn Achor's TED Talk**: [The Happy Secret to Better Work](https://www.ted.com/talks/shawn_achor_the_happy_secret_to_better_work)
- **Streamlit Docs**: [streamlit.io/docs](https://docs.streamlit.io/)
- **Snowflake Docs**: [docs.snowflake.com](https://docs.snowflake.com/)
- **The Happiness Advantage**: [Book & Research](https://www.shawnachor.com/)

## Future Enhancements

- 📊 Dashboard for visualizing trends
- 📧 Email notifications for survey milestones
- 🔐 Anonymous response mode
- 🌍 Multi-language support
- 📱 Mobile app integration
- 🤖 AI-powered insights from free-text responses
- 🎯 Personalized recommendations based on mood/team
- 🔔 Real-time alerts for critical feedback

---

**Made with ❤️ by Addleshaw Goddard**
Powered by Shawn Achor's Happiness Research
