from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.widgets.widget_api_helpers import Keenio

class Embedded_widget_use(Widget):
    query_urls = {
        "pageviews":"https://api.keen.io/3.0/projects/51d858213843314922000002/queries/count?api_key=69023dd079bdb913522954c0f9bb010766be7e87a543674f8ee5d3a66e9b127f5ee641546858bf2c260af4831cd2f7bba4e37c22efb4b21b57bab2a36b9e8e3eccd57db3c75114ba0f788013a08f404738535e9a7eb8a29a30592095e5347e446cf61d50d5508a624934584e17a436ba&event_collection=Served%20a%20page%20with%20embedded%20widget&filters=%5B%7B%22property_name%22%3A%22domain%22%2C%22operator%22%3A%22ne%22%2C%22property_value%22%3A%22impactstory.org%22%7D%2C%7B%22property_name%22%3A%22domain%22%2C%22operator%22%3A%22ne%22%2C%22property_value%22%3A%22jsbin.org%22%7D%5D&timezone=0",
        "clickthroughs": "https://api.keen.io/3.0/projects/51d858213843314922000002/queries/count?api_key=69023dd079bdb913522954c0f9bb010766be7e87a543674f8ee5d3a66e9b127f5ee641546858bf2c260af4831cd2f7bba4e37c22efb4b21b57bab2a36b9e8e3eccd57db3c75114ba0f788013a08f404738535e9a7eb8a29a30592095e5347e446cf61d50d5508a624934584e17a436ba&event_collection=Loaded%20a%20page%20(custom)&filters=%5B%7B%22property_name%22%3A%22referrer_hostname%22%2C%22operator%22%3A%22ne%22%2C%22property_value%22%3A%22www.impactstory.org%22%7D%2C%7B%22property_name%22%3A%22referrer_hostname%22%2C%22operator%22%3A%22ne%22%2C%22property_value%22%3A%22impactstory.org%22%7D%2C%7B%22property_name%22%3A%22page_type%22%2C%22operator%22%3A%22eq%22%2C%22property_value%22%3A%22item%22%7D%2C%7B%22property_name%22%3A%22source%22%2C%22operator%22%3A%22eq%22%2C%22property_value%22%3A%22widget%22%7D%5D"
    }
    def get_data(self):
        keenio = Keenio(self.query_urls)
        raw = keenio.get_raw_data()
        return raw