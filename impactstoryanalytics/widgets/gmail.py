import time
import requests
import iso8601
import logging

from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.widgets.widget_api_helpers import Keenio


logger = logging.getLogger("impactstoryanalytics.widgets.gmail")


class Gmail(Widget):

    def get_data(self):
        queries = {
            "both": {
                "project": "context",
                "analysis": "minimum",
                "params": {
                    "event_collection": "Inbox check", 
                    "target_property": "thread_count",
                    "group_by": "userId",
                    "timeframe": "this_48_hours",
                    "interval": "hourly" 
                }
            }
        }

        keenio = Keenio(queries)
        raw_data = keenio.get_raw_data()
        return keenio.ungroup("both", "userId", raw_data)

       
