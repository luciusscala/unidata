import json
import sqlite3

# Load JSON data
with open('schools.json', 'r') as f:
    data = json.load(f)

# Connect to SQLite
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table with only name and domain
cursor.execute('''
CREATE TABLE IF NOT EXISTS universities (
    name TEXT,
    domain TEXT
)
''')

# Insert data
for uni in data:
    name = uni.get('name')
    domain = uni.get('domains', [None])[0]  # Get first domain if it exists

    cursor.execute('''
        INSERT INTO universities (name, domain)
        VALUES (?, ?)
    ''', (name, domain))

# Commit and close
conn.commit()
conn.close()
