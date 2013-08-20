import logging
import json

from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.widgets.widget_api_helpers import Keenio
import impactstoryanalytics.widgets.widget_api_helpers as helpers

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
                "params": {
                    "filters": filter_string,
                    "target_property": "api_key",
                    "event_collection": "Imported products",
                }
            }

        queries["profiles_created"] = {
            "project": "production",
            "analysis": "count",
            "params": {
                "event_collection": "Started a profile",
            }
        }

        shared_params = {
            "timeframe": "this_30_days",
            "interval": "daily"
        }

        keenio = Keenio(queries, shared_params)
        raw_data = keenio.get_raw_data()
        processed_data = self.process_data(raw_data)
        return processed_data

    def process_data(self, rows):
        for row in rows:
            row["orcid_perc"] = helpers.perc(row["orcid"], row["profiles_created"])
            row["bibtex_perc"] = helpers.perc(row["bibtex"], row["profiles_created"])

        return rows[0:-1]  # remove today



