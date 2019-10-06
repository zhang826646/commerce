from __future__ import absolute_import
from Commerce.celery import app

@app.task
def taskExample():
    print('i am task Example')
    return 'i am task Example'

import requests
from Commerce.settings import DING_URL
import json
@app.task
def sendDing(content,to=None):
    headers = {
        "Content-Type": "application/json",
        "Charset": "utf-8"
    }

    requests_data = {
        "msgtype": "text",
        "text": {
            "content": content
        },
        "at": {
            "atMobiles": [
            ],
            "isAtAll": True
        }
    }
    if to:
        requests_data['at']['atMobiles'].append(to)
        requests_data['at']['isAtAll']=False
    else:
        requests_data['at']['atMobiles'].clear()
        requests_data['at']['isAtAll'] = True

    sendData = json.dumps(requests_data)
    response = requests.post(url=DING_URL, headers=headers, data=sendData)
    content = response.json()
    return content


