from unicodedata import normalize
import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://knife.media/'
frontpage = requests.get(url)
parsed = BeautifulSoup(frontpage.text, "html.parser")

links = [link.get('href') for link in parsed.findAll('a') if 'content' in str(link)]

values = []
for link in links:
    art_page = requests.get(link)
    parsed_page = BeautifulSoup(art_page.text, "html.parser")

    title = parsed_page.find('h1').text
    time_tag = parsed_page.find('time')['datetime']
    content = "\n".join([normalize("NFKD", text.text)
                        for text in parsed_page.select(".entry-content>p, h2, .entry-header__lead>p")])

    values.append([link, title, content, time_tag])

df = pd.DataFrame(data=values, columns=["url", "title", "content", "date"])
df.to_csv('knife.csv')
