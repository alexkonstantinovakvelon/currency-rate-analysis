from currency_codes import CurrencyCodes
from datetime import datetime
from models.rate import Rate
from pyquery import PyQuery
from retry import retry
from settings import Settings
from typing import Iterable
import requests


class CurrencyRateDataProvider:
    def get_currency_rates(
            self,
            from_date: datetime,
            to_date: datetime,
            currency: str) -> Iterable[Rate]:
        currency_code = CurrencyCodes.get_code(currency)
        if currency_code is None:
            raise AssertionError('currency_code is not expected')
        content = self.__load_currency_rates_data__(
            from_date, to_date, currency_code)
        pq = PyQuery(content)
        table_content = pq('table.data')
        for tr in table_content('tr').items():
            tds = list(tr('td'))
            if len(tds) < 3:
                continue
            yield Rate(datetime.strptime(tds[0].text, '%d/%m/%Y').date(),
                       float(tds[2].text))

    @retry(ConnectionError, delay=2, jitter=2, tries=5)
    def __load_currency_rates_data__(
            self,
            from_date: datetime,
            to_date: datetime,
            currency_code: str) -> bytes:
        url = self.__build_url(from_date, to_date, currency_code)
        response = requests.get(url)
        if response.status_code != 200:
            raise ConnectionError()
        return response.content

    def __build_url(
            self,
            from_date:
            datetime,
            to_date: datetime,
            currency_code: str) -> str:
        q = '?{0}.{1}&{0}.VAL_NM_RQ={2}&{0}.FromDate={3}&{0}.ToDate={4}'
        query = q.format(
            'UniDbQuery',
            'Posted=True',
            currency_code,
            from_date.strftime(Settings.QUERY_DATE_FORMAT),
            to_date.strftime(Settings.QUERY_DATE_FORMAT))
        return '{0}{1}'.format(Settings.CBR_SERVICE_URL, query)
