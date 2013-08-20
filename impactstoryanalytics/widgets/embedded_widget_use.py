from impactstoryanalytics.widgets.widget import Widget
from impactstoryanalytics.widgets.widget_api_helpers import Keenio

class Embedded_widget_use(Widget):
    def get_data(self):
        queries = {
            "pageviews": {
                "project": "production",
                "analysis": "count",
                "params": {
                    "event_collection": "Served a page with embedded widget",
                    "filters": '[{"property_name":"domain","operator":"ne","property_value":"impactstory.org"},{"property_name":"domain","operator":"ne","property_value":"jsbin.org"}]',
                }
            },
            "clickthroughs": {
                "project": "production",
                "analysis": "count",
                "params": {
                    "event_collection": "Loaded a page (custom)",
                    "filters": '[{"property_name":"referrer_hostname","operator":"ne","property_value":"www.impactstory.org"},{"property_name":"referrer_hostname","operator":"ne","property_value":"impactstory.org"},{"property_name":"page_type","operator":"eq","property_value":"item"},{"property_name":"source","operator":"eq","property_value":"widget"}]'
                }
            }            
        }
        keenio = Keenio(queries)
        raw = keenio.get_raw_data()
        return raw
