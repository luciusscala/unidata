#this file is used to get the routes for the ncaa website that bring you to page with athletic website of school
import requests
import sqlite3
from bs4 import BeautifulSoup


#connect to database and establish cursor
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
total = 0
for i in range(1, 24):
    url = 'https://www.ncaa.com/schools-index/'+str(i)
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    #find the tables rows
    table = soup.find('table')
    rows = table.find_all('tr')[1:]
    for i in range(0, len(rows)):
        name = rows[i].find_all('td')[2].text.strip()
        link = rows[i].find_all('a')[0].get('href')

        cursor.execute('SELECT 1 FROM universities WHERE name = ?', (name,))
        result = cursor.fetchone()

        if result:
            cursor.execute('UPDATE universities SET route = ? WHERE name = ?', (link, name))
        else:
            print(f'School not found in database: {name}')
            total+=1
            print(total)

# Commit changes to the database
conn.commit()

# Close the cursor and the connection
cursor.close()
conn.close()
