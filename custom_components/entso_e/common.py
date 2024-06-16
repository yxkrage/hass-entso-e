from datetime import datetime, timedelta
import logging

from .area_codes import area_codes
from .const import (
    CONST_CURRENCY_CODE_TO_SYMBOL,
    CONST_ENERGY_UOM_FIX_CASE,
    DAYS_LOOK_AHEAD,
)

# from .entso_e import call_api, parse_response
# from .entsoe_json import call_api, parse_response
from .entsoe import Entsoe

_LOGGER = logging.getLogger(__name__)


def to_datetime(iso_str) -> datetime:
    if iso_str[-1] == 'Z':
        iso_str = iso_str[0:-1] + '+00:00'
    return datetime.fromisoformat(iso_str)


async def async_get_data_from_api(token, area) -> tuple[bool, dict]:
    c_area = conv_price_area(area)
    if c_area is None:
        return (False, None)

    entsoe = Entsoe(
        api_key=token,
        area=c_area,
        date_from=datetime.now(),
        date_to=datetime.now() + timedelta(days=DAYS_LOOK_AHEAD)
    )

    parsed_resp = await entsoe.async_get_result()

    http_status_code = parsed_resp.get('http_status_code')
    data = parsed_resp.get('data')

    # Logg error and return false
    if data == None:
        message = parsed_resp.get('message')
        code = message.get('code')
        log_err = f"Http response {http_status_code}, {message.get('text')}"
        if code:
            log_err += f" (Code: {code})"
            _LOGGER.error(log_err)
        return (False, data)
    return (True, data)


def flatten_response(resp: dict) -> dict:
    ret = {}  # Create empty return structure
    cur = None  # Currency code. Returned and used to ensure that all TimeSeries have the same currency
    uom = None  # UoM. Returned and used to ensure that all TimeSeries have the same UoM
    tz = datetime.now().astimezone().tzinfo

    # Loop thru all TimeSeries in response
    for ts in resp.get('timeSeries'):
        tmp_cur = ts.get('currency')
        tmp_uom = ts.get('uom')

        # Check that currency is the same in all TimeSeries
        if cur is None:
            cur = tmp_cur
        elif cur != tmp_cur:
            pass  # TODO Raise error

        # Check that currency is the same in all TimeSeries
        if uom is None:
            uom = tmp_uom
        elif uom != tmp_uom:
            pass  # TODO Raise error

        # Loop thru all periods and add to return structure
        dt = to_datetime(ts.get('periodStart'))
        for pt in ts.get('points'):
            hr = int(pt.get('position')) - 1
            pr = pt.get('price')
            d = dt + timedelta(hours = hr)
            ret[d.astimezone(tz).isoformat()] = pr

    return {'currency': cur,
            'uom': uom,
            'data': ret}


def get_price_by_datetime(flat_resp: dict, dt: datetime) -> str:
    d = dt.replace(minute=0, second=0, microsecond=0)
    iso = d.astimezone().isoformat()
    return flat_resp.get(iso)


def conv_currency(currency: str) -> str:
    return CONST_CURRENCY_CODE_TO_SYMBOL.get(currency.upper(), currency)


def fix_uom_case(uom: str) -> str:
    return CONST_ENERGY_UOM_FIX_CASE.get(uom.upper(), uom)


def conv_price_area(area: str) -> str | None:
    """Translate Price Area e.g. 'SE3' to Entso-e name e.g. '10Y1001A1001A46L'"""
    for rec in area_codes:
        ac = rec.get('area', None)
        if ac == area:
            cd = rec.get('code', None)
            _LOGGER.debug(f"Using code '{cd}' for '{ac}' when calling API")
            return cd
    _LOGGER.error(f"Unable to convert area code '{area}' to Entso-e code.")
    return None
