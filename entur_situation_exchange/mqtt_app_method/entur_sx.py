import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime
from string import Template
import requests
import json

#
# EnTur situation exchange app
#
# Author: Jeremy Cook
#
# Args:
#
configTemplate = ("{ "
                  "\"name\": \"$name\", "
                  " $device_class "
                  # "\"state_class\": \"measurement\", "
                  "\"state_topic\": \"$state_topic\", "
                  "\"unique_id\": \"$unique_id\", "
                  # "\"object_id\": \"$object_id\", "
                  # "\"value_template\": \"{{ value_json.$entity_id }}\", "
                  "\"device\":{"
                  "\"identifiers\": [ \"$id\" ], "
                  "\"name\": \"$device_name\","
                  "\"manufacturer\": \"$manufacturer\" "
                  "},  "
                  "\"json_attributes_topic\": \"$state_topic/attr$name\", "
                  "\"json_attributes_template\": \"{{ value_json.attr | tojson }}\" "
                  "} ")


def sortByTimestamp(item):
    return item["valid_from"]


class EnturSX(hass.Hass):
    service_url = "https://api.entur.io/realtime/v1/rest/sx"

    def initialize(self):
        self.run_every(self.poll_entur, datetime.now(), 60)
        self.run_in(self.poll_entur, 10)
        self.include_future = self.args.get('include_future', True)
        self.lines_to_check = self.args.get('lines_to_check', [])
        self.module = self.args.get('module')
        self.device_id = self.args.get('device', 'EnTur deviations')
        operator = self.args.get('operator', None)
        if operator:
            self.service_url = f"{EnturSX.service_url}?datasetId={operator}"
        else:
            self.service_url = f"{EnturSX.service_url}"

        for line in self.lines_to_check:
            line_name = line.replace(':', '_')
            self.create_sensor(line, line_name)
        self.log(f"args: {self.args}", level="DEBUG")
        self.log(
            f"\n{self.args.get('class')} initialized:\n  "
            f"device: {self.device_id}\n  "
            f"service_url: {self.service_url}\n  "
            f"lines: {self.lines_to_check}\n  "
            f"include_future: {self.include_future}")

    def create_sensor(self, id, name):
        template = Template(configTemplate)
        config_topic = f"homeassistant/sensor/{name}/config"

        cfg_str = template.substitute(
            name=name,
            device_class="",
            state_topic=f"homeassistant/sensor/{name}/state",
            unique_id=id,
            id=self.device_id,
            device_name=self.device_id,
            manufacturer="EnTur AS"
        )
        self.log(f"publishing to {config_topic} : {cfg_str}", level="DEBUG")
        self.call_service("mqtt/publish", topic=config_topic, payload=cfg_str, retain=True, qos=2)

    def update_sensor(self, name, value, attr):
        payload = value
        attr_str = '{{ \"attr\": {attr} }}'.format(attr=json.dumps(attr))
        state_topic = f"homeassistant/sensor/{name}/state"
        attr_topic = f"homeassistant/sensor/{name}/state/attr{name}"
        self.log(f"publishing to {state_topic} : {payload}", level="DEBUG")
        self.call_service("mqtt/publish", topic=state_topic, payload=payload, retain=True, qos=2)
        self.call_service("mqtt/publish", topic=attr_topic, payload=attr_str, retain=True, qos=2)

    def poll_entur(self, kwargs=None):
        self.log(f"EnturSX {datetime.now()}", level="DEBUG")
        headers = {'Content-Type': 'application/json'}
        response = requests.get(self.service_url, headers=headers)
        value_dict = response.json()

        normal = "Normal service"

        allitems_dict = {}
        for look_for in self.lines_to_check:
            items = []
            for sed in value_dict['Siri']['ServiceDelivery']['SituationExchangeDelivery']:
                situations = sed.get('Situations')
                for element in situations.get('PtSituationElement', []):
                    progress = element['Progress']
                    # Only look at open situations
                    if progress == 'OPEN':
                        affects = element.get('Affects')
                        networks = affects.get('Networks', None)
                        start = element.get('ValidityPeriod')[0].get('StartTime')
                        if networks:
                            # If there are future situations we can exclude them by setting include_future = False
                            if (datetime.now().timestamp() > datetime.fromisoformat(
                                    start).timestamp()) or self.include_future:
                                affected_networks = networks.get('AffectedNetwork')
                                for an in affected_networks:
                                    affected_line = an.get('AffectedLine')
                                    line_ref = affected_line[0].get('LineRef').get('value')
                                    if look_for == line_ref:
                                        summary = element.get('Summary')[0]['value']
                                        description = element.get('Description')[0]['value']
                                        items.append(
                                            {"valid_from": start, "summary": summary, "description": description})
                # Ensure most recent situation found  is first
                if len(items) >= 1:
                    items.sort(reverse=True, key=sortByTimestamp)
                else:
                    # No situation for our requested line so set default value
                    items.append({"valid_from": datetime.now().isoformat(), "summary": normal, "description": normal})
                # This makes sure all reports for our requested line are returned in the output dict
                allitems_dict.update({look_for: items})

        self.log(f"Entur deviations: {allitems_dict}", ascii_encode=False, level="DEBUG")
        for line in allitems_dict:
            line_name = line.replace(':', '_')
            line_dict = allitems_dict[line]
            attributes = line_dict[0]
            self.update_sensor(line_name, attributes['summary'], attributes)
