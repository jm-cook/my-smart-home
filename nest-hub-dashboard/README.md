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

The ```yaml``` code shown below is the first part of the configuration. You can see that first the grid-layout is defined for the view, the ```path```, and the ```title```. You will also see that a custom ```theme``` is defined. More on that in the next sectoin. Next, in the ```cards``` specification, a ```custom:layout-card``` is defined. This is our main container for the dashboard.
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

Mushroom cards allow for some degree of customization using a custom theme. To achieve what I wanted I have tweaked a copy of the baseline theme to 
have larger fonts. The larger fonts will not work in all situations, and are designed to be used with my bespoke layout.

You can obtaine a copy of the baseline [mushroom theme at this location](https://github.com/piitaya/lovelace-mushroom-themes). Follow the instructions 
to install this or modify them to fit your own needs. It is important to give the theme a name that is unique so if you create more than one mushroom 
theme, be sure to give them different names.

In my tweaked theme I have changed the following to get the large font look that I was after:

```yaml
    masonry-view-card-margin: 4px 4px 4px 4px

    # Card
    mush-card-primary-font-size: 22px
    mush-card-secondary-font-size: 50px
    mush-card-primary-font-weight: 500
    mush-card-secondary-font-weight: 600
    mush-card-primary-line-height: 25px
    mush-card-secondary-line-height: 52px
    mush-card-primary-color: grey

    mush-card-border-radius: 18px

```

[Custom theme](https://github.com/jm-cook/my-smart-home/blob/main/nest-hub-dashboard/mush_nest_panel_theme.yaml)


## Date card

## Time card

## Nowcast (weather) card

## Sensor cards

## Flexit balanced air circulation card

## Weather chip
