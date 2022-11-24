import requests
import json
from pathlib import Path
import os
path = os.path.join(os.path.split(__file__)[0], Path(
    __file__).resolve().parents[1], 'config', 'config.json')


def get_url():
    f = open(path, encoding='utf-8')
    config = json.load(f)

    return config['slack_url']


def send_error_notification(url, scraper_name, message, detail_msg, image):
    payload = json.dumps({
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": scraper_name
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message + '\n:information_source: ' + detail_msg
                },
                "accessory": {
                    "type": "image",
                            "image_url": image,
                    "alt_text": scraper_name
                }
            }
        ]
    })
    headers = {
        'Content-type': 'application/json'
    }

    requests.request("POST", url, headers=headers, data=payload)


def send_notification(url, scraper_name, message, image):
    payload = json.dumps({
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": scraper_name
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                },
                "accessory": {
                    "type": "image",
                    "image_url": image,
                    "alt_text": scraper_name
                }
            }
        ]
    })
    headers = {
        'Content-type': 'application/json'
    }

    requests.request("POST", url, headers=headers, data=payload)


# url = get_url()
# send_notification(url, ':etsy: Test', ':white_check_mark: Image Test',
    #   'https://s3.amazonaws.com/cdn.legalbaseportal.com/etsy.png')
