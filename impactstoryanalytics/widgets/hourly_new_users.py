from collections import defaultdict
import iso8601
import arrow
import logging

from impactstoryanalytics.widgets.widget import Widget, get_raw_dataclip_data

logger = logging.getLogger("impactstoryanalytics.widgets.hourly_new_users")


class Hourly_new_users(Widget):

    new_accounts_query_url = "https://dataclips.heroku.com/hefcjkzcteluxosfhdvsofefjrjr.json"
    def get_data(self):
        number_of_datapoints = 72
        datapoints = get_raw_dataclip_data(self.new_accounts_query_url)["values"][0:number_of_datapoints]
        pans = Widget.get_time_pan_list(number_of_datapoints, interval="hour")

        for datapoint in datapoints:
            (iso_time, new_accounts, total_accounts) = datapoint
            time = arrow.get(str(iso_time), 'YYYY-MM-DDTHH:mm:ss')
            pans.add_to_pan(time, "new_accounts", int(new_accounts))

        return pans.replace_NAs_with_zeroes().as_list()
