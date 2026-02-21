import sqlite3
import json
import re
import os
from datetime import datetime
from multiprocessing import Pool, cpu_count

# =====================================================
# SENTIMENT DICTIONARIES
# =====================================================
POSITIVE_WORDS = {
    "good": 1, "great": 2, "excellent": 3, "amazing": 3,
    "love": 2, "perfect": 3, "nice": 1, "happy": 1,
    "useful": 1, "best": 3, "works": 1
}

NEGATIVE_WORDS = {
    "bad": -1, "poor": -2, "terrible": -3, "worst": -3,
    "hate": -2, "awful": -3, "disappointed": -2,
    "junk": -2, "cheap": -1
}

NEGATIONS = {"not", "never", "no"}
INTENSIFIERS = {"very", "extremely", "really"}
DIMINISHERS = {"slightly", "little"}
CONTRAST_WORDS = {"but", "however", "although"}

POSITIVE_EMOJIS = {"😊", "😍", "👍", "😁", "🔥"}
NEGATIVE_EMOJIS = {"😡", "😢", "👎", "😭"}

SARCASM_PATTERNS = {"yeah right", "as if", "just great"}

invalid_records = 0

# =====================================================
# CLEANING
# =====================================================
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    return text


# =====================================================
# STAR PREDICTION
# =====================================================
def predict_star(score):
    if score <= -3:
        return 1
    elif -2 <= score <= -1:
        return 2
    elif score == 0:
        return 3
    elif 1 <= score <= 3:
        return 4
    else:
        return 5


# =====================================================
# REVIEW PROCESSING
# =====================================================
def process_review(line):
    global invalid_records

    line = line.strip()
    if not line:
        return None

    try:
        item = json.loads(line)
    except json.JSONDecodeError:
        invalid_records += 1
        return None

    try:
        reviewer_id = item.get("reviewerID", "")
        reviewer_name = item.get("reviewerName", "Unknown")
        asin = item.get("asin", "")
        helpful = item.get("helpful", [0, 0])
        summary = item.get("summary", "")
        review_text = item.get("reviewText", "")
        actual_rating = item.get("overall", None)
        unix_time = item.get("unixReviewTime")

        timestamp = datetime.fromtimestamp(unix_time) if unix_time else datetime.now()

        review_id = f"{reviewer_id}_{unix_time}"

        cleaned = clean_text(review_text)
        words = cleaned.split()

        score = 0
        i = 0

        while i < len(words):
            word = words[i]

            if word in NEGATIONS and i + 1 < len(words):
                next_word = words[i + 1]
                if next_word in POSITIVE_WORDS:
                    score -= POSITIVE_WORDS[next_word]
                elif next_word in NEGATIVE_WORDS:
                    score -= NEGATIVE_WORDS[next_word]
                i += 2
                continue

            if word in INTENSIFIERS and i + 1 < len(words):
                next_word = words[i + 1]
                if next_word in POSITIVE_WORDS:
                    score += POSITIVE_WORDS[next_word] * 2
                elif next_word in NEGATIVE_WORDS:
                    score += NEGATIVE_WORDS[next_word] * 2
                i += 2
                continue

            if word in DIMINISHERS and i + 1 < len(words):
                next_word = words[i + 1]
                if next_word in POSITIVE_WORDS:
                    score += POSITIVE_WORDS[next_word] * 0.5
                elif next_word in NEGATIVE_WORDS:
                    score += NEGATIVE_WORDS[next_word] * 0.5
                i += 2
                continue

            if word in CONTRAST_WORDS:
                score *= 0.5

            if word in POSITIVE_WORDS:
                score += POSITIVE_WORDS[word]
            elif word in NEGATIVE_WORDS:
                score += NEGATIVE_WORDS[word]

            i += 1

        # Emoji handling
        for emoji in POSITIVE_EMOJIS:
            if emoji in review_text:
                score += 2
        for emoji in NEGATIVE_EMOJIS:
            if emoji in review_text:
                score -= 2

        # Sarcasm
        for pattern in SARCASM_PATTERNS:
            if pattern in cleaned:
                score *= -1

        if score > 1:
            sentiment = "Positive"
        elif score < -1:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        predicted_star = predict_star(score)

        reputation_score = score

        return (
            review_id,
            reviewer_id,
            reviewer_name,
            asin,
            review_text,
            summary,
            helpful[0],
            helpful[1],
            score,
            sentiment,
            predicted_star,
            actual_rating,
            reputation_score,
            timestamp
        )

    except:
        invalid_records += 1
        return None


