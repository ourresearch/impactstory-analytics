import logging
import json

from impactstoryanalytics.widgets.widget import Widget
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
            "timeframe": "today",
            "interval": "daily"
        }

        keenio = Keenio(queries, shared_params)
        raw_data = keenio.get_raw_data()

        ungrouped = Keenio.ungroup(raw_data, "request", "api_key")
        for mydict in ungrouped:
            try:
                mydict["EMPTY_STRING"] = mydict[""]
                del mydict[""]
            except KeyError:
                pass

        return ungrouped


