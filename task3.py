import os
import re
import sqlite3
from datetime import datetime
from multiprocessing import Pool, cpu_count

# ---------------------------
# Sentiment Scoring Dictionary
# ---------------------------
SCORES = {
    "good": 1,
    "great": 2,
    "excellent": 3,
    "happy": 1,
    "satisfied": 2,
    "bad": -1,
    "poor": -2,
    "sad": -1,
    "terrible": -3,
    "worst": -3,
    "refund": -2,
    "return": -1,
    "damaged": -2,
    "broken": -2
}

NEGATIONS = {"not", "never", "no", "hardly"}

REFUND_PATTERNS = [
    r"\brefund\b",
    r"\breturn\b",
    r"\bmoney back\b",
    r"\breplacement\b"
]

# ---------------------------
# Text Cleaning Function
# ---------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    return text


# ---------------------------
# Sentiment Analysis Function
# ---------------------------
def analyze_review(review):
    try:
        cleaned = clean_text(review)
        words = cleaned.split()

        score = 0
        i = 0

        while i < len(words):
            word = words[i]

            # Negation Handling
            if word in NEGATIONS and i + 1 < len(words):
                next_word = words[i + 1]
                if next_word in SCORES:
                    score -= SCORES[next_word]
                    i += 2
                    continue

            if word in SCORES:
                score += SCORES[word]

            i += 1

        # Refund Pattern Detection
        refund_flag = any(re.search(pattern, cleaned) for pattern in REFUND_PATTERNS)

        # Final Sentiment Decision
        if score > 0:
            sentiment = "Positive"
        elif score < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        return (review, sentiment, refund_flag)

    except Exception:
        return None


# ---------------------------
# Database Setup
# ---------------------------
def create_database():
    conn = sqlite3.connect("reviews.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        review TEXT,
        sentiment TEXT,
        refund_flag BOOLEAN,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


# ---------------------------
# Insert into Database
# ---------------------------
def insert_reviews(results):
    conn = sqlite3.connect("reviews.db")
    cursor = conn.cursor()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for result in results:
        if result is not None:
            review, sentiment, refund_flag = result
            cursor.execute("""
            INSERT INTO reviews (review, sentiment, refund_flag, created_at)
            VALUES (?, ?, ?, ?)
            """, (review, sentiment, refund_flag, current_time))

    conn.commit()
    conn.close()


# ---------------------------
# Main Processing Function
# ---------------------------
def process_reviews(review_list):
    with Pool(cpu_count()) as pool:
        results = pool.map(analyze_review, review_list)

    valid_results = [r for r in results if r is not None]
    corrupted_count = len(results) - len(valid_results)

    insert_reviews(valid_results)

    print("Processing Completed Successfully!")
    print(f"Skipped {corrupted_count} corrupted records")


# ---------------------------
# Sample Reviews
# ---------------------------
if __name__ == "__main__":
    create_database()

    reviews = [
        "The product is excellent and I am very happy",
        "Worst quality, I want refund immediately",
        "Not good at all",
        "The item was damaged and broken",
        "Great service and satisfied with delivery",
        "I need money back for this poor product"
    ]

    process_reviews(reviews)
