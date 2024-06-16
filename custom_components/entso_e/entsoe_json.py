"""This is the new JSON API module. It works with Entso-E's new JSON API. It is 
recommended to use this module instead of entsoe.py. that does not seem to work anymore."""


import requests
from datetime import date, datetime, timedelta, timezone
from mock_response import MockResponse


CONST_REQUEST_URL = "https://web-api.tp.entsoe.eu/api"
CONST_DOC_TYPE = 'A44'

def call_api(api_token: str,
             area: str,
             date_from: date = date.today(),
             date_to: date = None) -> requests.Response:
    url = build_request_url(api_token, area, date_from, date_to)
    resp = requests.request("GET", url)
    return resp


def build_request_url(token: str,
                      area: str,
                      date_from: date = date.today(),
                      date_to: date = None) -> str:

    if date_to is None:
        date_to = date_from + timedelta(days=1)

    period_start = datetime(date_from.year, date_from.month, date_from.day).astimezone(timezone.utc).strftime('%Y%m%d%H%M')
    period_end = datetime(date_to.year, date_to.month, date_to.day).astimezone(timezone.utc).strftime('%Y%m%d%H%M')

    return f"{CONST_REQUEST_URL}?" \
           f"securityToken={token}&" \
           f"documentType={CONST_DOC_TYPE}&" \
           f"in_Domain={area}&" \
           f"out_Domain={area}&" \
           f"periodStart={period_start}&" \
           f"periodEnd={period_end}"


def parse_response(response:dict|requests.Response|MockResponse) -> dict:
    if isinstance(response, requests.Response) or isinstance(response, MockResponse):
        resp_json = response.json()
    elif isinstance(response, dict):
        resp_json = response
    else:
        pass  ## Should not happen

    # Parse response by status code
    status_code = resp_json.get('http_status_code', 0)

    if status_code == 0:
        return {'message': 'No status code in response'}

    elif status_code == 200:
        data = resp_json.get('data', None)
        if data is not None:
            return data
        
        error = resp_json.get('message', None)
        if error is not None:
            return {'message': error.get('text', 'Unknown Error')}

    elif status_code == 400:
        return {'message': resp_json.get('message', None).get('text', 'Unknown Error')}

    if status_code == 401:
        return {'message': resp_json.get('message', None).get('text', 'Unauthorized')}

    else:
        return {'message': 'Unknown Error'}


def get_timeseries_by_datetime(dt: datetime, parsed_resp: dict) -> list:
    if not parsed_resp.get('data'):
        return []
    s = parsed_resp.get('intervalStart')
    e = parsed_resp.get('intervalEnd')


if __name__ == '__main__':
    print('Only for use as module')
