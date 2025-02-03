This app for appdaemon will create sensors for each of the lines that you select. 
To use it you will use the addons appdaemon and mqtt. This method may seem a little
complicated but gives the best results.

1. install the mosquitto broker add on for home assistant. TO do this go to the add-ons configuration section and select the mosquitto broker from the list of official addons.
   
[![Open your Home Assistant instance and show the add-on store.](https://my.home-assistant.io/badges/supervisor_store.svg)](https://my.home-assistant.io/redirect/supervisor_store/)
Install mosquitto and configure it.

2. You will need the MQTT integration from the integrations page:
   
[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=mqtt)

3. Now install the appdaemon addon which is available form the addon store

-----------------------------
The script "entur_sx.py" is an app for appdaemon that fetches the entur SX data and creates appropriate sensors on your system through autodiscovery of MQTT
Copy the script to your appdaemon app folder. It will probably be in something like: ```/addon_configs/a0d7b954_appdaemon/apps```, you will need 
to upload the file yourself, or copy/paste using an editor

Then configure the app in the apps.yml file. Similar to the following:

```yaml
---
entursx:
  module: entur_sx
  class: EnturSX
  log_level: INFO
  device: Skyss Avvik
  operator: SKY
  include_future: false
  lines_to_check:
    - SKY:Line:1
    - SKY:Line:2
    - SKY:Line:20
    - SKY:Line:990
```

The things that you can change are: operator, lines_to_check, device, and include_future

You might also change the log_level to DEBUG if needed.
The thins
