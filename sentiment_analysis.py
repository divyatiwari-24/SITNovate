import sqlite3
import os
import groq
from dotenv import load_dotenv

# 🔹 Load API keys from .env file
dotenv_path = os.path.join(os.path.dirname(__file__), "twitter.env")
load_dotenv(dotenv_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# 🔹 Initialize Groq client
groq_client = groq.Client(api_key=GROQ_API_KEY)

# 🔹 Connect to SQLite database
conn = sqlite3.connect("customer_feedbacks.db")
cursor = conn.cursor()

# 🔹 Fetch feedback from database
cursor.execute("SELECT id, feedback FROM feedbacks")
feedbacks = cursor.fetchall()

# 🔹 Function to analyze sentiment
def analyze_sentiment(text):
    try:
        response = groq_client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "Analyze sentiment (positive, negative, neutral)."},
                {"role": "user", "content": text}
            ]
        )
        sentiment = response.choices[0].message.content.strip().lower()
        return sentiment
    except Exception as e:
        print(f"Error in Groq API: {e}")
        return "error"

# 🔹 Add sentiment column if not exists
cursor.execute("PRAGMA table_info(feedbacks);")
columns = [col[1] for col in cursor.fetchall()]
if "sentiment" not in columns:
    cursor.execute("ALTER TABLE feedbacks ADD COLUMN sentiment TEXT")
    conn.commit()

# 🔹 Process each feedback and store sentiment
for feedback_id, text in feedbacks:
    sentiment = analyze_sentiment(text)
    cursor.execute("UPDATE feedbacks SET sentiment = ? WHERE id = ?", (sentiment, feedback_id))
    conn.commit()

# 🔹 Close connection
conn.close()

print("✅ Sentiment analysis completed & stored in database!")
