import time
import requests
import iso8601
import logging

from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.widgets.widget_api_helpers import Keenio


logger = logging.getLogger("impactstoryanalytics.widgets.javascript_errors")


class Javascript_errors(Widget):

    def get_data(self):
        queries = {
            "both": {
                "project": "context",
                "analysis": "count",
                "params": {
                    "event_collection": "Caused a JavaScript error",
                    "target_property": "message",
                    "group_by": "isFirstOccurrence",
                }
            }
        }

        keenio = Keenio(queries)
        raw_data = keenio.get_raw_data()
        ungrouped_data = keenio.ungroup(raw_data, "both", "isFirstOccurrence", prepend_group_name=True)
        return ungrouped_data



       
