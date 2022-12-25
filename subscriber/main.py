import json
import xmltodict
import redis
import os
import time
from slack_webhook import Slack
from apscheduler.schedulers.blocking import BlockingScheduler


def send_slack_msg(contents):
    slack_webhook_url = os.environ["SLACK_WEBHOOK_URL"]
    slack = Slack(url=slack_webhook_url)
    if contents:
        slack.post(text=contents)


def extract_data(res):
    contents = ''
    try:
        data = json.loads(json.dumps(xmltodict.parse(
            res.decode('utf-8')), indent=4, ensure_ascii=False))

        result_code = data["response"]["msgHeader"]["resultCode"]
        if result_code == "0":
            contents = f"```버스 도착 정보 🚎\n\n{data['response']['msgBody']['busArrivalItem']['locationNo1']}정거장 전\n{data['response']['msgBody']['busArrivalItem']['predictTime1']}분 후 도착\n남은 좌석 수 {data['response']['msgBody']['busArrivalItem']['remainSeatCnt1']}\n```"

            return contents

        else:

            return contents

    except:
        return contents


def subscribe_info():
    redis_host = os.environ["REDIS_HOST"]
    r = redis.Redis(host=redis_host, port=6379)
    s = r.pubsub()
    s.subscribe("main_channel")

    for i in range(2880):
        res = s.get_message()
        if res is not None and res['type'] == 'message':
            contents = extract_data(res['data'])
            send_slack_msg(contents)
        time.sleep(5)

    return


if __name__ == "__main__":
    sched = BlockingScheduler(timezone="Asia/Seoul")
    sched.add_job(subscribe_info, "cron", day_of_week="mon-fri", hour=5)
    sched.start()
