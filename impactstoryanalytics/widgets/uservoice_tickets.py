import time
from collections import defaultdict
import iso8601
import logging

from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.widgets.widget_api_helpers import Keenio



logger = logging.getLogger("impactstoryanalytics.widgets.uservoice_tickets")

class Uservoice_tickets(Widget):

    def get_data(self):
        queries = {}
        queries["all"] = {
                "project": "context",
                "analysis": "extraction",
                "params": {
                    "event_collection" : "UserVoice ticket stats",
                    "timeframe": "this_30_days",
                    "interval": "daily"                
                }
            }

        keenio = Keenio(queries)
        raw_data = keenio.get_raw_data()

        # bug in keenio that it ignores this_30_days, so get it this way
        raw_data = raw_data[-30:]

        return raw_data

        