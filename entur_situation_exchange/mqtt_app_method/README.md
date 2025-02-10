Navigate to: [My smart home](../..)

# Home Assistant EnTur situation exchange query app for appdaemon

This folder contains instructions and code for accessing the EnTur situation exchange data. EnTur is the Norwegian
national travel planner and provides various APIs for travel planning, ticketing, vehicle tracking and 
information on deviations in services.

The code in this folder accesses the situation-exchange and creates Home Assistant sensors monitoring the state of specified lines.

This standalone python app for appdaemon will create sensors for each of the lines that you select. 
To use it you will use the Home Assistant addons appdaemon and mqtt and install the python app
for appdaemon. This method may initially seem 
complicated but installation *should* be straightforward and the solution gives the best results out of all the methods that I tried.

## Why?

Why did I make this when the operator already provides this information in their app and on the web? I made this 
because I live near to the public stop that I use most often and wanted a more immediate information channel. Most of the time all is well, but sometimes
due to weather or some other outside influence, the whole line may stop and chaos ensues. It is great to 
know before I go out of the house that all systems are functioning normally, and if not then take some
avoiding action. I have the relevant sensors, like the ones described here, on my dashboard in the kitchen. They only show if there is
a problem (by using conditional visibility), but better to be able to see what is going on there than to open up the web or an app. 
I have also set up alerting in the HA companion app, something that 
the local operator's app does not do.

## Installation

To install the codes you must follow these steps:

1. install the mosquitto broker add on for home assistant. To do this go to the add-ons configuration section and select the mosquitto broker from the list of official addons.

   [![Open your Home Assistant instance and show the add-on store.](https://my.home-assistant.io/badges/supervisor_store.svg)](https://my.home-assistant.io/redirect/supervisor_store/)

   Install mosquitto and configure it.

1. You will need the MQTT integration from the integrations page:
   
   [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=mqtt)

1. Now install the appdaemon addon which is available form the addon store.

   [![Open your Home Assistant instance and show the add-on store.](https://my.home-assistant.io/badges/supervisor_store.svg)](https://my.home-assistant.io/redirect/supervisor_store/)

-----------------------------
The script "entur_sx.py" is an app for appdaemon that fetches the entur SX data and creates appropriate sensors on your system through Home Assistant  autodiscovery of MQTT.
Copy the script to your appdaemon app folder. It will probably be in something like: ```/addon_configs/a0d7b954_appdaemon/apps```, you will need 
to upload the file yourself, or copy/paste using an editor

Then configure the app in the ```apps.yml``` file located in the same folder as the python script. Similar to the following:

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

Once the ```app.yaml``` and the python app are in place, the app should run automatically, so check the logs for appdaemon.

The app will create the required sensors on your system (through MQTT discovery). You should find them
under the MQTT integration page similar to this:

![image](https://github.com/user-attachments/assets/356eb486-38de-40bd-ab11-5d9eb3e1dea0)

The sensors will have a default icon when they are created, but the app creates a ```unique_id``` for each sensor so you can edit the sensor and and change the icon to a mdi icon of your own choice.

![image](https://github.com/user-attachments/assets/0efaaf32-0b02-4702-9eec-f04c40e073d3)

Note that the app script specifies that MQTT topics should be retained. This is to ensure continuity between restarts
of HA (otherwise the sensors become unavailable). MQTT retention can be tricky, and if something goes wrong, or you want to remove a line/sensor, then 
it will most likely be retained. This may mean that old line sensors are still available after you have 
removed them from the configuration. There is currently no automatic purge to remove previous configurations (but see below).

Once you have your deviation sensors working, you can display them in your dashboard. A simple example:

![image](https://github.com/user-attachments/assets/27f9ddef-6c2a-4432-bdb1-5c0c280de0b7)

In this example, the description is conditionally shown, epending on whether there is an on-going deviation or not.

YAML code for a sections view:
```yaml
views:
  - type: sections
    max_columns: 4
    title: SKYSS
    path: skyss
    sections:
      - type: grid
        cards:
          - type: heading
            heading: Utvalgte SKYSS avvik
            heading_style: title
          - type: tile
            grid_options:
              columns: full
            entity: sensor.skyss_avvik_sky_line_20
            name: Bus 20
            icon: ''
          - type: markdown
            content: '{{ state_attr( ''sensor.skyss_avvik_sky_line_20'', ''description'') }}'
            visibility:
              - condition: state
                entity: sensor.skyss_avvik_sky_line_20
                state_not: Normal service
          - type: tile
            grid_options:
              columns: full
            entity: sensor.skyss_avvik_sky_line_1
            name: Bybanen
            icon: ''
          - type: markdown
            content: '{{ state_attr( ''sensor.skyss_avvik_sky_line_1'', ''description'') }}'
            visibility:
              - condition: state
                entity: sensor.skyss_avvik_sky_line_1
                state_not: Normal service
```

In addition you might like to send a notification to the companion app on your phone. An example 
automation to do this is shown below (you will need to define "COMPANION_APPS" yourself, check the documentation for notifications):

```yaml
alias: Bybanen avvik
description: ""
triggers:
  - trigger: state
    entity_id:
      - sensor.skyss_avvik_sky_line_1
    attribute: description
conditions: []
actions:
  - delay:
      hours: 0
      minutes: 1
      seconds: 0
  - action: notify.COMPANION_APPS
    metadata: {}
    data:
      message: "Bybanen: {{ states('sensor.skyss_avvik_sky_line_1') }}"
      data:
        sticky: "true"
        clickAction: /nest-mush-panel/skyss
mode: single
```
--------------------------------------------------------
If you should use a configuration that created a line sensor that you no longer need, the sensor will continue to exist even if you remove it from the ```lines_to_check``` configuration. This is due to
message retention in the mosquitto broker. The current method to remove unwanted line sensors is to access the mosquitto broker using MQTT Explorer (take a look here https://community.home-assistant.io/t/addon-mqtt-explorer-new-version/603739). If you connect MQTT Explorer to your broker, you can delete the unwanted topics there:

![image](https://github.com/user-attachments/assets/b0f9e176-149b-41f1-9038-f2b5f30b3bec)


