import logging
import json

from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.widgets.widget_api_helpers import Keenio
import impactstoryanalytics.widgets.widget_api_helpers as helpers

logger = logging.getLogger("impactstoryanalytics.widgets.importers_used")


class Provider_requests(Widget):

    def get_data(self):
        queries = {}
        queries["requests"] = {
            "project": "production",
            "analysis": "count",
            "params": {
                "event_collection": "Sent GET to Provider",
                "group_by": "provider"
            }
        }

        shared_params = {
            "timeframe": "this_30_days",
            "interval": "daily"
        }

        keenio = Keenio(queries, shared_params)
        raw_data = keenio.get_raw_data()

        ungrouped = Keenio.ungroup(raw_data, "requests", "provider")
        return ungrouped


