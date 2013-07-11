#!/usr/bin/env python

import os
import analytics
import logging
from impactstoryanalytics import gmail

# initialize the ImpactStory project ..
analytics.init('u94q3yg6t5ifx3hyi1rn')
logger = logging.getLogger("analytics.get_gmail")

logger.info("Getting inbox thread count for Heather")
count = gmail.count_threads_in_inbox(
    os.getenv("GMAIL_CLIENT_ID"),
    os.getenv("GMAIL_CLIENT_SECRET"),
    os.getenv("GMAIL_REFRESH_TOKEN_HEATHER"),
    os.getenv("GMAIL_ADDRESS_HEATHER")
)

print count
