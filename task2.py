import sqlite3

# Create / Connect to database
conn = sqlite3.connect("college.db")

cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    age INTEGER,
    course TEXT
)
""")

# Insert data
cursor.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
               ("Kulasri", 22, "MCA"))
cursor.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
               ("Surya", 21, "BSc"))
cursor.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
               ("BapiRaju", 22, "BSc"))
cursor.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
               ("Deepak", 25, "MSc"))
cursor.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
               ("Dinesh", 25, "BTech"))
cursor.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
               ("Deepika", 22, "MCA"))






# Commit changes
conn.commit()

# Fetch data
cursor.execute("SELECT * FROM students")
print(cursor.fetchall())

conn.close()