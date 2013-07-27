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
        products_per_profile = {}
        for row in rows:
            products_per_profile[row["key"]] = row["value"]

        return products_per_profile
