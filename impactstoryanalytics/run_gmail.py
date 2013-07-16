#!/usr/bin/env python

import os
import analytics
import logging
from impactstoryanalytics.lib import gmail_oauth2
import imaplib
import re

logger = logging.getLogger("analytics.run_gmail")



##############################################################################
#
#    functions
#
##############################################################################



def count_threads_in_inbox(self, client_id, client_secret, refresh_token, email_address):
    thread_id_list = []


    # renew the access token; it only last an hour.
    response = gmail_oauth2.RefreshToken(client_id, client_secret, refresh_token)
    access_token = response["access_token"]

    oAuthString = gmail_oauth2.GenerateOAuth2String(
        email_address,
        access_token,
        base64_encode=False
    ) #before passing into IMAPLib access token needs to be converted into string

    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.authenticate('XOAUTH2', lambda x: oAuthString)


    imap.select()
    _, data = imap.search(None, "ALL")


    # from http://docs.python.org/2/library/imaplib.html#imap4-example
    for email_num in data[0].split():
        _, data = imap.fetch(email_num, "(X-GM-THRID)")
        m = re.search("X-GM-THRID (\d+)", data[0])
        thread_id_list.append(m.group(1))

    unique_thread_count = len(set(thread_id_list))
    return unique_thread_count



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







##############################################################################
#
#    script
#
###############################################################################

for name in ["Heather", "Jason"]:
    check_inbox(name)


analytics.flush(async=False)  # make sure all the data gets sent to segment.io