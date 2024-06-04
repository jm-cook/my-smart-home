## Dashboard on Nest Hub

This document describes how I created a smart home dashboard with good visibility around the room, that can be shown on a Google Nest Hub.
The first image is a photo of the hub as it looks in the kitchen, the second is a screenshot of the dashboard from a web browser.


<img src="20240604_075825-1717483432984.jpg" width="400">
<img src="https://github.com/jm-cook/my-smart-home/assets/8317651/d1f6d6e3-eaf4-44e8-84b4-15017d3378d2" width="400">

Previously I have used the custom button-card for lovelace (https://github.com/custom-cards/button-card), but recently I experimented with the custom mushroom cards (https://github.com/piitaya/lovelace-mushroom) and liked the simple approach, requiring very little customization to achieve the look that I was after.

The dashboard uses primarily mushroom cards and the custom grid-layout from lovelace-layout-card (https://github.com/thomasloven/lovelace-layout-card).

# Pre-requisite

To make a dashboard like mine you will need to install:

 - [Mushroom](https://github.com/piitaya/lovelace-mushroom)
 - [Lovelace-layout-card](https://github.com/thomasloven/lovelace-layout-card)
 - [card-mod](https://github.com/thomasloven/lovelace-card-mod)

Follow the instructions for installing each package on your own installation.

# The Layout

For details of my layout and how it is implemented, see the file [nest_hub.yaml](nest_hub.yaml). This is the full export of the code for the entire dashboard. 
You should be able to create a new dashboard in 
your Home Assistant instance and paste some or all of this file into your own configuration:

The rest of this document describes how to achieve the layout and the individual sensor cards.

## Grid view
The dashboard uses the grid layout card. There was a problem displaying a grid layout directly on the nest hub so I first created a dashboard with a grid view, and then inserted a grid-layout card inside that. This then works and displays as you see in the images above.

The ```yaml``` code shown below id the first part of the configuration. You can see that first the grid-layout is defined for the view, the ```path```, and the ```title```. You will also see that a custom ```theme``` is defined. More on that later. Next, in the ```cards``` specification, a ```custom:layout-card``` is defined. This is our main container for the dashboard.
The ```layout```specifies 4 columns each taking a quarter of the width. We use 4 columns for the individual sensor cards, and merge into 2 columns for the date, clock and weather displays.

```yaml
views:
  - type: custom:grid-layout
    path: nest-dashboard
    theme: mush_nest_panel
    title: Nest
    cards:
      - type: custom:layout-card
        layout_type: custom:grid-layout
        layout:
          grid-template-columns: repeat(4, 1fr)
          grid-template-rows: auto auto auto auto
          grid-template-areas: |
            "datearea  datearea   weather  weather" 
            "timearea  timearea   weather  weather"  
            "button1   button2    button3  fan" 
            "button4   button5    button6  chips "
```

## Custom theme

## Date card

## Time card

## Nowcast (weather) card

## Sensor cards

## Flexit balanced air circulation card

## Weather chip
