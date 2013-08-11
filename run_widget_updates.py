#!/usr/bin/env python

import os
import logging
import argparse

import impactstoryanalytics
from impactstoryanalytics.views import dashboards, widget_data_raw


logger = logging.getLogger("analytics.run_widget_updates")


def run_widget_updates(dashboards_to_update=None):

    if not dashboards_to_update:
        dashboards_to_update = dashboards.keys()

    for dashboard in dashboards_to_update:
        logger.info("getting fresh data for all widgets on dashboard {dashboard}".format(
            dashboard=dashboard))

        for widget_name in dashboards[dashboard]:
            logger.info("adding fresh data to cache for widget {widget_name}".format(
                widget_name=widget_name))

            widget_response = widget_data_raw(widget_name, get_from_cache=False)  # force getting fresh data




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='update widget data')

    parser.add_argument('--today', help="just update the today and realtime dashboards instead of all of them", action="store_true")
    args = parser.parse_args()
    if args.today:
        run_widget_updates(["today", "realtime"])
    else:
        run_widget_updates()


