import time
from sys import stdout
from threading import Thread

from wuhanncov.dingxiangyuan import DingXiangYuan

bar = [
    " [=     ]",
    " [ =    ]",
    " [  =   ]",
    " [   =  ]",
    " [    = ]",
    " [     =]",
    " [    = ]",
    " [   =  ]",
    " [  =   ]",
    " [ =    ]",
]


class CheckLoop:

    def __init__(self):
        self.last_summary = None
        self.last_event_list = None

    def _fetch(self):
        summary, event_list = DingXiangYuan().fetch()

        if self.last_summary is None:
            summary.print_desc()
            event_list.print_desc()
        else:
            summary.print_desc(self.last_summary)
            event_list.print_desc_with_compare(self.last_event_list)

        self.last_summary = summary
        self.last_event_list = event_list

    def start(self):
        # first enter just print news
        self._fetch()

        i = 0
        interval_sec = 5
        thread = None
        while True:
            try:
                if thread and thread.isAlive():
                    info = 'checking news'
                else:
                    interval_sec -= .2
                    info = "waiting next check less %ds" % interval_sec

                print(bar[i % len(bar)] + ' ' + info + '\r'),
                i += 1
                stdout.flush()
                time.sleep(.2)

                if interval_sec <= 0:
                    thread = Thread(target=self._fetch)
                    thread.start()
                    interval_sec = 5
            except KeyboardInterrupt:
                exit(0)
