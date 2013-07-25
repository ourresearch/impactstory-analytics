import time
import requests
import iso8601
import logging

from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.widgets.widget_api_helpers import Keenio




logger = logging.getLogger("impactstoryanalytics.widgets.gmail")


class Gmail(Widget):

    query_urls = {"both": "https://api.keen.io/3.0/projects/51df37f0897a2c7fcd000000/queries/minimum?api_key=b915f0ca9fcbe1cc4760640adf9f09fa1d330f74c763bfd1aa867d6148f528055a3f97afc6b111e8905ef78bfe7f97d1d2dd2b7ddbb0f9ed8e586fd69d79f12f2215d06298924631d8ccfa7a12845dde94921855ae223c69ad26789dca2ec5fd26296a80af72c3a014df5554948bac8e&event_collection=Inbox%20check&timezone=-25200&target_property=thread_count&group_by=userId"}
    params = {
        "timeframe": "this_48_hours",
        "interval": "hourly"
    }

    def get_data(self):
        keenio = Keenio(self.query_urls)
        keenio.params.update(self.params)
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