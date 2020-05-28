import requests, re, json, csv, click
from lxml import html

def get_digit(x):
    if x.isdigit():
        return x

def write_to_csv(filename, data):
    headers = ['title', 'price', 'in_stock', 'description']
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers, delimiter=';')
        writer.writeheader()
        writer.writerow(data)

def write_to_json(filename, data):
    with open(filename, 'w') as f:
        f.write(json.dumps(data))

@click.command()
@click.option('--bookurl', default='http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html', help='Enter url of book for scraping')
@click.option('--filename', default='output/book.json', help='Enter filename for saving data with JSON/CSV extension')
def scrape(bookurl, filename):
    res = requests.get(url=bookurl,
                       headers={
                           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
                       })

    tree = html.fromstring(html=res.text)
    scraping_book = tree.xpath('//div[contains(@class, "product_main")]')[0]
    title = scraping_book.xpath('.//h1/text()')[0]
    price = scraping_book.xpath('.//p[1]/text()')[0].replace('Â£', '£')
    availability = scraping_book.xpath('.//p[2]/text()')[1].strip()
    # in_stock = re.compile(r"\d+").findall(availability)[0]
    # in_stock = ''.join(list(filter(get_digit,availability)))
    in_stock = ''.join(list(filter(lambda x: x.isdigit(), availability)))
    description = tree.xpath('//div[@id="product_description"]/following-sibling::p/text()')[0]
    book = {
        'title': title,
        'price': price,
        'in_stock': in_stock,
        'description': description
    }
    extension = filename.split('.')[1]
    if extension == 'json':
        write_to_json('output/' + filename, book)
    elif extension == 'csv':
        write_to_csv('output/' + filename, book)
    else:
        click.echo('Your extension of file is NOT supported!')
    print('Done')


if __name__=='__main__':
    scrape()

