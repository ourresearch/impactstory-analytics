import time
import requests
import iso8601
import logging
import redis
import os

from impactstoryanalytics.widgets.widget import Widget, by_hour
from impactstoryanalytics.widgets.widget_api_helpers import Keenio


logger = logging.getLogger("impactstoryanalytics.widgets.celery")

REDIS_CELERY_TASKS_DATABASE_NUMBER = 1
my_celery_redis = redis.from_url(os.getenv("REDIS_URL"), REDIS_CELERY_TASKS_DATABASE_NUMBER)

class Celery(Widget):

    def get_data(self):
        response = []

        #[(q, len(r_tasks.lrange(q, -10000, 10000))) for q in r_tasks.keys("core_*")]

        for queue_name_base in ["core_*", "celery"]:
            queue_length_total = 0
            for queue_name in my_celery_redis.keys(queue_name_base):
                queue_length = my_celery_redis.llen(queue_name)
                queue_length_total += queue_length
                if queue_length > 100:
                    logger.warning(u"HIGH celery queue length: {queue_name} is length {queue_length}".format(
                        queue_name=queue_name, queue_length=queue_length))

                response.append({"queue_name":queue_name, "queue_length":queue_length})

            response.append({"queue_name":queue_name_base+"TOTAL", "queue_length":queue_length_total})
            
        logger.info(u"celery queue length: {response}".format(
            response=response))
        return response



       
