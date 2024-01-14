# hass-352-skin-humidifier

Home assistant integration for 352 skin humidifier.

## Screenshots

![dashboard](https://raw.githubusercontent.com/jzhangdev/hass-352-skin-humidifier/main/screenshots/dashboard.png)
![entity-details](https://raw.githubusercontent.com/jzhangdev/hass-352-skin-humidifier/main/screenshots/entity-details.png)

## Config

`configuration.yaml`

```yaml
humidifier:
  - platform: 352_skin_humidifier
    name: 352 Skin Humidifier
    device_id:
    token:

template:
  - sensor:
    - name: Temperature
      unit_of_measurement: "°C"
      state: "{{ state_attr('humidifier.352_skin_humidifier', 'current_temperature')}}"
```

