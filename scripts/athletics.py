#this will be used to retrieve a roster from a certain school.SEL

import requests
import sqlite3
from bs4 import BeautifulSoup

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("SELECT id, route FROM schools")
rows = cursor.fetchall()

for row in rows:
    route = row[1]
    
    url = 'https://www.ncaa.com'+str(route)
    response = requests.get(url)
    print(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    icon_web = soup.find('span', class_='icon-web')
    if icon_web is None:
        continue
    website_name = icon_web.find_next_sibling("span", class_="info").text.strip()
    cursor.execute('UPDATE schools SET athletics = ? WHERE route = ?', (website_name, route))

# Commit changes to the database
conn.commit()

# Close the cursor and the connection
cursor.close()
conn.close()

