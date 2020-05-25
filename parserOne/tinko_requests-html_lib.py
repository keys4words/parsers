from requests_html import HTMLSession

session = HTMLSession()
url = 'https://www.tinko.ru/catalog/product/010002/'
r = session.get(url)

r.html.render(sleep=1, keep_page=True, scrolldown=1)
desc = r.html.find('.tovar-detail__description')
for item in desc:
    print(item.text)
