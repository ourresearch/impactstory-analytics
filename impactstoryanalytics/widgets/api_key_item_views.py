import logging
import json

from impactstoryanalytics.widgets.widget import Widget, by_hour
from impactstoryanalytics.widgets.widget_api_helpers import Keenio
import impactstoryanalytics.widgets.widget_api_helpers as helpers

logger = logging.getLogger("impactstoryanalytics.widgets.api_key_item_views")


class Api_key_item_views(Widget):

    def get_data(self):
        queries = {
            "request": {
                "project": "production",
                "analysis": "count",
                "params": {
                "filters": '[{"property_name":"requested_to_view_item","operator":"eq","property_value":true}]'
                }
            }
        }
        shared_params = {
            "event_collection": "Received API request from external",
            "group_by": "api_key",
            "timeframe": "this_30_days",  # change to last_30_days after we have some data
            "interval": "daily"
        }

        keenio = Keenio(queries, shared_params)
        raw_data = keenio.get_raw_data()
        
        ungrouped = Keenio.ungroup(raw_data, "request", "api_key")

        all_api_keys = []
        for one_day_dict in ungrouped:
            all_api_keys += one_day_dict.keys()
        all_api_keys_set = set(all_api_keys)

        for one_day_dict in ungrouped:
            for api_key in all_api_keys_set:
                if api_key not in one_day_dict:
                    one_day_dict[api_key] = 0
            try:
                one_day_dict["EMPTY_STRING"] = one_day_dict[""]
                del one_day_dict[""]
            except KeyError:
                pass

        data_by_hour = by_hour(ungrouped)
        return data_by_hour

