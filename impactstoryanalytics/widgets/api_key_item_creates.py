import logging
import json

from impactstoryanalytics.widgets.widget import Widget
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


