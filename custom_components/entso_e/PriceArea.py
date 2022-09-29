import logging
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import track_time_change

from datetime import datetime

from .common import flatten_response, get_data_from_api
from homeassistant.const import CONF_TYPE
from .const import (CONF_AREA, CONF_AREAS, DOMAIN, CONF_TOKEN, POLL_API_TIME_PATTERN, 
                    CONST_HOUR, CONST_MINUTE, CONST_SECOND, EVENT_PRICE_DATA_UPDATED,
                    EVENT_TYPE_DATA_UPDATED)

_LOGGER = logging.getLogger(__name__)


def get_price_area_obejct(hass: HomeAssistant, area):
    for pa in hass.data[DOMAIN][CONF_AREAS]:
        if pa.area == area:
            return pa
    return None


class PriceArea:
    ok = None  # Set to None until data has been tried to be retrieved
    data = None
    currency = None
    uom = None

    def __init__(self, hass, area) -> None:
        self._hass = hass
        self.area = area

        self._hass.async_add_executor_job(self.update_from_api)

        track_time_change(hass, 
                          self.update_from_api_callback, 
                          hour=POLL_API_TIME_PATTERN.get(CONST_HOUR, None), 
                          minute=POLL_API_TIME_PATTERN.get(CONST_MINUTE, None), 
                          second=POLL_API_TIME_PATTERN.get(CONST_SECOND, None))
        _LOGGER.debug(f"PriceArea object created for area '{self.area}'")


    @property
    def token(self):
        return self._hass.data[DOMAIN].get(CONF_TOKEN)

    def update_from_api(self):
        self.ok, data = get_data_from_api(self.token, self.area)
        if self.ok:
            # Get data from API response structure
            flat_resp = flatten_response(data)

            # TODO: Check if new data was retrieved (list(data)[-1])
            # TODO: Implement retry if no new data was retrieved

            self.currency = flat_resp.get('currency')
            self.uom = flat_resp.get('uom')
            self.data = flat_resp.get('data')

            # Update Hass
            self._hass.states.set(f"{DOMAIN}.{self.area}", "ok", flat_resp.get('data'))
            _LOGGER.info(f"Price data retrieved from API for area '{self.area}'")

            # Fire Event to signal that data is updated
            event_data = {
                CONF_TYPE: EVENT_TYPE_DATA_UPDATED,
                CONF_AREA: self.area
            }
            self._hass.bus.async_fire(EVENT_PRICE_DATA_UPDATED, event_data)

        else:
            self._hass.states.set(f"{DOMAIN}.{self.area}", "error")
            _LOGGER.error(f"Failed to retrieve price data from API for area '{self.area}' ({data})")
            # TODO: Implement Rasie error 
            # TODO: Implement retry if no new data was retrieved

    @callback
    def update_from_api_callback(self, now: datetime) -> None:
        self._hass.async_add_executor_job(self.update_from_api)
