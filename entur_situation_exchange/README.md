# EnTur situation echange query

This folder contains instructions and code for accessing the EnTur situation exchange data. EnTur is the Norwegian
national travel planner and provides various APIs for travel planning, ticketing, vehicle tracking and 
information on deviations in services.

The code in this folder accesses the situation-exchange so that Home Assistant sensors can be created to
monitor the state of individual lines.

For example:

![image](https://github.com/user-attachments/assets/c22c59bb-4486-41d9-8046-1c416ad800c4)

## Why?

Why did I make this when the operator already provides this informatin in their app and on the web? I made this 
because I live near to the public stop that I use most often and wanted a more immediate information channel. Most of the time all is well, but sometimes
due to weather or some other outside influence, the whole line may stop and chaos ensues. It is great to 
know before I go out of the house that all systems are functioning normally, and if not then take some
avoiding action. I have the relevant sensors, like the ones described here, on my dashboard in the kitchen. They only show if there is
a problem (by using conditional visibility), but better to be able to see what is going on there than to open up the web or an app. 
I have also set up alerting in the HA companion app, something that 
the local operator's app does not do.

## Installation

To install the codes you must follow these steps:

1. Add the ```python_script``` integration to your installation and create the folder ```python_scripts``` as described here: https://www.home-assistant.io/integrations/python_script/#writing-your-first-script-reading-input-and-logging-the-activity
2. Download the files ```entur_sx.py``` and ```services.yaml```from this github folder and upload them to the ```python_scripts``` folder that you created in step 1 above. You can upload files using the File editor sidebar menu.
3. add the following resr comand defnition to configuration.yaml:
```yaml
rest_command:
    skyss_sx: 
        url: https://api.entur.io/realtime/v1/rest/sx?datasetId=SKY
        method: GET
        headers:
            User-Agent: Home Assistant
        content_type: application/json
```
5. Restart your home assistant core.
6. Test that the script is working. Use the developer menu and select the actions tab. You should be able to see the script and try it out in the actions menu:

   ![image](https://github.com/user-attachments/assets/f065b2be-14b4-442c-9e9c-5581aa207588)

 If you click on "Perform action" you should get a response that looks similar to this one:

  ![image](https://github.com/user-attachments/assets/6ddd58fa-f449-4d5e-a737-aab660fd5032)


   The service returns a dict containing start (a datetime when the deviation started), summary, and description.
   
5. Create sensors for each of the lines you are interested in. To do this you can create trigger based template sensors. For example (in ```configuration.yaml```):


```yaml
template:
  - trigger:
      - platform: time_pattern
        minutes: /1
        seconds: "15"
    action: 
      - service: python_script.entur_sx
        data:
            include_future: false
            lines_to_check:  
              - SKY:Line:1
              - SKY:Line:3
            operator: SKY
        response_variable: lines_report
    sensor:
      - name: skyss_situation_line_1
        unique_id: skyss_situation_line_1
        state: "{{ lines_report.get('SKY:Line:1')[0].get('summary')  }}"
        attributes:
            valid_from:   "{{ lines_report.get('SKY:Line:1')[0].get('start')  }}"
            summary:      "{{ lines_report.get('SKY:Line:1')[0].get('summary')  }}"
            description:  "{{ lines_report.get('SKY:Line:1')[0].get('description')  }}"
      - name: skyss_situation_line_3
        unique_id: skyss_situation_line_3
        state: "{{ lines_report.get('SKY:Line:3')[0].get('summary')  }}"
        attributes:
            valid_from:   "{{ lines_report.get('SKY:Line:3')[0].get('start')  }}"
            summary:      "{{ lines_report.get('SKY:Line:3')[0].get('summary')  }}"
            description:  "{{ lines_report.get('SKY:Line:3')[0].get('description')  }}"
      - name: skyss_situation_line_20
        unique_id: skyss_situation_line_20
        state: "{{ lines_report.get('SKY:Line:20')[0].get('summary')  }}"
        attributes:
            valid_from:   "{{ lines_report.get('SKY:Line:20')[0].get('start')  }}"
            summary:      "{{ lines_report.get('SKY:Line:20')[0].get('summary')  }}"
            description:  "{{ lines_report.get('SKY:Line:20')[0].get('description')  }}"
```

In this template, the trigger fires at 15 seconds past every minute and calls the python script as a service. The ```lines_report```
response variable contains a dict that is then used to update 2 sensors and their attributes. The dict will contain 
all reports for the selected lines so in the template we take just the first (and most recent) one.

The sensors can be viewed in the developer panel:

![image](https://github.com/user-attachments/assets/6d3b8448-e552-4197-86b9-10be97fae1d0)

