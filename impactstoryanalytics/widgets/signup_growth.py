import time
from collections import defaultdict
import iso8601
import logging

from impactstoryanalytics.widgets.widget import Widget, get_raw_dataclip_data
from impactstoryanalytics.widgets.widget_api_helpers import Converter



logger = logging.getLogger("impactstoryanalytics.widgets.signup_growth")


class Signup_growth(Widget):
    total_accounts_query_url = "https://dataclips.heroku.com/feblvvoknanzuiumyiawutmqdwbo.json"

    def get_weekly_growth_data(self):
        data = defaultdict(list)

        dataclip_data = get_raw_dataclip_data(self.total_accounts_query_url)

        JUNE2013 = "2013-06-01 00:00:00"
        dataclip_data = [datapoint for datapoint in dataclip_data["values"] if datapoint[0]>=JUNE2013]
        # start at 1 so we don't include today
        dataclip_data_weekly = dataclip_data[1::7]
        datapoints = []
        for datapoint in dataclip_data_weekly:
            (date, IGNORE, total_accounts_string) = datapoint 
            datapoints.append({
                "from_date": iso8601.parse_date(date), 
                "accounts": int(total_accounts_string)
                })
        new_accounts_per_week = [i["accounts"]-j["accounts"] for i, j in zip(datapoints[:-1], datapoints[1:])]

        merged_datapoints = []
        for datapoint, new_accounts in zip(datapoints[:-1], new_accounts_per_week):
            datapoint.update({"new_accounts_per_week": new_accounts})
            merged_datapoints.append(datapoint)
        merged_datapoints.reverse()

        for datapoint in merged_datapoints:
            print datapoint

            try:
                percent_growth = (100.0 * datapoint["new_accounts_per_week"]) / (datapoint["accounts"] - datapoint["new_accounts_per_week"])

                data["timestamp_list"].append(int(time.mktime(datapoint["from_date"].timetuple())))
                data["total_accounts"].append(datapoint["accounts"])
                data["new_accounts_per_week"].append(datapoint["new_accounts_per_week"])
                data["percent_growth"].append(round(percent_growth, 1))
            except TypeError:
                print "no data"
        return data


    def get_data(self):

        number_of_bins = 7  # eventually make this bins for 30 days
        data = self.get_weekly_growth_data()

        response = [
                    { 
                        "display": "accounts",
                        "name": "accounts",
                        "x": data["timestamp_list"], 
                        "y": data["total_accounts"]
                        }, 
                    { 
                        "display": "new accounts per week",
                        "name": "new_accounts_per_week",
                        "x": data["timestamp_list"], 
                        "y": data["new_accounts_per_week"]
                        }, 
                    {
                        "display": "% growth",
                        "name": "percent_growth",
                        "x": data["timestamp_list"], 
                        "y": data["percent_growth"]
                        }
                   ]
        return Converter.from_x_y_format(response)