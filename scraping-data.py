import requests
from bs4 import BeautifulSoup
import pandas as pd

# url website
url = "https://www.detik.com"
 
# send request to website
response = requests.get(url)
if response.status_code == 200:
    print("request berita berhasil")
else:
    print("gagal mengakses request")

# parsing html 
soup = BeautifulSoup(response.text, 'lxml')

items_news = soup.find_all('article')
data = []

for item in items_news:
    title = item.find('h2').get_text(strip=True) if item.find('h2') else None
    link = item.find('a').get('href') if item.find('a') else None
    description = item.find('p').get_text(strip=True) if item.find('p') else None
    date = item.find('div', class_= 'detail__date').get_text(strip=True) if item.find('div', class_= 'detail__date') else None
    data.append({
        'Title': title,
        'Link': link,
        'Description': description,
        'Date': date,
    })

# saving data to DataFrame
df = pd.DataFrame(data)

# saving to CSV file
df.to_csv('news_items.csv', index=False)
print("Data berhasil menyimpan ke news_items.csv")