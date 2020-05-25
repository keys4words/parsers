import requests, json
from fake_useragent import UserAgent
import pprint
from urllib.parse import urljoin
import sqlite3


ua = UserAgent()
res = []

def scrape(pageNumber=1):
    url = "https://www.walgreens.com/productsearch/v1/products/search"


    payload = {"p":pageNumber,"s":24,"view":"allView","geoTargetEnabled":False,"abtest":["tier2","showNewCategories"],"deviceType":"desktop","id":["350006"],"requestType":"tier3","sort":"Top Sellers","couponStoreId":"15196"}
    headers = {
        'content-type': 'application/json',
        'user-agent': ua.random
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    data = response.json()

    try:
        products = data['products']
        for product in products:
            pr_info = product['productInfo']
            pr = {
                'img': pr_info['imageUrl'],
                'price': pr_info['priceInfo']['regularPrice'],
                'id': pr_info['prodId'],
                'name': pr_info['productDisplayName'],
                'size': pr_info['productSize'],
                'url': urljoin(base='https://www.walgreens.com', url=pr_info['productURL'])
            }
            res.append(pr)

        pageNumber += 1
        scrape(pageNumber=pageNumber)
    except KeyError:
        return None

scrape()
# pprint.pprint(res)
connection = sqlite3.connect("walgreens.db")
cursor = connection.cursor()
try:
    cursor.execute('''
        CREATE TABLE products (
            id TEXT PRIMARY KEY,
            name TEXT,
            url TEXT,
            size TEXT,
            price TEXT,
            image TEXT
        )
    ''')
    connection.commit()
except sqlite3.OperationalError as e:
    print(e)

for product in res:
    try:
        cursor.execute('''
            INSERT INTO products (id, name, url, size, price, image) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            product['id'],
            product['name'],
            product['url'],
            product['size'],
            product['price'],
            product['img'],
        ))
    except sqlite3.IntegrityError:
        pass

connection.commit()
connection.close()

print(f'{len(res)} items successfully scraped')
