import logging
import arrow

from impactstoryanalytics.widgets.widget import Widget

import widget_api_helpers



logger = logging.getLogger("impactstoryanalytics.widgets.signup_funnel")


class Signup_funnel(Widget):
    def get_data(self):
        mixpanel_data = widget_api_helpers.Mixpanel.get_data("omtm")
        return self.convert_to_timepan_format(mixpanel_data)



    def convert_to_timepan_format(self, mixpanel_data):
        days_dict = mixpanel_data["omtm"]
        days_list = []
        for iso_day in sorted(days_dict.keys()):
            day = days_dict[iso_day]
            day["start_iso"] = arrow.get(str(iso_day), 'YYYY-MM-DD').isoformat(" ")
            days_list.append(day)

            for i, step in enumerate(day["steps"]):

                day[str(i) + "_count"] = step["count"]
                day[str(i) + "_conv"] = step["step_conv_ratio"] * 100



            day["signup_conv"] = 100 * day["3_count"] / day["0_count"]
            del day["steps"]
            del day["analysis"]



        return days_list

