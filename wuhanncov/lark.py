import requests


def notify_lark(title=None, msg="", lark_url=""):
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

    payload = u' '.join([payload]).encode('utf-8').strip()

    requests.request("POST", url, headers=headers, data=payload)
