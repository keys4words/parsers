import xml.etree.ElementTree as et
import pprint
import csv

tree = et.parse('data/orders_(2020-05-25).xml')
root = tree.getroot()

orders = []

def get(list_elements):
    try:
        return list_elements.pop(0)
    except:
        return ''

for doc in root.iter('Документ'):
    order = {}
    for child in doc:
        if child.tag == 'Номер':
            order['id'] = child.text
        elif child.tag == 'Дата':
            order['date'] = child.text
        elif child.tag == 'Сумма':
            order['sums'] = child.text
            client_name = (doc.findall('./Контрагенты//ПолноеНаименование')[0]).text
            client_contacts = doc.findall('./Контрагенты//Контакты//Значение')
            contacts = ''
            for el in client_contacts:
                contacts += el.text + ' '
            order['client'] = ' '.join([client_name, contacts])
        elif child.tag == 'Товары':
            p_list = []
            for product in child:  #   moving via Товар/Товары
                res = ''
                for tags_product in product:   #   moving via теги товара
                    if tags_product.tag == 'Артикул':
                        res += tags_product.text + ' '
                    if tags_product.tag == 'Наименование' and tags_product.text != 'Доставка заказа':
                        res += tags_product.text + ' '
                        res += product.find('Количество').text + 'x'
                        res += product.find('ЦенаЗаЕдиницу').text
                if res != '':
                    p_list.append(res)
            order['product_list'] = p_list

    orders.append(order)

pprint.pprint(orders)

csv_file = "output/orders.csv"
csv_columns = ['client', 'date','id','product_list', 'sums']
try:
    with open(csv_file, 'w', encoding='cp1251', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in orders:
            writer.writerow(data)
except IOError:
    print("I/O error")
