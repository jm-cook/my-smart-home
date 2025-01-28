# Home Assistant python script to retrieve data from EnTur,
# Process and filter the data,
# and return a dict of filtered situation reports
#
# When called, the user can specify which lines are to be filtered.
# To reduce the amount of data retrieved, the user can also specify the operator
# so that only data for that operator will be retrieved.
#
# 
"""

    :param include_future: If set to true the query will return all situations, including those planned in the future. The parameter is optional with the default value set to true
    :param lines_to_check: This is a list of lines to query for deviations. All requested lines will be included in the returned structure (python dict).
                     Line numbers are usually of the form OPR:Line:nnn where OPR is the operator codespace and nnn is the local line number.
    """
# Utility to sort list of dictionaries by date
def sortByTimestamp(item):
  return item["start"]

include_future = data.get("include_future", True)
lines_to_check = data.get("lines_to_check", [])

trying = True
retry_count = 0
while trying:
    try:
        response = hass.services.call("rest_command", "skyss_sx", {}, blocking=True, return_response=True)
        status = response.get('status')
        value_dict = response.get('content')
    except Exception as e:
        status = 999
        logger.warn(f"error from rest_command \n{e}")
        value_dict = "error"
        
    if isinstance(value_dict, str):
        logger.warning("content is a string not a dict, retrying")
        logger.warning(f"content: {value_dict[:200]} ")
        retry_count = retry_count + 1
        if retry_count > 3:
            trying = false
        else:
            time.sleep(15)
    elif status != 200:
        logger.warning(f"content not retrieved, retrying")
        retry_count = retry_count + 1
        if retry_count > 3:
            trying = false
        else:
            time.sleep(15)
    else:
        if retry_count > 0:
            logger.warning("success")
        trying = False
        
# Default value
normal = "Normal service"

allitems_dict = {}
for look_for in lines_to_check:
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
          if (dt_util.as_timestamp(dt_util.now()) > dt_util.as_timestamp(datetime.datetime.fromisoformat(start))) or include_future:
            affected_networks = networks.get('AffectedNetwork')
            for an in affected_networks:
              affected_line = an.get('AffectedLine')
              line_ref = affected_line[0].get('LineRef').get('value')
              if look_for == line_ref:
                summary = element.get('Summary')[0]['value']
                description = element.get('Description')[0]['value'] 
                items.append( {"start": start, "summary": summary, "description": description } )
    # Ensure most recent situation found  is first
    if len(items) >= 1:
      items.sort(reverse=True, key=sortByTimestamp)
    else:
      # No situation for our requested line so set default value
      items.append( {"start": dt_util.now().isoformat(), "summary": normal, "description": normal } )
    # This makes sure all reports for our requested line are returned in the output dict
    allitems_dict.update({look_for: items})
output = allitems_dict


