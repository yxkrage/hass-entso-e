import aiohttp
from typing import Union
from datetime import date, datetime, timedelta, timezone
from .parsers import EntsoeResponseParser
from .http_response import HttpResponse


class Entsoe:
    def __init__(
        self,
        api_key: str,
        area: str, 
        date_from: Union[date, str], 
        date_to: Union[date, str, None] = None,
        session_cls = None  # Allow dependency injection for testing
    ):
        self.api_key = api_key
        self.area = area
        if isinstance(date_from, str):
            self.date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
        elif isinstance(date_from, date):
            self.date_from = date_from
        else:
            raise ValueError('date_from must be str or date')

        if isinstance(date_to, str):
            self.date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
        elif isinstance(date_to, date) or date_to is None:
            self.date_to = date_to
        else:
            raise ValueError('date_to must be str, date or None')

        if session_cls is None:
            self.session_cls = aiohttp.ClientSession
        else:
            self.session_cls = session_cls

        self.CONST_REQUEST_URL = "https://web-api.tp.entsoe.eu/api"
        self.CONST_DOC_TYPE = 'A44'
        self.response = None
        self.response_data = None


    async def async_call_api(self) -> HttpResponse:
        url = self.request_url()
        timeout = aiohttp.ClientTimeout(total=30)  # Set timeouts for safety
        # async with aiohttp.ClientSession(timeout=timeout) as session:
        async with self.session_cls(timeout=timeout) as session:
            async with session.get(url) as resp:
                data = await resp.text()
                code = resp.status
        self.response = HttpResponse(code, data)
        return self.response 


    async def async_get_result(self) -> dict:
        if self.response is None:
            await self.async_call_api()
        resp = self.parse_response()
        return resp


    def request_url(self):
        if self.date_to is None:
            self.date_to = self.date_from + timedelta(days=1)

        period_start = datetime(
            year=self.date_from.year,
            month=self.date_from.month,
            day=self.date_from.day) \
        .astimezone(timezone.utc).strftime('%Y%m%d%H%M')

        period_end = datetime(
            year=self.date_to.year,
            month=self.date_to.month,
            day=self.date_to.day) \
        .astimezone(timezone.utc).strftime('%Y%m%d%H%M')

        return f"{self.CONST_REQUEST_URL}?" \
            f"securityToken={self.api_key}&" \
            f"documentType={self.CONST_DOC_TYPE}&" \
            f"in_Domain={self.area}&" \
            f"out_Domain={self.area}&" \
            f"periodStart={period_start}&" \
            f"periodEnd={period_end}"


    def parse_response(self) -> dict:
        parser = EntsoeResponseParser.parser_factory(self.response)
        self.response_data = parser.parse_response()
        return self.response_data


if __name__ == '__main__':
    raise(Exception('Only for use as module'))
