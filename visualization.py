import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Connect to database
conn = sqlite3.connect("customer_feedbacks.db")

# Load cleaned feedbacks
query = "SELECT feedback FROM feedbacks;"  # Sentiment column hata diya
df = pd.read_sql_query(query, conn)

conn.close()

# Word Cloud Visualization
text = " ".join(df["feedback"])  # Join all feedbacks for visualization
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

# Plot
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Customer Feedback WordCloud")
plt.show()
