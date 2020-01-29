# coding=utf-8
import subprocess
import re
import sys
import time
from datetime import datetime

import requests

lark_url = sys.argv[1]
log_path = sys.argv[2]


def notify_lark(title=None, msg=""):
    url = lark_url
    if not url.startswith('http'):
        print "lark webhook url not valid %s" % url

    if title is not None:
        payload = "{\n\n\"title\": \"" + title + "\",\n\"text\": \"" + msg + "\"\n\n} "
    else:
        payload = "{\n\n\"text\": \"" + msg + "\"\n\n} "

    headers = {
        'Content-Type': 'application/json'
    }

    # payload = u' '.join([payload]).encode('utf-8').strip()
    print payload

    response = requests.request("POST", url, headers=headers, data=payload)
    print response.content


print "lark url: " + lark_url
print "log path: " + log_path

while True:
    # get whether service is exist
    result = subprocess.check_output("ps aux| grep whncov", shell=True)
    lines = result.splitlines()
    alive = False
    for line in lines:
        if '/usr/bin/python /usr/local/bin/whncov' in line:
            alive = True
            break

    if not alive:
        # get tail log
        tail_log = subprocess.check_output("tail -n 5 " + log_path, shell=True)
        latest_log = tail_log.splitlines()[-1]
        tail_log = tail_log.replace('\n', '\\n')
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        tail_log = ansi_escape.sub('', tail_log)

        print datetime.now().strftime('%y-%m-%d %I:%M:%S %p') + "not exist! " + latest_log
        notify_lark("service not exist(0)", latest_log)
        notify_lark(latest_log, tail_log)
        break
    time.sleep(10)
