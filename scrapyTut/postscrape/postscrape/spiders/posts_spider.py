import scrapy

class PostSpider(scrapy.Spider):
    name = 'posts'
    start_urls = [
        'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=%D1%83%D1%84%D1%81%D0%B8%D0%BD&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&pageNumber=1&sortDirection=false&recordsPerPage=_50&showLotsInfoHidden=false&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&currencyIdGeneral=-1'
    ]

    def parse(self, response):
        for tender in response.css('div.search-registry-entry-block.box-shadow-search-input'):
            yield {
                'number': tender.css('div.registry-entry__header-mid__number a::text').get().strip().replace('\n', '').replace('\u2116 ', '')
            }
        next_page = response.css('a.paginator-button paginator-button-next::attr(href)').get()
        print(next_page)
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)