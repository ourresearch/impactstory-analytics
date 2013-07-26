from collections import defaultdict
import iso8601
import logging

from impactstoryanalytics.widgets.widget import Widget, get_raw_dataclip_data

logger = logging.getLogger("impactstoryanalytics.widgets.daily_new_users")


class Daily_new_users(Widget):

    new_accounts_query_url = "https://dataclips.heroku.com/brczfyjvdlovipuuukgjselrnilk.json"

    def get_raw_data(self, number_of_bins):
        data = defaultdict(list)

        accounts_data = get_raw_dataclip_data(self.new_accounts_query_url)

        dataclip_datapoints = accounts_data["values"][0:number_of_bins]

        response = []
        for datapoint in dataclip_datapoints:
            (date, new_accounts, total_accounts) = datapoint
            response.append({
                "start_iso": iso8601.parse_date(date).isoformat(),
                "new_accounts": int(new_accounts),
                "total_accounts": int(total_accounts)
                })

        return response


    def get_data(self):
        number_of_bins = 30  #show 30 days worth
        data = self.get_raw_data(number_of_bins)

        # javascript currently expects data with most recent data last
        data.reverse()

        return data
