import requests

res = requests.get(url='http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html',
                   headers={
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
                   })
print(res.headers)
print('-'*32)
print(res.request.headers)