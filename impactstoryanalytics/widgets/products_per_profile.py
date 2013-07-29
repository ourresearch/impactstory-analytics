import time
from collections import defaultdict
import iso8601
import logging

from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.widgets.widget_api_helpers import Couchdb


logger = logging.getLogger("impactstoryanalytics.widgets.products_per_profile")

class Products_per_profile(Widget):

    def get_data(self):
        rows = Couchdb.get_view("products_per_collection/products_per_collection", True)
        result = []
        for row in rows:
            result.append({
            				"products_per_profile": row["key"], 
            				"number_of_profiles": row["value"],
            				"start_iso": "1900-01-01 00:00:00+00:00"  # dummy date to keep sparklines wrappers happy
            				})

        return result
