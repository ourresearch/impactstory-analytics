import os, logging, sys, analytics
from flask import Flask


# set up logging
# see http://wiki.pylonshq.com/display/pylonscookbook/Alternative+logging+configuration
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='[%(process)d] %(levelname)8s %(threadName)30s %(name)s - %(message)s'
)
logger = logging.getLogger("impactstoryanalytics")


# set up application
app = Flask(__name__)

# allow slashes and end of URLs even when they're not part of views:
# http://flask.pocoo.org/mailinglist/archive/2011/2/27/re-automatic-removal-of-trailing-slashes/#043b1a0b6e841ab8e7d38bd7374cbb58
app.url_map.strict_slashes = False


# setup segment.io
analytics.init(os.getenv("SEGMENTIO_KEY"), log_level=logging.DEBUG, flush_at=1)
analytics.identify(user_id='Heather', traits={
    "name": "Heather",
    "email": "heather@impactstory.org",
})
analytics.identify(user_id='Jason', traits={
    "name": "Jason",
    "email": "jason@impactstory.org",
})


# set up views
from impactstoryanalytics import views
