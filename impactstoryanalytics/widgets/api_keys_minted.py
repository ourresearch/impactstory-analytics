from collections import defaultdict
import arrow
import logging
from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.widgets.widget import get_raw_dataclip_data


logger = logging.getLogger("impactstoryanalytics.widgets.api_keys_minted")


class Api_keys_minted(Widget):

    new_accounts_query_url = "https://dataclips.heroku.com/wfxdfophzccptmxhnjzlrraixnok.json"

    def get_data(self):
        datapoints = get_raw_dataclip_data(self.new_accounts_query_url)["values"]
        pans = self.get_time_pan_list(100)

        for datapoint in datapoints:
            (iso_time, api_keys_minted) = datapoint
            time = arrow.get(str(iso_time), 'YYYY-MM-DDTHH:mm:ss')
            pans.add_to_pan(time, "api_keys_minted", int(api_keys_minted))

        return pans.replace_NAs_with_zeroes().as_list()


