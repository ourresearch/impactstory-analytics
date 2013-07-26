import time
import requests
import iso8601
import logging

from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.widgets.widget_api_helpers import Keenio


logger = logging.getLogger("impactstoryanalytics.widgets.gmail")


class Gmail(Widget):

    def get_data(self):
        query_urls = {"both": "minimum"}
        params = {
            "timeframe": "this_48_hours",
            "interval": "hourly", 
            "event_collection": "Inbox check", 
            "target_property": "thread_count",
            "group_by": "userId"
        }

        keenio = Keenio(query_urls, params, "context")
        raw_data = keenio.get_raw_data()
        return self.ungroup(raw_data)


    def ungroup(self, rows):
        """
        Tranform from Keenio's GroupBy format to our normal flat return format.
        here's what Keenio sends back (one row):
        {
            "both": [
                {
                    "userId": "Heather",
                    "result": 30
                },
                {
                    "userId": "Jason",
                    "result": 89
                }
            ],
            "end_iso": "2013-07-22T19:00:00-07:00",
            "start_iso": "2013-07-22T18:00:00-07:00"
        }
        """

        for row in rows:
            for userDict in row["both"]:
                key = userDict["userId"]
                val = userDict["result"]
                row[key] = val
            del row["both"]
        return rows

       
