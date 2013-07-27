import logging
import json

from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.widgets.widget_api_helpers import Keenio

logger = logging.getLogger("impactstoryanalytics.widgets.importers_used")


class Importers_used(Widget):

    def get_data(self):
        importer_names = ["orcid", "bibtex"]
        queries = {}
        for importer_name in importer_names:
            filters = [{
                "property_name": "import source",
                "operator": "eq",
                "property_value": importer_name
            }]
            filter_string = json.dumps(filters)
            print "here's the filter string: ", filter_string

            queries[importer_name] = {
                "project": "production",
                "analysis": "count",
                "params": {"filters": filter_string}
            }

        shared_params = {
            "event_collection" : "Imported products",
            "timeframe": "this_30_days",
            "interval": "daily"
        }

        keenio = Keenio(queries, shared_params)
        raw_data = keenio.get_raw_data()
        return raw_data


