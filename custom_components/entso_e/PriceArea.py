from datetime import datetime
import logging
import asyncio

from homeassistant.const import CONF_TYPE
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.event import async_track_time_change

from .common import flatten_response, async_get_data_from_api
from .const import (
    CONF_AREA,
    CONF_AREAS,
    CONF_TOKEN,
    CONST_HOUR,
    CONST_MINUTE,
    CONST_SECOND,
    DOMAIN,
    EVENT_PRICE_DATA_UPDATED,
    EVENT_TYPE_DATA_UPDATED,
    POLL_API_TIME_PATTERN,
)

_LOGGER = logging.getLogger(__name__)


def get_price_area_object(hass: HomeAssistant, area):
    conf = hass.data.get(DOMAIN)
    if not conf:
        return None

    for pa in conf.get(CONF_AREAS):
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

        # self._hass.async_add_executor_job(self.async_update_from_api)
        self._hass.async_create_task(self.async_update_from_api())

        async_track_time_change(
            hass,
            self.async_update_from_api_callback,
            hour=POLL_API_TIME_PATTERN.get(CONST_HOUR, None),
            minute=POLL_API_TIME_PATTERN.get(CONST_MINUTE, None),
            second=POLL_API_TIME_PATTERN.get(CONST_SECOND, None)
        )
        _LOGGER.debug(f"PriceArea object created for area '{self.area}'")
        self.event_setup_done = asyncio.Event()

    @property
    def token(self):
        return self._hass.data[DOMAIN].get(CONF_TOKEN)

    async def async_update_from_api(self):
        self.ok, data = await async_get_data_from_api(self.token, self.area)
        if self.ok:
            # Get data from API response structure
            flat_resp = flatten_response(data)

            # TODO: Check if new data was retrieved (list(data)[-1])
            # TODO: Implement retry if no new data was retrieved

            self.currency = flat_resp.get('currency')
            self.uom = flat_resp.get('uom')
            self.data = flat_resp.get('data')

            # Update Hass
            self._hass.states.async_set(f"{DOMAIN}.{self.area}", "ok", flat_resp.get('data'))

            _LOGGER.info(f"Price data retrieved from API for area '{self.area}'")

            # Fire Event to signal that data is updated
            event_data = {
                CONF_TYPE: EVENT_TYPE_DATA_UPDATED,
                CONF_AREA: self.area
            }
            self.event_setup_done.set()
            self._hass.bus.async_fire(EVENT_PRICE_DATA_UPDATED, event_data)

        else:
            self._hass.states.async_set(f"{DOMAIN}.{self.area}", "error")
            _LOGGER.error(f"Failed to retrieve price data from API for area '{self.area}' ({data})")
            # TODO: Implement Rasie error
            # TODO: Implement retry if no new data was retrieved

    @callback
    async def async_update_from_api_callback(self, now: datetime) -> None:
        # self._hass.async_add_executor_job(self.update_from_api)
        await self.async_update_from_api()

