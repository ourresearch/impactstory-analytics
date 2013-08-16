import time
import requests
import iso8601
import logging

from impactstoryanalytics.widgets.widget import Widget, by_hour
from impactstoryanalytics.widgets.widget_api_helpers import Keenio


logger = logging.getLogger("impactstoryanalytics.widgets.exceptions")


class Exceptions(Widget):

    def get_data(self):
        queries = {
            "javascript": {
                "project": "context",
                "analysis": "count",
                "params": {
                    "event_collection": "Caused a JavaScript error",
                    "target_property": "message"
                }
            },
            "python": {
                "project": "context",
                "analysis": "count",
                "params": {
                    "event_collection": "Threw an Exception",
                    "target_property": "message"
                }
            },
            "daily_pageviews": {
                "project": "production",
                "analysis": "count",
                "params": {
                    "event_collection": "Loaded a page (custom)",
                    "target_property": "url"
                }
            }
        }

        shared_params = {
                    "timeframe": "this_30_days",  # want it to stay THIS so can see today
                    "interval": "daily"
                }

        keenio = Keenio(queries, shared_params)
        raw_data = keenio.get_raw_data()

        data_by_hour = by_hour(raw_data)
        return data_by_hour



       
