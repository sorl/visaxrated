import datetime
import requests
from bs4 import BeautifulSoup as Soup


RATES_URL = 'http://www.visaeurope.com/making-payments/exchange-rates'
CURRENCIES = ('AFN', 'ALL', 'DZD', 'AOA', 'ARS', 'AMD', 'AWG', 'AUD', 'AZN',
'BSD', 'BHD', 'BDT', 'BBD', 'BYR', 'BZD', 'BMD', 'BTN', 'BOB', 'BAM', 'BWP',
'BRL', 'GBP', 'BND', 'BGN', 'BIF', 'KHR', 'CAD', 'CVE', 'KYD', 'XOF', 'XAF',
'XPF', 'CLP', 'CNY', 'COP', 'KMF', 'CDF', 'CRC', 'HRK', 'CZK', 'DKK', 'DJF',
'DOP', 'EGP', 'SVC', 'GQE', 'ERN', 'EEK', 'ETB', 'EUR', 'FKP', 'FJD', 'GMD',
'GEL', 'GHS', 'GIP', 'GTQ', 'GNF', 'GWP', 'GYD', 'HTG', 'HNL', 'HKD', 'HUF',
'ISK', 'INR', 'IDR', 'IQD', 'JMD', 'JPY', 'JOD', 'KZT', 'KES', 'KWD', 'KGS',
'LAK', 'LVL', 'LBP', 'LSL', 'LRD', 'LYD', 'LTL', 'MRO', 'MOP', 'MKD', 'MGA',
'MWK', 'MYR', 'MVR', 'MTL', 'MUR', 'MXN', 'MDL', 'MNT', 'MAD', 'MZN', 'NAD',
'NPR', 'ANG', 'ILS', 'TWD', 'NZD', 'NIO', 'NGN', 'NOK', 'OMR', 'PKR', 'PGK',
'PYG', 'PEN', 'PHP', 'PLN', 'QAR', 'RON', 'RUB', 'RWF', 'ZAR', 'WST', 'STD',
'SAR', 'RSD', 'SCR', 'SLL', 'SGD', 'SBD', 'SOS', 'KRW', 'SSP', 'LKR', 'SHP',
'SDG', 'SRD', 'SZL', 'SEK', 'CHF', 'SYP', 'TJS', 'TZS', 'THB', 'TOP', 'TTD',
'TND', 'TRY', 'TMT', 'AED', 'UGX', 'UAH', 'USD', 'UYU', 'UZS', 'VUV', 'VEF',
'VND', 'YER', 'ZMK', 'ZMW')


class VisaxratedException(Exception):
    pass


def get_rate(card, trans, fee, date, amount):
    if card not in CURRENCIES:
        raise VisaxratedException('Card currency %s not available.' % card)
    if trans not in CURRENCIES:
        raise VisaxratedException('Transaction currency %s not available.' % trans)
    date = '17/11/2014'
    data = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        'ctl00$ctl00$ctl09$SearchBox$txtSearch': '',
        'ctl00$ctl00$ctl09$SearchBox2$txtSearch': '',
        'ctl00$ctl00$MainContent$MainContent$ctl00$ddlCardCurrency': card,
        'ctl00$ctl00$MainContent$MainContent$ctl00$ddlTransactionCurrency': trans,
        'ctl00$ctl00$MainContent$MainContent$ctl00$txtFee': fee,
        'ctl00$ctl00$MainContent$MainContent$ctl00$txtDate': date,
        'ctl00$ctl00$MainContent$MainContent$ctl00$txtAmount': amount,
        'ctl00$ctl00$MainContent$MainContent$ctl00$ctl02': '',
    }
    r = requests.get(RATES_URL)
    soup = Soup(r.text)
    form = soup.find('form', {'id': 'form1'})
    data = {}
    for inp in form.find_all('input', {'type': 'hidden'}):
        data[inp['id']] = inp['value']
    r = requests.post(RATES_URL, data=data)
    return r.text.encode('utf8')


def get_currencies():
    """
    Returns a list of tuples with ( Currency(3-letter capital), Readable name )
    of all availabale currencies
    """
    r = requests.get(RATES_URL)
    soup = Soup(r.text)
    sel = soup.find('select', {'id': 'MainContent_MainContent_ctl00_ddlCardCurrency'})
    currs = []
    for opt in sel.find_all('option'):
        if opt.string:
            currs.append((opt['value'], opt.string))
    return currs


if __name__ == '__main__':
    print get_rate('SEK', 'USD', 1.65, datetime.date(year=2014, month=11, day=17), 123)
