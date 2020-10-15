import requests
import random
import os
import logging
import time
import re
from bs4 import BeautifulSoup
from openpyxl import Workbook
from datetime import datetime
import yagmail

from config import from_email, password, to_emails2, bcc

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def save_results(res):
    wb = Workbook()
    ws = wb.active
    headers = ['Номер', 'Наименование', 'Время до окончания подачи предложений',
               'Заказчик', 'Стартовая цена', 'Информация о закупке']
    ws.append(headers)
    for tender_number, tender_info in res.items():
        ws.append([tender_number, tender_info['name'], tender_info['timer'],
                   tender_info['customer'], tender_info['price'], tender_info['info']])
        ws.column_dimensions['A'].width = 20
        ws.column_dimensions['B'].width = 100
        ws.column_dimensions['D'].width = 60
        ws.column_dimensions['E'].width = 20

    name = os.path.join(
        BASE_DIR, 'out', datetime.now().strftime("%d-%m-%Y_%H-%M"))
    results_file_name = name + '.xlsx'
    wb.save(results_file_name)
    return results_file_name

res = dict()
res['100163320120000065'] = {
    'name': 'Оказание услуг по разработке проектной документации для монтажа автоматической пожарной сигнализации и системы оповещения и управления людей при пожаре в здании',
    'timer': '23:05:37',
    'customer': 'ФКУ ИК-20 ГУФСИН РОССИИ ПО ПРИМОРСКОМУ КРАЮ',
    'price': '53 583, 00 руб.',
    'info': 'https://agregatoreat.ru/purchase/1472401/order-info'}

save_results(res)
