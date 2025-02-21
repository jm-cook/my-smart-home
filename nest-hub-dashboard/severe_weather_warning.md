```yaml
sensor:
  - platform: met_alerts
    name: MET Alerts Oslo
    latitude: 59.951071
    longitude: 10.673786
```

```jinja2
{%- macro met_alerts_view(snsr) -%}
{%- set weekdays = ['Søndag', 'Mandag', 'Tirsdag', 'Onsdag', 'Torsdag', 'Fredag', 'Lørdag'] %} 
{%- set start_time = state_attr(snsr, 'starttime') %}
{%- set end_time = state_attr(snsr, 'endtime') %} 
{%- if start_time and end_time %}
{%-   set start_timestamp = as_timestamp(strptime(start_time, "%Y-%m-%dT%H:%M:%S%z")) %}
{%-   set end_timestamp = as_timestamp(strptime(end_time, "%Y-%m-%dT%H:%M:%S%z")) %}
{%-   set start_day_index = start_timestamp | timestamp_custom("%w") | int %}
{%-   set end_day_index = end_timestamp | timestamp_custom("%w") | int %}
{%-   set start_day = weekdays[start_day_index] %}
{%-   set end_day = weekdays[end_day_index] | lower %}
{%-   if start_day_index == end_day_index %}
{%-     set met_alerts_time = start_day + ' kl ' + (start_timestamp | timestamp_custom("%H:%M")) + ' til ' + (end_timestamp | timestamp_custom("%H:%M")) %}
{%-   else %}
{%-     set met_alerts_time = start_day + ' kl ' + (start_timestamp | timestamp_custom("%H:%M")) + ' til ' + end_day + ' kl ' + (end_timestamp | timestamp_custom("%H:%M")) %}
{%-   endif %}

{%-   set time_diff = (as_timestamp(start_time) - as_timestamp(now())) / 3600 %}
{%-   if time_diff < 24 %}
        <center><font color="{{ state_attr(snsr, 'awareness_level_color') }}"><ha-icon icon="mdi:alert"></ha-icon> Farevarsel - {{ state_attr(snsr, 'event_awareness_name') }} <ha-icon icon="mdi:alert"></ha-icon></font></center>
        <center>{{ met_alerts_time }}</br></br>
        {{ state_attr(snsr, 'description') }}</center>
        </br>
        <i>{{ state_attr(snsr, 'instruction') }}</i>
        
![image]({{ state_attr(snsr, 'map_url') }})
{% endif %}
{% else %}
{{none}}
{%- endif %}
{%- endmacro -%}
```

```jinja2
{% from 'met_alerts_view.jinja' import met_alerts_view %}
{{ met_alerts_view('sensor.met_alerts_oslo') }}
```

![image](oslo_alert_example.png)
