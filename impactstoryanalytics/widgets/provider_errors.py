import logging

from impactstoryanalytics.widgets.widget import Widget, by_hour
from impactstoryanalytics.widgets.widget_api_helpers import Keenio

logger = logging.getLogger("impactstoryanalytics.widgets.provider_errors")


class Provider_errors(Widget):

    def get_data(self):
        queries = {}

        events = {
            "provider_request_exception": "Received RequestException from Provider",
            "provider_error_response": "Received error response from Provider",
            "provider_timeout": "Received no response from Provider (timeout)",
            }
        for event in events:
            queries[event] = {
                    "project": "production",
                    "analysis": "count",
                    "params": {"event_collection": events[event]}
                }

        shared_params = {
                    "timeframe": "this_30_days",  # WANT to include today for this one
                    "target_property": "id",
                    "interval": "daily"
                }

        keenio = Keenio(queries, shared_params)
        raw_data = keenio.get_raw_data()

        data_by_hour = by_hour(raw_data)

        return data_by_hour


