# Parallel Text Handling Processor

This Python project demonstrates the **difference between single processing and multiprocessing** using text file sentiment analysis.

📘Task1 : difference between single processing and multiprocessing
📌 Task1 Overview
The program:
1.Reads multiple text files  
2.Applies rule-based sentiment analysis  
3.Calculates sentiment scores  
4.Measures execution time for:
        - Single processing
        - Multiprocessing

It also saves all results to an `output.csv` file and compares performance.

## 📁 Files Included

- `reviews1.txt` … `reviews5.txt` — text files with product reviews  
- `task1.py` — Python script with analysis logic  
- `output.csv` — CSV with sentiment results  
- `README.md` — Project documentation

## 🚀 How It Works

1. Reads every review from text files
2. Applies a rule engine:
   - Positive keywords → +1
   - Negative keywords → −1
   - Neutral → 0
3. Runs single processing (one file after another)
4. Runs multiprocessing (parallel processes)
5. Saves output and compares time.


📘 Task2 – SQLite Students Database Project
📌 Task2 Overview

This project demonstrates how to:
Create a SQLite database using Python
Create a table
Insert records into the table
Retrieve and display stored data
It is a beginner-friendly database project using Python’s built-in sqlite3 module.

🛠 Technologies Used
Python 3
SQLite

sqlite3 (Built-in Python Library)
🗄 Database Information
Database Name: students.db
Table Name: students
📋 Table Structure
Column	Data Type	Description
id	      INTEGER	   Primary Key (Auto Increment)
name	   TEXT	      Student Name
age	   INTEGER	   Student Age
course	TEXT	      Course Name

📘 Task 3 – Sentiment Analysis on Amazon Product Reviews
📌 Task3 Overview

This project performs Rule-Based Sentiment Analysis on Amazon product reviews.
The dataset was taken from Kaggle (Amazon Product Reviews dataset).
The system:  Classifies reviews as Positive, Negative, or Neutral 
             Detects refund-related reviews
             Handles negation words like “not good”
             Stores results in a SQLite database

📂 Dataset
Source: Kaggle
Dataset: Amazon Product Reviews
Type: Text review data

🚀 Features
Text cleaning (lowercase + remove special characters)
Weighted sentiment scoring
Negation handling
Refund pattern detection
Multiprocessing for faster execution
SQLite database storage

Stored fields:
Review text
Sentiment (Positive / Negative / Neutral)
Refund flag (True / False)
Timestamp

🛠 Technologies Used
Python
SQLite
Regular Expressions
Multiprocessing

📘 Task 4 – Database Performance & Optimization
📌 Task4 Overview
This project is designed to test how indexing affects database performance.It measures query execution time before and after applying indexing to understand how optimization improves speed.

🔹 Step 1: Database Creation
First, a new SQLite database called performance_test.db is created.
Inside it, a table named reviews is created with the following columns:   id
                                                                          review_text
                                                                          sentiment_score
                                                                          sentiment_label
                                                                          created_at, At this stage, no indexes are added.
Purpose:
To measure how queries perform without any optimization.

🔹 Step 2: Generate Data
The program generates random review text using predefined positive and negative words.
Then it:
      Calculates the sentiment score
      Assigns a sentiment label (Positive, Negative, or Neutral)
Purpose:
To simulate real-world review data for performance testing.

🔹 Step 3: Insert 1,000,000 Records
The system inserts 1 million rows into the database.
It uses batch insertion (10,000 records at a time) to improve insertion performance.
Insertion time is measured.
Purpose:
To create a large dataset so that performance differences can be observed clearly.

🔹 Step 4: Run Queries (Before Optimization)
Several queries are executed, such as:
Counting positive reviews
Calculating average sentiment score
Fetching records with a specific score
The time taken to execute these queries is recorded.
This is called Query Time (Before Optimization).
Purpose:
To establish baseline performance.

🔹 Step 5: Apply Indexing
Indexes are created on:
sentiment_label
sentiment_score
Indexing creates a faster lookup structure, reducing the need to scan the entire table.
Purpose:
To improve query performance.

🔹 Step 6: Run Queries Again
The same queries are executed again after indexing.
The new execution time is recorded as Query Time (After Optimization).
Performance improvement is then calculated and compared.

📂Task 5: Multi File Viewer(textuploader)
Project Description
This project is a web application built using Streamlit.
It allows users to upload different types of files and view their content in one place.

After uploading files, the file names appear on the left side, and when a file is selected, its content is shown on the right side.
What This App Can Do
Upload multiple files at the same time
View text files
Read PDF documents
Open Word documents
Display Excel and CSV files as tables
Easily switch between uploaded files

Tools Used
Python
Streamlit
Pandas
PDF reader library
Word document reader library

How the App Works
The user uploads files using the upload option.
Uploaded files are listed on the left side.
The user selects a file from the list.
The app shows the file content on the right side.

Purpose of This Project
This project helps in learning:
File handling in Python
Building web apps using Streamlit
Working with different file formats
Creating interactive user interfaces

Future Improvements
Add search inside files
Add document summary feature
Support more file formats
Improve user interface design
