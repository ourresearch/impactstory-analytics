from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.widgets.widget_api_helpers import Keenio
from collections import defaultdict
import numpy

class Profile_load_times(Widget):

    def get_data(self):
        shared_params = {
            "timeframe": "this_30_days",
            "interval": "daily"
        }

        queries = {}
        queries["load_success"] = {
            "project": "production",
            "analysis": "extraction",
            "params": {
                "event_collection": "Completed profile load",
            }
        }
        queries["load_failure"] = {
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
                point["success_state"] = success_state
                all_points = self.add_to_points_list(point, all_points)


        return self.bin_points(all_points)


    def bin_points(self, points, num_bins=100, max_value=300):
        for point in points:
            point["num_products_ceil"] = min(point["number products"], max_value)

        keys = self.find_all_keys(points)

        bin_width = max_value / num_bins
        bins = []
        for bin_start in xrange(0, max_value, bin_width):
            bin = self.create_bin(bin_start, bin_start + bin_width, keys)

            for point in points:
                if bin["bin_start"] <= point["num_products_ceil"] < bin["bin_end"]:
                    key = self.key_for_this_point(point)
                    bin[key] += 1

            bins.append(bin)

        return bins


    def key_for_this_point(self, point):
        return "_".join([
            "num",
            point["success_state"],
            point["prev collection action"]
        ])

    def find_all_keys(self, points):
        keys = set()
        for point in points:
            key = self.key_for_this_point(point)
            keys.add(key)

        return list(keys)

    def create_bin(self, start, end, keys):
        bin = {
            "bin_start": start,
            "bin_end": end
        }

        for key in keys:
            bin[key] = 0

        return bin


    def add_to_points_list(self, new_point, points_list):
        required_keys = ["seconds", "number products", "prev collection action"]
        for required_key in required_keys:
            if required_key not in new_point.keys():
                return points_list

        points_list.append(new_point)
        return points_list


