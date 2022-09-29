# Electricity Price integration for Home Assistant (ENTSO-E / Nordpool)
The [ENTSO-E](www.entsoe.eu) electricity price integration retrieves the **day ahead electricity prices** (spot price) from the *European Network of Transmission System Operators for Electricity* into **Home Assistant**. ENTSO-E is the association for the cooperation of the European transmission system operators (TSOs).

The data in ENTSO-E is the **same as from *Nordpool*** but unlike Nordpool, ENTSO-E provides an open API!

This integration gives you the hourly electricity prices for today and tomorrow (day ahead) as they are published by Nordpool via ENTSO-E. It is possible to...
 - Configure sensors that show the current spot price.
 - Add markups to reflect the retail price that that your electricty reseller is charging you i.e. price incl. VAT and reseller's margin.
 - Convert the price to any currency using exchange rates from [European Central Bank (ECB)](https://www.ecb.europa.eu/).

## Getting started
### Obtaining a ENTSO-E API token
To call the ENTSO-E API a token is needed. These are handed out free of charge but you have to register on the ENTSO-E site.

1. Goto the [ENTSO-E Transparency Platform](https://transparency.entsoe.eu).
2. Resgister on the ENTSO-E Transparency Platform. Click `Login` and chose to `Register`.
3. Login at least once! (ENTSO-E will **NOT** give you API access if you have not been logged in at least once.)
4. Request an API key by sending an e-mail to transparency@entsoe.eu with “Restful API access” in the subject line and nothing but you e-mail address in the e-mail body. You will receive an email when you have been provided with the API key. This usually goes quickly but can take up to three days.
5. Login to the transparency platform and goto [`My Account Settings`](https://transparency.entsoe.eu/usrm/user/myAccountSettings).
6. Click `Generate a new token` and copy the result.

### Installing the ENTSO-E integration
Copy the `entso_e` folder into your `config/custom-components` folder in you Home Assistant.

### Configuration
```yaml
entso_e:
    token: xxx-xxx-xxx-xxx
    areas:
      - SE3
      - SE4
```

```yaml
sensor:
  # Spot price for SE3 in EUR per MWh
  - platform: entso_e
    area: SE3

  # Actual price, incl. retail markups, in SEK per kWh
  - platform: entso_e
    area: SE3
    friendly_name: Mitt elpris
    decimals: 2
    convert_uom_to: kWh
    convert_currency:
        to_currency: SEK
        exchange_rate: sensor.ecb_exr_sek_to_eur
    markups:
      - friendly_name: Energy tax
        amount: 0.45
      - friendly_name: Transmission fee
        percent: 25