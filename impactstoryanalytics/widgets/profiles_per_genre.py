import time
from collections import defaultdict
import iso8601
import logging

from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.widgets.widget_api_helpers import Keenio



logger = logging.getLogger("impactstoryanalytics.widgets.profiles_per_genre")

class Profiles_per_genre(Widget):

    def get_data(self):
        shared_params = {
                    "event_collection" : "Profiles per quasigenre",
                    "timeframe": "this_30_days",
                    "interval": "daily"
                }

        queries = {}
        queries["all"] = {
                "project": "context",
                "analysis": "extraction",
                "params": shared_params
            }

        keenio = Keenio(queries)
        raw_data = keenio.get_raw_data()
        return raw_data



        