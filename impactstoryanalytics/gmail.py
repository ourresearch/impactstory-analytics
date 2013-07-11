import imaplib
import re
from impactstoryanalytics.lib import gmail_oauth2



def count_threads_in_inbox(client_id, client_secret, refresh_token, email_address):
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
