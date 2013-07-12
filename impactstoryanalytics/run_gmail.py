#!/usr/bin/env python

import os
import analytics
import logging
from impactstoryanalytics import gmail

logger = logging.getLogger("analytics.get_gmail")


def check_inbox(name):
    logger.info("Getting inbox thread count for " + name.capitalize())
    count = gmail.count_threads_in_inbox(
        os.getenv("GMAIL_CLIENT_ID"),
        os.getenv("GMAIL_CLIENT_SECRET"),
        os.getenv("GMAIL_REFRESH_TOKEN_" + name.upper()),
        os.getenv("GMAIL_ADDRESS_" + name.upper())
    )

    logger.info("found " + str(count) + " threads threads in " + name + "'s inbox.")

    analytics.track(user_id=name.capitalize(), event='Inbox check', properties={
        "thread_count": count
    })

for name in ["Heather", "Jason"]:
    check_inbox(name)


analytics.flush(async=False)  # make sure all the data gets sent to segment.io