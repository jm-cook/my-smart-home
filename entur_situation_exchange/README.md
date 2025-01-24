# EnTur situation echange query

This folder contains instructions and code for accessing the EnTur situation exchange data. EnTur is the Norwegian
national travel planner and provides various APIs for travel planning, ticketing, vehicle tracking and 
information on deviations in services.

The code in this folder accesses the situation-exchange so that Home Assistant sensors can be created to
monitor the state of individual lines.

For example:

![image](https://github.com/user-attachments/assets/f6cb174e-95fa-4d52-82ea-b9178222ada0)

## Installation

To install the codes you must follwo these steps:

1. Add the ```python_script``` integration to your installation and create the folder ```python_scripts``` as described here: https://www.home-assistant.io/integrations/python_script/#writing-your-first-script-reading-input-and-logging-the-activity
2. Download the files ```entur_sx.py``` and ```services.yaml```from this github folder and upload them to the ```python_scripts``` folder that you created in step 1 above. You can upload files using the File editor sidebar menu.
3. Restart your home assistant core.
4. Test that the script is working. Use the developer menu and select the actions tab. You should be able to see the script and try it out in the actions menu:

   ![image](https://github.com/user-attachments/assets/7764ee9b-5999-4af0-906f-b9f9ed6c1cac)
If you click on "Perform action" you should get a response that looks similar to this one:

    ![image](https://github.com/user-attachments/assets/230a23a2-abb2-4fed-aeae-1d5b35e797ed)
   The service returns a dict containing start (a datetime when the deviation started), summary, and description.
   
5. Create sensors for each of the lines you are interested in. To do this you can create trigger based teplate sensors. For example (in ```configuration.yaml```):


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
      - name: skyss_situation_line_20
        unique_id: skyss_situation_line_20
        state: "{{ lines_report.get('SKY:Line:3')[0].get('summary')  }}"
        attributes:
            valid_from:   "{{ lines_report.get('SKY:Line:3')[0].get('start')  }}"
            summary:      "{{ lines_report.get('SKY:Line:3')[0].get('summary')  }}"
            description:  "{{ lines_report.get('SKY:Line:3')[0].get('description')  }}"
```

In this template, the trigger fires at 15 seconds past every minute and calls the python script as a service. The ```lines_report```
response variable contains a dict that is then used to update 2 sensors and their attributes. The dict will contain 
all reports for the selected lines so in the template we take just the first (and most recent) one.
