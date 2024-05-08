from datetime import datetime, date
from bs4 import BeautifulSoup
import aiohttp
from db import Currency, session
from openpyxl import Workbook


async def process_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    exchange_rate = soup.find('div', {'data-target': 'UAH'})['data-last-price']
    return str(round(float(exchange_rate), 4))


async def make_answer():
    url = 'https://www.google.com/finance/quote/USD-UAH'

    async with aiohttp.ClientSession() as http_session:
        async with http_session.get(url) as response:
            html_text = await response.text()
            exchange_rate = await process_html(html_text)
            datetime_now = datetime.now()
            currency = Currency(datetime=datetime_now, exchange_rate=exchange_rate)
            session.add(currency)
            session.commit()
            return datetime_now, exchange_rate


async def generate_excel():
    wb = Workbook()
    ws = wb.active

    ws['A1'] = 'datetime'
    ws['B1'] = 'exchange_rate'

    today_date = date.today()

    rows = session.query(Currency).filter(Currency.datetime == today_date).all()

    for idx, row in enumerate(rows, start=2):
        ws[f'A{idx}'] = row.datetime.strftime('%d.%m.%Y %H:%M:%S')
        ws[f'B{idx}'] = row.kurs

    excel_filename = f'exchange_rate_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx'
    wb.save(excel_filename)

    return excel_filename
