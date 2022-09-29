import requests
from urllib.parse import quote as url_encode
import xml.etree.ElementTree as et
from datetime import date, datetime, timedelta


CONST_REQUEST_URL = "https://web-api.tp.entsoe.eu/api"
CONST_XML_NS = 'xmlns'


def call_api(api_token: str,
             area: str,
             date_from: date = date.today(),
             date_to: date = None) -> requests:
    url = build_request_url(api_token, area, date_from, date_to)
    resp = requests.request("GET", url)
    return resp


def build_request_url(token: str,
                      area: str,
                      date_from: date = date.today(),
                      date_to: date = None) -> str:

    if date_to is None:
        date_to = date_from + timedelta(days=1)

    time_int = url_encode(
        datetime(date_from.year, date_from.month, date_from.day).astimezone().isoformat(timespec='minutes') +
        "/" +
        datetime(date_to.year, date_to.month, date_to.day).astimezone().isoformat(timespec='minutes'))

    return f"{CONST_REQUEST_URL}?" \
           f"securityToken={token}&" \
           f"documentType=A44&" \
           f"in_Domain={area}&" \
           f"out_Domain={area}&" \
           f"TimeInterval={time_int}"


def parse_response(response):
    # Parse response body according to response type
    ret_key = 'message' # Tag to use in return structure
    if response.status_code == 401:
        ret = parse_response_401(response.text)

    elif response.status_code in [200, 400]:
        root = et.fromstring(response.text)
        ns, tag = root.tag[1:].split('}')  # Get NS from tag
        xml_ns = {CONST_XML_NS: ns}

        if tag == 'Publication_MarketDocument':
            ret = parse_response_publication_market_document(response.text, xml_ns)
            ret_key = "data"  # Update to 'data'. All other cases are 'message'
        elif tag == 'Acknowledgement_MarketDocument':
            ret = parse_response_acknowledgement_market_document(response.text, xml_ns)
        else:
            ret = {'text': f'Unknown response dokument type ({tag})'}
    else:
        ret = {'text': 'Unknown Error'}

    # Wrap and return response
    return {'http_status_code': response.status_code,
            ret_key: ret}


def parse_response_401(xml):
    root = et.fromstring(xml)
    return {'text': root.find('body').text}


def parse_response_acknowledgement_market_document(xml, xml_ns):
    root = et.fromstring(xml)
    return {'code': root.find(f"{CONST_XML_NS}:Reason/{CONST_XML_NS}:code", xml_ns).text,
            'text': root.find(f"{CONST_XML_NS}:Reason/{CONST_XML_NS}:text", xml_ns).text}


def parse_response_publication_market_document(xml, xml_ns):
    ret = {}

    root = et.fromstring(xml)
    interval_start = root.find(f"{CONST_XML_NS}:period.timeInterval/{CONST_XML_NS}:start", xml_ns).text
    interval_end = root.find(f"{CONST_XML_NS}:period.timeInterval/{CONST_XML_NS}:end", xml_ns).text
    ret["intervalStart"] = interval_start
    ret["intervalEnd"] = interval_end

    ts = root.findall(f"{CONST_XML_NS}:TimeSeries", xml_ns)
    ret_ts = []
    for t in ts:
        area = t.find(f"{CONST_XML_NS}:in_Domain.mRID", xml_ns).text
        currency = t.find(f"{CONST_XML_NS}:currency_Unit.name", xml_ns).text
        uom = t.find(f"{CONST_XML_NS}:price_Measure_Unit.name", xml_ns).text
        res = t.find(f"{CONST_XML_NS}:Period/{CONST_XML_NS}:resolution", xml_ns).text
        period_start = t.find(f"{CONST_XML_NS}:Period/{CONST_XML_NS}:timeInterval/{CONST_XML_NS}:start", xml_ns).text
        period_end = t.find(f"{CONST_XML_NS}:Period/{CONST_XML_NS}:timeInterval/{CONST_XML_NS}:end", xml_ns).text

        points = t.findall(f"{CONST_XML_NS}:Period/{CONST_XML_NS}:Point", xml_ns)
        ret_ps = []
        for p in points:
            pos = p.find(f"{CONST_XML_NS}:position", xml_ns).text
            price = p.find(f"{CONST_XML_NS}:price.amount", xml_ns).text
            ret_ps.append({"position": pos,
                           "price": price})

        ret_ts.append({"area": area,
                       "currency": currency,
                       "uom": uom,
                       "resolution": res,
                       "periodStart": period_start,
                       "periodEnd": period_end,
                       "points": ret_ps})

    ret["timeSeries"] = ret_ts
    return ret


if __name__ == '__main__':
    print('Only for use as module')
