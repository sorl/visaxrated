
visaxrated
==========
Get exchange rates for Visa.
Arguments: Card currency, Transaction currency, Fee (percent), Date, Amount

    >>> import datetime
    >>> from visaxrated import xrate
    >>> xrate('SEK', 'USD', 1.65, datetime.date(year=2014, month=10, day=16), 40)
    296.228298328
