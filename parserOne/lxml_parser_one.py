from lxml import  etree

# important!!!!
# replace all & to &amp; in xml

# parsing using a lxml etree
tree = etree.parse("C:/Users/keys4.000/Documents/4git/parsers/parserOne/data/web_page.html")
# print(etree.tostring(tree))
# title_element = tree.find('head/title')
# print(title_element.text)
# print(tree.find('body/p').text)
# list_items = tree.findall("body/ul/li")
# for item in list_items:
#     a = item.find('a')
#     if a is not None:
#         print(f'{item.text.strip()} {a.text}')
#     else:
#         print(item.text)

# parsing with cssselect lib
# html = tree.getroot()
# print(html)
# title_element = html.cssselect('title')[0]
# print(title_element.text)
# print((html.cssselect('p'))[0].text)
# list_items = html.cssselect("li")
# for item in list_items:
#     a = item.cssselect('a')
#     if len(a) == 0:
#         print(item.text)
#     else:
#         print(f'{item.text.strip()} {a[0].text}')
        
# parsing with xpath
title_element = tree.xpath('//title/text()')[0]
print(title_element)
print(tree.xpath('//p/text()')[0])
list_items = tree.xpath("//li")
for item in list_items:
    text = ''.join(map(str.strip, item.xpath('.//text()')))
    print(text)