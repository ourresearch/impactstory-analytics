import time
from datetime import timedelta
from collections import defaultdict
import iso8601
import logging

from impactstoryanalytics.widgets.widget import Widget, get_raw_dataclip_data, get_raw_keenio_data
from impactstoryanalytics.widgets.widget_api_helpers import Converter


logger = logging.getLogger("impactstoryanalytics.widgets.monthly_active_users")

class Monthly_active_users(Widget):

    total_accounts_query_url = "https://dataclips.heroku.com/feblvvoknanzuiumyiawutmqdwbo.json"
    active_accounts_query_pattern = "https://api.keen.io/3.0/projects/51d858213843314922000002/queries/count_unique?api_key=69023dd079bdb913522954c0f9bb010766be7e87a543674f8ee5d3a66e9b127f5ee641546858bf2c260af4831cd2f7bba4e37c22efb4b21b57bab2a36b9e8e3eccd57db3c75114ba0f788013a08f404738535e9a7eb8a29a30592095e5347e446cf61d50d5508a624934584e17a436ba&event_collection=Loaded%20own%20profile&filters=%5B%7B%22property_name%22%3A%22keen.created_at%22%2C%22operator%22%3A%22lt%22%2C%22property_value%22%3A%22{from_date}%22%7D%2C%7B%22property_name%22%3A%22keen.created_at%22%2C%22operator%22%3A%22gte%22%2C%22property_value%22%3A%22{to_date}%22%7D%5D&target_property=user.userId"

    def format_date(self, date):
        date_only = date.isoformat()[0:10]
        return date_only

    def get_raw_data(self, number_of_bins):
        data = defaultdict(list)

        total_accounts = get_raw_dataclip_data(self.total_accounts_query_url)

        # start at 1 so that we don't include today
        datapoints = total_accounts["values"][1:number_of_bins+1]
        # javascript currently expects data with most recent data last
        datapoints.reverse()

        for datapoint in datapoints:
            (date, new_accounts, total_accounts) = datapoint

            from_date = iso8601.parse_date(date)
            to_date = from_date - timedelta(days=30)

            active_accounts_query_url = self.active_accounts_query_pattern.format(
                from_date = self.format_date(from_date), 
                to_date = self.format_date(to_date))
            active_accounts = get_raw_keenio_data(active_accounts_query_url)

            fraction_active = (0.0+int(active_accounts)) / int(total_accounts)

            data["timestamp_list"].append(int(time.mktime(from_date.timetuple())))
            data["total_accounts"].append(int(total_accounts))
            data["monthly_active_accounts"].append(int(active_accounts))
            data["percent_monthly_active_users"].append(round(100*fraction_active, 1))

        return data


    def get_data(self):
        number_of_bins = 30  # eventually make this bins for 30 days
        data = self.get_raw_data(number_of_bins)

        response = [
                    { 
                        "display": "accounts",
                        "name": "accounts",
                        "x": data["timestamp_list"], 
                        "y": data["total_accounts"]
                        }, 
                    { 
                        "display": "monthly actives",
                        "name": "monthly_actives",
                        "x": data["timestamp_list"], 
                        "y": data["monthly_active_accounts"]
                        }, 
                    {
                        "display": "% MAU",
                        "name": "percent_MAU",
                        "x": data["timestamp_list"], 
                        "y": data["percent_monthly_active_users"]
                        }
                   ]
        return Converter.from_x_y_format(response)