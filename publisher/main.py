import time
import requests
import json
import xmltodict
import redis
import os
from apscheduler.schedulers.blocking import BlockingScheduler


def get_arrival_info():
    service_key = os.environ["SERVICE_KEY"]
    url = os.environ["API_URL"]
    station_id = os.environ["STATION_ID"]
    bus_id = os.environ["BUS_ID"]
    bus_order = os.environ["BUS_ORDER"]

    params = {"serviceKey": service_key, "stationId": station_id,
              "routeId": bus_id, "staOrder": bus_order}

    try:

        return requests.get(url, params=params).content

    except:

        return None


def publish_info(data):
    redis_host = os.environ["REDIS_HOST"]
    r = redis.Redis(host=redis_host, port=6379)
    r.publish(channel="main_channel", message=data)


def work():
    for i in range(360):
        data = get_arrival_info()
        publish_info(data)
        time.sleep(30)


if __name__ == "__main__":
    sched = BlockingScheduler(timezone="Asia/Seoul")
    sched.add_job(work, "cron", day_of_week="mon-fri", hour=5, minute=30)
    sched.start()
