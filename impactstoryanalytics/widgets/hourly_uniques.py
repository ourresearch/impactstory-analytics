import time
import requests
import iso8601
import logging

from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.widgets.widget_api_helpers import Keenio


logger = logging.getLogger("impactstoryanalytics.widgets.hourly_uniques")


class Hourly_uniques(Widget):

    def get_data(self):
        queries = {
            "hourly_uniques": {
                "project": "production",
                "analysis": "count_unique",
                "params": {
                    "event_collection": "Loaded a page (custom)",
                    "target_property": "user.userId",
                    "timeframe": "this_24_hours",
                    "interval": "hourly"
                }
            }
        }

        keenio = Keenio(queries)
        raw_data = keenio.get_raw_data()
        return raw_data



       
