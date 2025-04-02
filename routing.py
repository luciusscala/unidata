import requests
import sqlite3
from bs4 import BeautifulSoup


for i in range(1, 24):
    url = 'https://www.ncaa.com/schools-index'+i
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    #find the tables rows
    table = soup.find('table')
    rows = table.find_all('tr')[1:]

    #connect to database and establish cursor
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    for i in range(0, len(rows)):
        name = rows[i].find_all('td')[2].text.strip()
        link = rows[i].find_all('a')[0].get('href')
        cursor.execute('UPDATE schools SET route = ? WHERE name = ?', (link, name))

    # Commit changes to the database
    conn.commit()

# Close the cursor and the connection
cursor.close()
conn.close()
