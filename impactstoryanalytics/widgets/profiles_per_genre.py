import time
from collections import defaultdict
import iso8601
import logging

from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.widgets.widget_api_helpers import Keenio



logger = logging.getLogger("impactstoryanalytics.widgets.profiles_per_genre")

class Profiles_per_genre(Widget):

    def get_data(self):
        target_properies = [
                    "without_response_count", 
                    "waiting_for_agent_count",
                    "total_count",
                    "median_open_days"
                ]
        queries = {}
        for target_property in target_properies:
            queries[target_property] = {
                    "project": "context",
                    "analysis": "minimum",
                    "params": {"target_property": target_property}
                }

        shared_params = {
                    "event_collection" : "UserVoice ticket stats",
                    "timeframe": "this_30_days",
                    "interval": "daily"
                }

        keenio = Keenio(queries, shared_params)
        raw_data = keenio.get_raw_data()
        return raw_data



        