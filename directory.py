import requests
import sqlite3
from bs4 import BeautifulSoup

#cleaning functions
def clean_domain(domain):
    if domain.startswith('http://www.'):
        return domain[11:]  # Strip the 'www.' prefix
    if domain.startswith('http://'):
        return domain[7:]
    return domain
def clean_website(url):
    if url.endswith('/landing/index'):
        return url[:-14]
    return url

# Connect to SQLite
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create table with only domain and website
cursor.execute('''
CREATE TABLE IF NOT EXISTS universities (
    website TEXT,
    domain TEXT
)
''')



for i in range(0,100):
    url = 'https://web3.ncaa.org/directory/orgDetail?id='+str(i)
    response = requests.get(url)

    #parse
    soup = BeautifulSoup(response.text, 'html.parser')

    #find all the links
    links = soup.find_all('a', class_='list-group-item')


    domains = []
    for link in links:
        href = link.get('href')
        if href and href != '#':
            domain = href
            domains.append(domain)

    # Get the first two relevant domains (institution + athletics)
    main_domain = clean_domain(domains[0]) if len(domains) > 0 else None
    athletics_domain = clean_website(domains[1]) if len(domains) > 1 else None

    if main_domain and athletics_domain:
        cursor.execute('''
            INSERT INTO universities (website, domain)
            VALUES (?, ?)
        ''', (athletics_domain, main_domain))


# Commit changes to the database
conn.commit()

# Close the cursor and the connection
cursor.close()
conn.close()

    
