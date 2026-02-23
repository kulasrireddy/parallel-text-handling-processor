# Parallel Text Handling Processor

This Python project demonstrates the **difference between single processing and multiprocessing** using text file sentiment analysis.

## 🧠 Task1 Overview

The program:

Reads multiple text files  
Applies rule-based sentiment analysis  
Calculates sentiment scores  
Measures execution time for:
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


📘 task2 – SQLite Students Database Project
📌 Project Overview

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