# =====================================================
# MAIN PROCESSING
# =====================================================
def process_dataset(file_path):

    if not os.path.exists(file_path):
        print("File not found!")
        return

    conn = sqlite3.connect("amazon_intelligence.db")
    cursor = conn.cursor()

    # NORMALIZED TABLES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviewers (
            reviewer_id TEXT PRIMARY KEY,
            reviewer_name TEXT,
            reputation_score REAL DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            asin TEXT PRIMARY KEY
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            review_id TEXT PRIMARY KEY,
            reviewer_id TEXT,
            asin TEXT,
            review_text TEXT,
            summary TEXT,
            helpful_yes INTEGER,
            helpful_total INTEGER,
            score REAL,
            sentiment TEXT,
            predicted_star INTEGER,
            actual_rating REAL,
            timestamp DATETIME,
            FOREIGN KEY(reviewer_id) REFERENCES reviewers(reviewer_id),
            FOREIGN KEY(asin) REFERENCES products(asin)
        )
    """)

    conn.commit()

    with open(file_path, "r", encoding="utf-8") as file:
        pool = Pool(cpu_count())
        results = pool.map(process_review, file)
        pool.close()
        pool.join()

    results = [r for r in results if r is not None]

    for r in results:
        cursor.execute("INSERT OR IGNORE INTO reviewers VALUES (?, ?, ?)",
                       (r[1], r[2], r[12]))

        cursor.execute("INSERT OR IGNORE INTO products VALUES (?)",
                       (r[3],))

        cursor.execute("""
            INSERT OR IGNORE INTO reviews
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (r[0], r[1], r[3], r[4], r[5], r[6], r[7],
              r[8], r[9], r[10], r[11], r[13]))

    conn.commit()

    # =====================================================
    # PRODUCT ANALYTICS
    # =====================================================
    print("\nTop 5 Positive Products:")
    cursor.execute("""
        SELECT asin, AVG(score) as avg_score
        FROM reviews
        GROUP BY asin
        ORDER BY avg_score DESC
        LIMIT 5
    """)
    print(cursor.fetchall())

    print("\nTop 5 Negative Products:")
    cursor.execute("""
        SELECT asin, AVG(score) as avg_score
        FROM reviews
        GROUP BY asin
        ORDER BY avg_score ASC
        LIMIT 5
    """)
    print(cursor.fetchall())

    # =====================================================
    # REVIEWER ANALYTICS
    # =====================================================
    print("\nMost Active Reviewers:")
    cursor.execute("""
        SELECT reviewer_id, COUNT(*)
        FROM reviews
        GROUP BY reviewer_id
        ORDER BY COUNT(*) DESC
        LIMIT 5
    """)
    print(cursor.fetchall())

    # =====================================================
    # ACCURACY
    # =====================================================
    cursor.execute("SELECT predicted_star, actual_rating FROM reviews")
    rows = cursor.fetchall()

    correct = 0
    total = 0

    for pred, actual in rows:
        if actual is not None:
            total += 1
            if int(pred) == int(actual):
                correct += 1

    if total > 0:
        accuracy = (correct / total) * 100
        print(f"\nModel Accuracy: {accuracy:.2f}%")

    conn.close()

    print(f"\nSkipped {invalid_records} corrupted records")
    print("Processing Completed Successfully!")


if __name__ == "__main__":
    process_dataset("Cell_Phones_and_Accessories_5.json")