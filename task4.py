# ============================================================
# PERFORMANCE & OPTIMIZATION TEST
# ============================================================

import sqlite3
import time
import random
from datetime import datetime

DB_NAME = "performance_test.db"

# ============================================================
# STEP 1: Setup Database
# ============================================================

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Drop table if exists (fresh benchmark)
    cursor.execute("DROP TABLE IF EXISTS reviews")

    # Create table (NO indexes initially)
    cursor.execute("""
    CREATE TABLE reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        review_text TEXT,
        sentiment_score INTEGER,
        sentiment_label TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()

    print("Step 1 Completed: Database Initialized")


# ============================================================
# STEP 2: Sentiment Rules
# ============================================================

POSITIVE_WORDS = {
    "good": 1, "great": 2, "excellent": 3,
    "amazing": 3, "love": 2
}

NEGATIVE_WORDS = {
    "bad": -1, "poor": -2,
    "terrible": -3, "hate": -2
}


def generate_and_score():
    sample_words = list(POSITIVE_WORDS.keys()) + list(NEGATIVE_WORDS.keys())
    text = " ".join(random.choices(sample_words, k=10))

    score = 0
    for word in text.split():
        score += POSITIVE_WORDS.get(word, 0)
        score += NEGATIVE_WORDS.get(word, 0)

    if score > 0:
        label = "Positive"
    elif score < 0:
        label = "Negative"
    else:
        label = "Neutral"

    return (text, score, label, datetime.now().isoformat())


# ============================================================
# STEP 3: Insert 1 Million Records (Batch Insert)
# ============================================================

def process_and_insert():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    total_records = 1_000_000
    batch_size = 10000

    start_time = time.time()

    for _ in range(0, total_records, batch_size):

        batch = []
        for _ in range(batch_size):
            batch.append(generate_and_score())

        cursor.executemany("""
            INSERT INTO reviews
            (review_text, sentiment_score, sentiment_label, created_at)
            VALUES (?, ?, ?, ?)
        """, batch)

        conn.commit()

    end_time = time.time()

    # Verify insertion
    cursor.execute("SELECT COUNT(*) FROM reviews")
    total_rows = cursor.fetchone()[0]

    print("Total Rows Inserted:", total_rows)
    print("Insertion Time:", round(end_time - start_time, 2), "seconds")

    conn.close()


# ============================================================
# STEP 4: Benchmark Queries
# ============================================================

def run_queries():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    queries = [
        "SELECT COUNT(*) FROM reviews WHERE sentiment_label='Positive'",
        "SELECT AVG(sentiment_score) FROM reviews",
        "SELECT * FROM reviews WHERE sentiment_score = 3"
    ]

    start = time.time()

    for q in queries:
        cursor.execute(q)
        cursor.fetchall()

    end = time.time()

    conn.close()

    return round(end - start, 2)


# ============================================================
# STEP 5: Apply Index Optimization
# ============================================================

def apply_optimization():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("CREATE INDEX idx_label ON reviews(sentiment_label)")
    cursor.execute("CREATE INDEX idx_score ON reviews(sentiment_score)")

    conn.commit()
    conn.close()

    print("Indexing Applied Successfully")


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":

    # Step 1: Setup
    setup_database()

    # Step 2: Insert Data
    process_and_insert()

    # Step 3: Benchmark BEFORE optimization
    before_time = run_queries()
    print("Query Time (Before Optimization):", before_time, "seconds")

    # Step 4: Apply Index
    apply_optimization()

    # Step 5: Benchmark AFTER optimization
    after_time = run_queries()
    print("Query Time (After Optimization):", after_time, "seconds")

    # Step 6: Compare Results
    improvement = ((before_time - after_time) / before_time) * 100

    print("\nFinal Performance Report")
    print("Before Optimization:", before_time, "seconds")
    print("After Optimization:", after_time, "seconds")
    print("Performance Improvement:", round(improvement, 2), "%")