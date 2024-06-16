"""Constants for the Entso-e integration."""

# Configuration constants
DOMAIN = "entso_e"
CONF_TOKEN = "token"
CONF_AREAS = "areas"
CONF_AREA = "area"
CONF_CODE = "code"
CONF_DECIMALS = "decimals"
CONF_CONVERT_TO_UOM = "convert_uom_to"
CONF_CONVERT_CURRENCY = 'convert_currency'
CONF_CONVERT_TO_CURRENCY = 'to_currency'
CONF_CONVERT_EXCHANGE_RATE = 'exchange_rate'
CONF_EVENT_SETUP_DONE = 'event_setup_done'

CONF_MARKUPS = "markups"
CONF_AMOUNT = "amount"
CONF_PERCENT = "percent"

EVENT_PRICE_DATA_UPDATED = f"{DOMAIN}_event"
EVENT_TYPE_DATA_UPDATED = "data_updated"

SETUP_TIMEOUT = 30

# Convert currency code to symbol
CONST_CURRENCY_CODE_TO_SYMBOL = {
    'EUR': '€',
    'USD': '$',
    'SEK': 'kr',
    'NOK': 'kr',
    'DKK': 'kr'
    # Add more
}

# Fix Case of UoMs
CONST_ENERGY_UOM_FIX_CASE = {
    'MWH': 'MWh',
    'KWH': 'kWh',
    'WH': 'Wh'
}

CONST_VALID_ENERGY_UOMS = [uom for uom in CONST_ENERGY_UOM_FIX_CASE]

# Convert between energy UoMs
CONST_ENERGY_UOM_CONV = {
    'MWH': {
        'KWH': 1000,
        'WH': 1000000
    },
    'KWH': {
        'MWH': 0.001,
        'WH': 1000
    },
    'WH': {
        'MWH': 0.000001,
        'KWH': 0.001
    }
}

# Other constants
CONST_HOUR = 'hour'
CONST_MINUTE = 'minute'
CONST_SECOND = 'second'

# Functional Parameters
DAYS_LOOK_AHEAD = 2  # Try to get price data for this many days into the future
POLL_API_TIME_PATTERN = {
    #CONST_HOUR: 21,
    #CONST_MINUTE: 17,
    #CONST_SECOND: [0, 10, 20, 30, 40, 50]
    CONST_HOUR: 14,
    CONST_MINUTE: 30,
    CONST_SECOND: 0
}
