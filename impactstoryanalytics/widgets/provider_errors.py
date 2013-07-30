import logging

from impactstoryanalytics.widgets.widget import Widget
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
                    "timeframe": "last_30_days",
                    "target_property": "id",
                    "interval": "daily"
                }

        keenio = Keenio(queries, shared_params)
        raw_data = keenio.get_raw_data()
        return raw_data


