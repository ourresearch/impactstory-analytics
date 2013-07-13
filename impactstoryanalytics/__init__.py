import os, logging, sys, analytics
from flask import Flask


# set all the environmental variables defined in the .env list
try:
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', ".env"))
    with open(path, "r") as f:
        str = f.read()

    for line in str.split("\n"):
        try:
            key, val = line.split("=")
            os.environ[key] = val
        except ValueError:
            continue  # line wasn't a value assignment, move on
except IOError:
    pass  # we're on the server, not local; env vars are already set.


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
