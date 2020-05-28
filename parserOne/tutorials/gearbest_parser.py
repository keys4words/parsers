import requests
from lxml import html
import pprint

script = '''
  headers = {
    ['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    ['cookie'] = 'gb_pipeline=GB; gb_countryCode=RU; gb_currencyCode=USD; gb_lang=en; gb_vsign=adb5f3894dfc6c9922a0e0bbff80f042018a0f06; AKAM_CLIENTID=d3a7fedeac621a30f576ca2f375c1dc8; landingUrl=https://www.gearbest.com/flash-sale.html; cdn_countryCode=RU; gb_fcm=0; gb_fcmPipeLine=GB; AKA_A2=A; ak_bmsc=8EBD569499110AC2ACAE810640F585EA02161F65F23F0000C98ACF5EEF155133~plpmTI34AfElxTea/Bt/3G1ANYVqPoPQzUvObRsAW37MO6wFkAI/boSAJUSHm4HviK0ZG/d79kwHWiQdPg5BndBefmTZyZ3phJSoiJ2PCaYanhSTwLx1yTZ6iY7W2GJ42b+ln2PqmUpFx+hpvp0toFyxJPR40WOJR7nAWPNBmtqQEfsHmfVuWNsYc7QC+h6tyxU+ACd/ymEX0YOFc94MdSKhGS0X2Fvv3L9fLmbn+kUdCc4cRGA3hRVhVfRoIek3i4; bm_sv=53ED75C8C7903484FE06DD43873CE7C0~HnFC93sYn2eJFrTKUwrvogp2AW1GuStojVC4IEBNxXifU67Bj99AKzt4BraXNUDBFLGjAdzs7J/UGAZVG6TR5+0b4TLiIle05unMze8bKxJI/DbnJW/Wfcw8E23x+7Ri0rxqnCX2DjPD7sP8/FJLUwvsuD/cMmbIdBA/eHZ/WMs=; gb_soa_www_session=eyJpdiI6IkROOHdSc2g4VlpMQnR6TXZ4N05reHc9PSIsInZhbHVlIjoia0E0QTdEeXlnVHhlbDBTRmpReXU1QmtlRUtERUJQT2tWWERjRm5cL2RXcDJrZXA5ajQwOWFhRHFQU1E2RDU5anp4NmdWVk5LY25SRnBRTWlNdFJtMHVRPT0iLCJtYWMiOiI4NWE1Y2QyZmI0YzRjYzYyMjlkODkzYTg3ODdlMzI5OWU2M2E5MjEwMzM4ZTA0ZGYzNDRjNDJlMGY4OWJlYTg0In0%3D'
  }
  splash:set_custom_headers(headers)
  splash.private_mode_enabled = false
  splash.images_enabled = false
  assert(splash:go(args.url))
  assert(splash:wait(1))
  return splash:html()
'''

products = []

resp = requests.post(url='http://localhost:8050/run',
                     json={
                         'lua_source': script,
                         'url': 'https://www.gearbest.com/flash-sale.html'
                     })
tree = html.fromstring(resp.content)
deals = tree.xpath('//li[contains(@class, "goodsItem")]/div[@class="goodsItem_content"]')
for deal in deals:
    product = {
        'name': deal.xpath('.//div[@class="goodsItem_title"]/a/text()')[0].strip(),
        'url': deal.xpath('.//div[@class="goodsItem_title"]/a/@href')[0],
        'original_price': deal.xpath('.//div[@class="goodsItem_delete"]/del/@data-currency'),
        'discounted_price': deal.xpath('.//div[@class="goodsItem_detail"]/span/@data-currency'),
    }
    products.append(product)

pprint.pprint(products)