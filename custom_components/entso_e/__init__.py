import logging
import asyncio

import voluptuous as vol

import homeassistant.helpers.config_validation as cv

from .const import CONF_AREAS, CONF_TOKEN, DOMAIN, SETUP_TIMEOUT, CONF_EVENT_SETUP_DONE
from .PriceArea import PriceArea, get_price_area_object

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_TOKEN): cv.string,
                vol.Required(CONF_AREAS): cv.ensure_list(cv.string)
            }
        )
    },
    extra=vol.ALLOW_EXTRA
)


async def async_setup(hass, config):
    def handle_get_data(call):
        """Handle the service call."""
        tmp = call.data.get(CONF_AREAS)
        if isinstance(tmp, str):
            areas = [tmp]
        elif isinstance(tmp, list):
            areas = tmp
        else:
            areas = []

        _LOGGER.debug(f"Service 'get_data' called for area '{areas}'")

        # Get new price data from API
        for area in areas:
            pa = get_price_area_object(hass, area)
            if pa:
                pa.update_from_api()
            else:
                _LOGGER.error(
                    f"Price data cannot be retrieved for price area '{area}' " +\
                    "because it is not setup in 'configuration.yaml'. Add to " +\
                    f"'{CONF_AREAS}:' under '{DOMAIN}:'."
                )

    # Setup integration
    conf = config.get(DOMAIN)
    if conf is None:
        _LOGGER.info(f"No configuration for '{DOMAIN}' found")
        return True
    token = conf.get(CONF_TOKEN)
    areas = conf.get(CONF_AREAS)

    hass.data[DOMAIN] = {
        CONF_TOKEN: token,
        CONF_AREAS: [],
        CONF_EVENT_SETUP_DONE: asyncio.Event()  # Used to signal that all PriceArea objects are setup
    }

    # Register service
    hass.services.async_register(DOMAIN, "get_data", handle_get_data)

    # Create on PriceArea object for each area in
    # config and add it to hass
    for area in areas:
        pa = PriceArea(hass, area)
        if not pa:
            _LOGGER.error(f"Price area '{area}' could not be setup")
        hass.data[DOMAIN][CONF_AREAS].append(pa)
        _LOGGER.info(f"Price area '{area}' setup")

    # All PriceArea objects in hass.data[DOMAIN][CONF_AREAS] contains the property self.event_setup_done
    # which is an asyncio.Event object. This is used to signal that the object is fully setup.
    # Wait for all events to signal that all objects are setup with a timeout of 60 seconds
    try:
        await asyncio.wait(
            [asyncio.create_task(pa.event_setup_done.wait()) for pa in hass.data[DOMAIN][CONF_AREAS]],
            timeout=SETUP_TIMEOUT
        )
    except asyncio.TimeoutError:
        _LOGGER.error("At least one PriceArea objects timed out during setup")
        return False

    # Add asyncio event to hass.data[DOMAIN] to signal that all objects are setup
    hass.data[DOMAIN][CONF_EVENT_SETUP_DONE].set()

    return True