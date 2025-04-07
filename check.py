from fastapi import FastAPI, HTTPException
import sqlite3
import requests
from bs4 import BeautifulSoup

app = FastAPI()

@app.post('/verify')
def verify(email: str, name: str):
    #get domain
    domain = email.split('@')[-1]

    #check databse
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT website FROM new WHERE domain = ?", (domain,))
    result = cursor.fetchone()
    conn.close()

    #if domain is not found
    if not result:
        raise HTTPException(status_code=404, detail='School not found')
    
    website = result[0]
    roster = website + '/sports/mens-soccer/roster'

    #get the roster names
    try:
        page = requests.get(roster)
        soup = BeautifulSoup(page.text, 'html.parser')
    except Exception:
        raise HTTPException(status_code=500, detail='Failed to fetch roster')
    
    if name.lower() in soup.get_text().lower():
        return {"status": "valid"}
    else:
        return {"status": "invalid"}

