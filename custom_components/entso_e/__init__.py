import logging
from optparse import Option

import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .PriceArea import PriceArea, get_price_area_obejct
from .const import DOMAIN, CONF_TOKEN, CONF_AREAS

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


#async def async_setup(hass, config):
def setup(hass, config):
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
            pa = get_price_area_obejct(hass, area)
            if pa:
                pa.update_from_api()
            else:
                _LOGGER.error(f"Price data cannot be retrieved for price area '{area}' " +\
                              f"because it is not setup in 'configuration.yaml'. Add to " +\
                              f"'{CONF_AREAS}:' under '{DOMAIN}:'.")

    # Setup integration
    conf = config[DOMAIN]
    token = conf.get(CONF_TOKEN)
    areas = conf.get(CONF_AREAS)

    hass.data[DOMAIN] = {CONF_TOKEN: token,
                         CONF_AREAS: []}
    #_LOGGER.debug('Config read')

    # Register service 
    hass.services.register(DOMAIN, "get_data", handle_get_data)

    # Create on PriceArea object for each area in 
    # config and add it to hass
    for area in areas:
        pa = PriceArea(hass, area)
        hass.data[DOMAIN][CONF_AREAS].append(pa)
        _LOGGER.info(f"Price area '{area}' setup")

    if token:
        return True
    else:
        return False
