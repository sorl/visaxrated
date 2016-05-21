import requests
from bs4 import BeautifulSoup as Soup


RATES_URL = 'https://www.visaeurope.com/making-payments/exchange-rates'
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


def xrate(card, trans, fee, date, amount):
    """
    Returns the exchenge rate (amount) from Visa.
    """
    if card not in CURRENCIES:
        raise VisaxratedException('Card currency %s not available.' % card)
    if trans not in CURRENCIES:
        raise VisaxratedException('Transaction currency %s not available.' % trans)
    date = date.strftime('%d/%m/%Y')
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
        'ctl00$ctl00$MainContent$MainContent$ctl00$btnSubmit': '',
    }
    headers = {
        'Referer': RATES_URL,
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36',
    }
    r = requests.get(RATES_URL, headers=headers)
    soup = Soup(r.text, 'html.parser')
    form = soup.find('form', {'id': 'form1'})
    for inp in form.find_all('input', {'type': 'hidden'}):
        data[inp['id']] = inp['value']
    r = requests.post(RATES_URL, data=data, headers=headers)
    soup = Soup(r.text, 'html.parser')
    main = soup.find('main')
    div = main.find_all('div', {'class': 'col-lg-12'})[1]
    return float(div.find_all('strong')[1].text.replace(',', ''))


def currencies():
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
