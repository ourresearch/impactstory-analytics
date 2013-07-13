import requests
import os
from datetime import date, timedelta

def get_data(user):

    env_key = "RESCUETIME_KEY_" + user.upper()
    rescuetime_api_key = os.getenv(env_key)

    params = {
        "key": rescuetime_api_key,
        "format": "json",
        "perspective": "interval",
        "resolution_time": "day",
        "restrict_kind": "category",
        "restrict_begin": date.today() - timedelta(days=6),
        "restrict_end": date.today() + timedelta(days=1)
    }
    url = "https://www.rescuetime.com/anapi/data"


    data = requests.get(url, params=params).json()["rows"]
    return data