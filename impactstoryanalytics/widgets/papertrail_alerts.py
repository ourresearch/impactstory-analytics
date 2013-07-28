import logging

from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.widgets.widget_api_helpers import Keenio

logger = logging.getLogger("impactstoryanalytics.widgets.papertrail_alerts")


class Papertrail_alerts(Widget):

    def get_data(self):
        queries = {}

        context_events = {
            "threw_exception": "Threw an Exception",
            "cant_start_thread": "Couldn't start a new thread",
            "threw_server_error": "Returned a server error from our API"
            }
        for event in context_events:
            queries[event] = {
                    "project": "context",
                    "analysis": "count",
                    "params": {"event_collection": context_events[event]}
                }

        production_events = {
            "provider_request_exception": "Received RequestException from Provider",
            "provider_error_response": "Received error response from Provider",
            "provider_timeout": "Received no response from Provider (timeout)",
            "api_user_limit_exceeded": "Raised Exception"
            }
        for event in production_events:
            queries[event] = {
                    "project": "production",
                    "analysis": "count",
                    "params": {"event_collection": production_events[event]}
                }

        shared_params = {
                    "timeframe": "last_30_days",
                    "target_property": "id",
                    "interval": "daily"
                }

        keenio = Keenio(queries, shared_params)
        raw_data = keenio.get_raw_data()
        return raw_data


