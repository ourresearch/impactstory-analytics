from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.widgets.widget_api_helpers import Keenio

class Profile_load_fail_fraction(Widget):
    def get_data(self):
        queries = {
            "successful_loads": {
                "project": "production",
                "analysis": "count",
                "params": {
                    "event_collection": "Completed profile load",
                }
            },
            "failed_loads": {
                "project": "production",
                "analysis": "count",
                "params": {
                    "event_collection": "Timed out profile load",
                }
            }
        }

        shared_params = {
            "filters": '[{"property_name":"collection id","operator":"eq","property_value":"q1kvih"}]',
            "timeframe": "this_30_days",
            "interval": "daily"
        }

        keenio = Keenio(queries, shared_params)
        raw = keenio.get_raw_data()

        for datapoint in raw:
            datapoint["total_loads"] = datapoint["successful_loads"] + datapoint["failed_loads"]

        return raw
