"""Platform for sensor integration."""
from __future__ import annotations

from datetime import datetime
from tokenize import Number
from typing import Any, Optional
from typing_extensions import Required

import logging
import re
from unicodedata import decimal
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from homeassistant.core import HomeAssistant, StateMachine, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.event import async_track_time_change
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
    PLATFORM_SCHEMA
)

from .PriceArea import PriceArea, get_price_area_obejct
from .common import get_price_by_datetime, conv_currency, fix_uom_case 

from homeassistant.const import (CONF_FRIENDLY_NAME, CONF_TYPE, EVENT_STATE_CHANGED,
                                 ATTR_ENTITY_ID)
from .const import (DOMAIN, CONF_AREA, CONF_MARKUPS, CONF_CONVERT_CURRENCY,
                   CONF_CONVERT_TO_CURRENCY, CONF_CONVERT_EXCHANGE_RATE,
                   CONF_AMOUNT, CONF_PERCENT, EVENT_PRICE_DATA_UPDATED, 
                   EVENT_TYPE_DATA_UPDATED, CONST_VALID_ENERGY_UOMS,
                   CONF_DECIMALS, CONF_CONVERT_TO_UOM, CONST_ENERGY_UOM_CONV)


_LOGGER = logging.getLogger(__name__)


def validate_exchange_rate(value: Any) -> str | float:
    """ Validate that configuration parameter 'exchange_rate'
    is a valid entity id or a number"""

    if value is None:
        raise vol.Invalid("value cannot be None or empty")

    if isinstance(value, str):
        if cv.valid_entity_id(value):
            return str(value)
        else:
            raise vol.Invalid("value is not a valid entity id")
    elif isinstance(value, (float, int)):
        return float(value)
    else:
        raise vol.Invalid("value must be a string or a number")

def validate_energy_uom(value: Any) -> str:
    """ Validate that Energy UoM is of known/allowed type"""
    if isinstance(value, str) and value.upper() in CONST_VALID_ENERGY_UOMS:
        return value.upper()
    raise vol.Invalid(f"UoM must be one of {CONST_VALID_ENERGY_UOMS}")

MARKUP_MSG = f"Both '{CONF_AMOUNT}' and '{CONF_PERCENT}' cannot be present in the same markup item."

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_AREA): cv.string,
        vol.Optional(CONF_FRIENDLY_NAME): cv.string,
        vol.Optional(CONF_DECIMALS): vol.Coerce(int),
        vol.Optional(CONF_CONVERT_TO_UOM): validate_energy_uom,
        vol.Optional(CONF_CONVERT_CURRENCY): vol.Schema(
            {
                vol.Required(CONF_CONVERT_TO_CURRENCY): cv.string,
                vol.Required(CONF_CONVERT_EXCHANGE_RATE): validate_exchange_rate
            }
        ),
        vol.Optional(CONF_MARKUPS): cv.ensure_list(
            vol.Schema(
                {
                    vol.Optional(CONF_FRIENDLY_NAME): cv.string,
                    vol.Exclusive(CONF_AMOUNT, CONF_MARKUPS, msg=MARKUP_MSG): vol.Coerce(float),
                    vol.Exclusive(CONF_PERCENT, CONF_MARKUPS, msg=MARKUP_MSG): vol.Coerce(float)
                }
            )
        )
    }
)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
    ) -> None:
    """Setup the sensor platform."""

    area = config.get(CONF_AREA)
    pa = get_price_area_obejct(hass, area)
    sensor = EntsoeSensor(pa, config)
    add_entities([sensor], True)
    _LOGGER.info(f"Sensor '{sensor.name}' ({area}) created")


