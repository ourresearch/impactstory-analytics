import logging
import json

from impactstoryanalytics.widgets.widget import Widget, by_hour
from impactstoryanalytics.widgets.widget_api_helpers import Keenio
import impactstoryanalytics.widgets.widget_api_helpers as helpers

logger = logging.getLogger("impactstoryanalytics.widgets.api_key_item_creates")


class Api_key_item_creates(Widget):

    def get_data(self):
        queries = {
            "request": {
                "project": "production",
                "analysis": "count",
                "params": {}
            }
        }
        shared_params = {
            "event_collection": "Created item because of registration",
            "group_by": "api_key",
            "timeframe": "this_30_days", # change to last_30_days after we have some data
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
                try:
                    if not one_day_dict[api_key]:
                        one_day_dict[api_key] = 0
                except KeyError:
                    pass
            try:
                one_day_dict["EMPTY_STRING"] = one_day_dict[""]
                del one_day_dict[""]
            except KeyError:
                pass

        data_by_hour = by_hour(ungrouped)
        return data_by_hour

