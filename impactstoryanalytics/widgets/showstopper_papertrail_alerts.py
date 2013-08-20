import logging

from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.widgets.widget_api_helpers import Keenio

logger = logging.getLogger("impactstoryanalytics.widgets.showstopper_papertrail_alerts")


class Showstopper_papertrail_alerts(Widget):

    def get_data(self):
        queries = {}

        events = {
            "cant_start_thread": "Couldn't start a new thread",
            "threw_server_error": "Returned a server error from our API"
            }
        for event in events:
            queries[event] = {
                    "project": "context",
                    "analysis": "count",
                    "params": {"event_collection": events[event]}
                }

        shared_params = {
                    "timeframe": "this_30_days",
                    "target_property": "id",
                    "interval": "daily"
                }

        keenio = Keenio(queries, shared_params)
        raw_data = keenio.get_raw_data()
        return raw_data