class EntsoeSensor(SensorEntity):
    """Entso-e Sensor. Showing electricity price for each hour"""
    
    CONV_MODE_NONE = 'N'
    CONV_MODE_FIXED = 'F'
    CONV_MODE_ENTITY = 'E'

    _attr_should_poll = False
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.MEASUREMENT

    _friendly_name = None
    _price_area_obj = None
    _conv_mode = CONV_MODE_NONE
    _conv_to_uom = None
    _conv_to_currency = None
    _conv_exchange_rate_fixed = None
    _conv_entity_id = None
    _markups = None

    def __init__(self,
                 price_area_obj: PriceArea,
                 config: dict):
        super().__init__()

        self._price_area_obj = price_area_obj
        self._friendly_name = config.get(CONF_FRIENDLY_NAME, None)
        self.decimals = config.get(CONF_DECIMALS, None)
        self._conv_to_uom = config.get(CONF_CONVERT_TO_UOM, None)
        self._markups = config.get(CONF_MARKUPS, None)

        # Set exchange rate and mode
        conv = config.get(CONF_CONVERT_CURRENCY, None)
        if conv is not None:
            self._conv_to_currency = conv.get(CONF_CONVERT_TO_CURRENCY, None)
            tmp_exr = conv.get(CONF_CONVERT_EXCHANGE_RATE)
            self._conv_mode = self.CONV_MODE_ENTITY if isinstance(tmp_exr, str) else self.CONV_MODE_FIXED
            if self._conv_mode == self.CONV_MODE_FIXED:
                self._conv_exchange_rate_fixed = float(tmp_exr)
            else:
                self._conv_entity_id = tmp_exr

        _LOGGER.debug(f"Sensor '{self.name}' ({self.area}) created")

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        _LOGGER.debug(f"Sensor '{self.name}' ({self.area}) added to Hass")

        # Call 'update_callback' function every hour, on the hour
        async_track_time_change(self._hass, 
                                self.update_callback,
                                minute=0,
                                second=0)

        # Subscribe to event for updated price data
        self._hass.bus.async_listen(EVENT_PRICE_DATA_UPDATED, self.handle_event_data_updated)

        # Subscribe to exchange rate entity updates
        if self._conv_mode == self.CONV_MODE_ENTITY:
            self._hass.bus.async_listen(EVENT_STATE_CHANGED, self.handle_event_exchange_rate_updated)

    @property
    def _conv_entity_obj(self):
        sm: StateMachine = self._hass.states
        en = sm.get(self._conv_entity_id)
        return en if en else None
    
    @property
    def conv_exchange_rate(self) -> float | None:
        if self._conv_mode == self.CONV_MODE_NONE:
            return None
        elif self._conv_mode == self.CONV_MODE_FIXED:
            return self._conv_exchange_rate_fixed
        else:
            if self._conv_entity_obj is None:
                return None
            try:
                return float(self._conv_entity_obj.state)
            except ValueError:
                _LOGGER.error(f"Unable to retrieve Currency Exchange Rate: " +
                              f"Entity '{self._conv_entity_id}' is not numeric.")
                return None
    @property
    def currency(self) -> str | None:
        if self._conv_mode == self.CONV_MODE_NONE:
            return self._price_area_obj.currency
        else:
            return self._conv_to_currency

    @property
    def energy_uom(self) -> str:
        if self._conv_to_uom:
            return self._conv_to_uom
        else:
            return self._price_area_obj.uom

    @property
    def _hass(self):
        return self._price_area_obj._hass

    @property
    def _attr_name(self) -> str:
        if self._friendly_name:
            return self._friendly_name
        else:
            return f'Electricity Price {self.area}'

    @property
    def area(self) -> str:
        return self._price_area_obj.area

    @property
    def unique_id(self) -> str:
        # Concatinate a string with all config for the sensor
        r = '' 
        r += self.area
        r += self.currency
        r += self.energy_uom
        r += 'dn' if self.decimals is None else 'd' + str(self.decimals)

        if self._conv_mode == self.CONV_MODE_NONE:
            r += 'cn'
        elif self._conv_mode == self.CONV_MODE_FIXED:
            r += 'c' + str(self._conv_exchange_rate_fixed)
        elif self._conv_mode == self.CONV_MODE_ENTITY:
            r += 'c' + self._conv_entity_id.split('.')[1]
        else:
            r += 'cx'  # Should never happen  

        r += self._markup_hash

        # Remove special chars
        r = re.sub('[^A-Za-z0-9]+', '', r)
        return f"{DOMAIN}_{r.lower()}"

    @property
    def _attr_native_unit_of_measurement(self):
        return f'{conv_currency(self.currency)}/{fix_uom_case(self.energy_uom)}'

    @property
    def _markup_hash(self) -> str:
        if not self._markups:
            return ''

        n = 0
        for m in self._markups:
            if CONF_AMOUNT in m:
                n += m.get(CONF_AMOUNT)
            elif CONF_PERCENT in m:
                n += m.get(CONF_PERCENT)
        return str(n)

    def _update_sensor(self, now: datetime = None):
        def convert_currency(p):
            if self._conv_mode == self.CONV_MODE_NONE:
                return float(p)
            else:
                return None if self.conv_exchange_rate is None else float(p) * self.conv_exchange_rate

        def round_value(v) -> float | int:
            """ Round to specified number of decimals """
            r = v
            if isinstance(v, (float, int)) and self.decimals is not None:
                r = round(r, self.decimals)
                if self.decimals == 0:
                    r = int(r)
            return r

        def convert_energy_uom(v) -> float | None:
            if not isinstance(v, (float, int)):
                return None
            if self.energy_uom != self._price_area_obj.uom:
                f = CONST_ENERGY_UOM_CONV.get(self._price_area_obj.uom.upper()).get(self.energy_uom.upper())
                return v / f
            else:
                return v

        def add_markups(v) -> float | None:
            if not isinstance(v, (float, int)):
                return None
            elif self._markups is None:
                return v
            r = v
            for m in self._markups:
                if CONF_AMOUNT in m:
                    r += m.get(CONF_AMOUNT)
                elif CONF_PERCENT in m:
                    r += r * m.get(CONF_PERCENT) / 100
            return r

        if now is None:
            now = datetime.now()

        # Update hourly prices
        tmp = {}
        if self._price_area_obj.data:
            for k in self._price_area_obj.data.keys():
                p = self._price_area_obj.data.get(k)
                p = convert_currency(p)
                p = convert_energy_uom(p)
                p = add_markups(p)
                tmp[k] = round_value(p)
        self._attr_extra_state_attributes = tmp

        # Get current price
        if self._price_area_obj.data:
            self._attr_native_value = get_price_by_datetime(self._attr_extra_state_attributes, now)
            if self._price_area_obj.data:
                _LOGGER.debug(f"Sensor '{self.name}' ({self.area}) updated")
            else:
                _LOGGER.error(f"No price found for sensor '{self.name}' ({self.area}) for '{datetm:%Y-%m-%d %H:%M}'")
        else:
            # Data not available
            self._attr_native_value = None
            _LOGGER.warning(f"No data found for sensor '{self.name}' ({self.area}) when trying to update")

    async def async_update(self) -> None:
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant."""
        self._update_sensor()

    @callback
    async def update_callback(self, now: datetime) -> None:
        self._update_sensor(now)
        self.async_schedule_update_ha_state()

    def handle_event_data_updated(self, event):
        # Check that event is for this sensor
        if event.data.get(CONF_TYPE) == EVENT_TYPE_DATA_UPDATED and \
           event.data.get(CONF_AREA) == self.area:
                _LOGGER.debug(f"Event captured: '{EVENT_PRICE_DATA_UPDATED}' is of type '{EVENT_TYPE_DATA_UPDATED}' and for area '{self.area}'")
                self._update_sensor()
                self.async_schedule_update_ha_state()
        else:
            _LOGGER.debug(f"Event ignored: '{EVENT_PRICE_DATA_UPDATED}' is of type '{EVENT_TYPE_DATA_UPDATED}' and for area '{self.area}'")

    def handle_event_exchange_rate_updated(self, event):
        if event.event_type == EVENT_STATE_CHANGED and \
           event.data.get(ATTR_ENTITY_ID) == self._conv_entity_id:
                _LOGGER.debug(f"Event captured: Exchange rate entity {self._conv_entity_id} updated.")
                self._update_sensor()
                self.async_schedule_update_ha_state()
