import logging

from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.widgets.widget_api_helpers import Keenio

logger = logging.getLogger("impactstoryanalytics.widgets.api_keey_limit_exceeded")


class Api_key_limit_exceeded(Widget):

    def get_data(self):
        queries = {}

        queries["api_key_limit_exceeded"] = {
                "project": "production",
                "analysis": "count",
                "params": {
                    "event_collection": "Raised Exception",
                    "exception class": "ApiLimitExceededException"
                    }
            }

        shared_params = {
                    "timeframe": "last_30_days",
                    "target_property": "id",
                    "interval": "daily"
                }

        keenio = Keenio(queries, shared_params)
        raw_data = keenio.get_raw_data()
        return raw_data


