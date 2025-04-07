
import requests
from bs4 import BeautifulSoup

roster = 'https://ucsdtritons.com/sports/mens-soccer/roster'
roster2 = 'https://uclabruins.com/sports/mens-soccer/roster'
roster3 = 'https://gostanford.com/sports/mens-soccer/roster'
page = requests.get(roster3)
soup = BeautifulSoup(page.text, 'html.parser')

text = soup.get_text(separator=' ').replace('\n', ' ')

print(text)
