from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.widgets.widget_api_helpers import Keenio

class Profile_load_times(Widget):

    def get_data(self):
        shared_params = {
            "timeframe": "this_30_days",
            "interval": "daily"
        }

        queries = {}
        queries["load success"] = {
            "project": "production",
            "analysis": "extraction",
            "params": {
                "event_collection": "Completed profile load",
            }
        }
        queries["load failure"] = {
            "project": "production",
            "analysis": "extraction",
            "params": {
                "event_collection": "Timed out profile load",
            }
        }

        keenio = Keenio(queries, shared_params)
        raw_data_dict = keenio.get_raw_data(True)
        all_points = []
        for success_state, datapoints in raw_data_dict.iteritems():

            for point in datapoints:
                if "prev collection action" not in point.keys():
                    continue

                new_point = {
                    "success state": success_state,
                    "seconds": point["seconds"],
                    "number products": point["number products"]
                }
                all_points.append(new_point)



        return all_points

