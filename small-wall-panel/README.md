![20240609_103911](https://github.com/jm-cook/my-smart-home/assets/8317651/85ebf7f8-b1d6-4978-b53c-6a520244fe1d)

This wall panel is made from a 7" Huawei Media Pad T3. It has a resolution of 1024x600, its quite small, and a few years old, but it does work as an excellent display in the kitchen area. 
The compact display is designed to be easy to read from a distance, and just shows the essential sensor values that I am most interested in. 
The panel is at our holiday cottage, which is in a remote location with no road. There 
is electricity and fibre broadband, but no mains water, so it can still be smart!

![image](https://github.com/jm-cook/my-smart-home/assets/8317651/a6adee02-b8c0-4492-9123-7e3e78984f90)

The essential components are a date/time card, a thermostat card for the living room, the outdoor temperature, the hot tub temperature, and the state of the borehole, with a few essential bits of information along the bottom.
Most of the cards use [mushroom cards](https://github.com/piitaya/lovelace-mushroom), but with some changes to the default theme so that I can see them clearly when standing a short distance away.


![20240609_103901](https://github.com/jm-cook/my-smart-home/assets/8317651/c68e9b54-6e6f-4fa7-8ac9-0ab5b4ed1e42)

The yaml configuration for the dashboard can be [downloaded from here](https://github.com/jm-cook/my-smart-home/blob/dev/small-wall-panel/panel_config.yaml) but below you will find 
detailed descriptions of each of the cards so that you can make something similar yourself.

# Grid layout
The whole panel is based on the ```custom:grid-layout``` which is part of the [lovelace-layout-card](https://github.com/thomasloven/lovelace-layout-card). 
The display is divided into 3 columns and 3 rows:

```yaml
views:
  - type: custom:grid-layout
    layout:
      grid-template-columns: 1fr 1fr 1fr
      grid-template-rows: auto auto auto
      grid-template-areas: |
        "datetime  datetime  wellarea   "
        " button1   button2   button3   "
        "chip2area chip2area chip2area  "
    title: Weather station
    path: weather-station-new
    theme: mush_panel
    cards: []
```
Each column has an equal width, but as we will see later, the date/time card spans 2 columns and the strip along the bottom scans all 3.
There is not much space on the 7" tablet but enough to display key information and provide access to other sensors through mushroom "chips".

# Custom theme
Mushroom cards allow customization through [themes](https://github.com/piitaya/lovelace-mushroom-themes) that can be applied to the whole dashboard. 
To get a clear display I have made a theme that overrides the default. The main changes are to the font sizes and the colour of the primary text.
The theme used in this panel is carefully crafted so that the text fits on my particular 7" panel. You can access it [here for reference](https://github.com/jm-cook/my-smart-home/blob/dev/small-wall-panel/mush_panel_theme.yaml) but please refer to the theme documentation (link above) for installation.

# The date-time card
The date-time card uses the mushroom template card. This is because we want to show data from two different sensors so the regular entity card cannot be used.

![image](https://github.com/jm-cook/my-smart-home/assets/8317651/8f846e8c-af79-478c-9848-c1509fe5c053)


For the date-time card to work you will need to enable the [```time_date``` integration](https://www.home-assistant.io/integrations/time_date/). You will need the ```display_options``` **time**, and **date**.

The date can be formatted however you prefer, here is the template code that I have for my formatted date:

```yaml
template:
  - sensor:   
      - name: "Current Date"
        icon: mdi:calendar-today
        unique_id: current_date_sensor
        state: >-
          {% set date = states('sensor.date') %}
          {% set datetime = strptime(date, '%Y-%m-%d') %}
          {% set weekday = datetime.strftime('%A') %}
          {% set month = datetime.strftime('%B') %}
          {% set day = datetime.strftime('%d') | int %}
          {%
            set suffix = 'st' if (day % 10 == 1 and day != 11)
            else 'nd' if (day % 10 == 2 and day != 12)
            else 'rd' if (day % 10 == 3 and day != 13)
            else 'th'
          %}
          {{ weekday }} {{ month }} {{ day }}{{ suffix }}
```

Include this code or similar into your ```configuration.yaml```.

The Date card with time display is a mushroom template card displaying both the time and the date. You can create it in the editor for mushroom cards, but here is the full yaml configuration for my card:

```yaml
type: custom:mushroom-template-card
primary: '{{ states(''sensor.current_date'') }}'
secondary: '{{ states(''sensor.time'') }}'
icon: ''
tap_action:
  action: none
hold_action:
  action: none
double_tap_action:
  action: none
entity: sensor.time
fill_container: true
icon_color: ''
layout: vertical
card_mod:
  style:
    mushroom-card $: |
      .container {
         --card-secondary-font-size: 160px;
         --card-secondary-line-height: 175px;
         --card-primary-line-height: 40px;
         --card-primary-font-size: 30px;
         --card-padding: 0px;
         --card-margin: 0px;
      }
view_layout:
  grid-area: datetime
```
