# coding=utf-8
"""
Copyright (C) 2020 Jacksgong.com.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import json
import re
from datetime import datetime

from wuhanncov.osx import notify
from wuhanncov.terminalcolor import colorize, YELLOW, GREEN


class Event:
    # {
    #     "sourceUrl": "https://weibo.com/2803301701/IqG2VvjtS?ref=home&rid=0_0_8_2704774672808346954_0_0_0&type=comment#_rnd1579684374015",
    #     "provinceName": "安徽省",
    #     "pubDate": 1579684171000,
    #     "title": "安徽确诊首例新型肺炎病例",
    #     "provinceId": "34",
    #     "createTime": 1579685159000,
    #     "summary": "22日16时，经国家卫生健康委确认，安徽省收到合肥市报告的首例新型冠状病毒感染的肺炎为确诊病例。另截至1月22日16时，省卫生健康委收到省内2市累计报告新型冠状病毒感染的肺炎疑似病例4例（合肥市3例，六安市1例）",
    #     "pubDateStr": "16分钟前",
    #     "modifyTime": 1579685159000,
    #     "infoSource": "人民日报",
    #     "id": 63
    # }
    def __init__(self, event_json):
        self.source_url = event_json['sourceUrl']
        self.source_name = event_json['infoSource']
        if 'provinceName' in event_json:
            self.province = event_json['provinceName']
        else:
            self.province = event_json['provinceId']

        self.timestamp_ms = event_json['pubDate']
        self.title = event_json['title']
        self.summary = event_json['summary']
        self.data_desc = event_json['pubDateStr']
        self.origin_json = event_json

    def dump_json(self):
        return json.dumps(self.origin_json, ensure_ascii=False)

    def print_desc(self, append_list=None):
        title = "%s - %s %s" % (self.title, self.source_name, datetime.fromtimestamp(self.timestamp_ms / 1000))
        if append_list is not None:
            append_list.append(title)

        print(colorize(title, fg=YELLOW))
        print(self.summary)

    def is_same(self, event):
        return self.summary == event.summary


class City:

    # {
    #     "sort": 1,
    #     "countryType": 1,
    #     "tags": "确诊 270 例，疑似 11 例，治愈 25 例，死亡 9 例",
    #     "createTime": 1579538652000,
    #     "id": 1,
    #     "modifyTime": 1579662606000,
    #     "operator": "zhanglifeng",
    #     "provinceId": "42",
    #     "provinceName": "湖北省"
    # }
    def __init__(self, city_json):
        self.sort = city_json['sort']
        self.is_mainland = city_json['countryType'] == 1
        self.create_timestamp_ms = city_json['createTime']
        self.modify_timestamp_ms = city_json['modifyTime']
        self.content = city_json['tags']
        self.province = city_json['provinceName']
        self.origin_json = city_json

    def dump_json(self):
        return json.dumps(self.origin_json, ensure_ascii=False)


class EventList:

    def __init__(self, event_list_json):
        self.event_list = list()
        self.origin_json = event_list_json
        for event in event_list_json:
            self.event_list.append(Event(event))

    def print_json(self, count=2):
        index = 0
        for event in self.event_list:
            if index >= count:
                break
            print(event.dump_json())
            index += 1

    def print_desc(self, count=2):
        index = 0
        change_list = list()
        for event in self.event_list:
            if index >= count:
                break
            event.print_desc(change_list)
            print("--------------                                               ")
            index += 1
        return change_list

    def print_desc_with_compare(self, last_event_list):
        top_event = last_event_list.event_list[0]
        next_event = last_event_list.event_list[1]
        third_event = last_event_list.event_list[3]
        change_list = list()
        for event in self.event_list:
            if event.is_same(next_event) or event.is_same(third_event):
                # 这种情况是最新的居然比旧的旧数据一样
                break
            if not event.is_same(top_event):
                print("--------------                                               ")
                event.print_desc(change_list)
            else:
                break
        return change_list


class Summary:
    def __init__(self, summary_json):
        # 全国 确诊 455 例 疑似 143 例 治愈 25 例 死亡 9 例
        self.content = summary_json['countRemark']
        self.deleted = summary_json['deleted'] != 'false'
        # 传播进展：疫情扩散中，存在病毒变异可能
        self.proceed = summary_json['summary']
        # 尚不明确；病毒：新型冠状病毒 2019-nCoV
        self.source = summary_json['infectSource']
        self.map_url = summary_json['imgUrl']
        # 未完全掌握，存在人传人、医务人员感染、一定范围社区传播
        self.passWay = summary_json['passWay']
        self.origin_json = summary_json

    def dump_json(self):
        return json.dumps(self.origin_json, ensure_ascii=False)

    def print_desc(self, last_summary=None):
        if last_summary is None or last_summary.content != self.content:
            print("=======================================================")
            print(colorize(self.content, fg=GREEN))
            print("=======================================================")
            return self.content
        return None


class DingXiangYuan:
    def __init__(self):
        pass

    @staticmethod
    def fetch():
        import requests

        headers = {
            'authority': '3g.dxy.cn',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
            'sec-fetch-user': '?1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8'
        }

        params = (
            ('scene', '2'),
            # ('clicktime', '1579578460'),
            # ('enterid', '1579578460'),
            ('from', 'timeline'),
            ('isappinstalled', '0'),
        )

        response = requests.get('https://3g.dxy.cn/newh5/view/pneumonia', headers=headers, params=params)
        # print response.content

        summary_re = re.compile(r'try *\{ *window\.getStatisticsService *=(.*)\}catch\(e\)')
        detail_re = re.compile(r'try *\{ *window\.getTimelineService *=(.*)\}catch\(e\)')

        is_in_body = False
        lines = response.content.splitlines()
        summary = None
        event_list = None
        for line in lines:
            if line.startswith("<body>"):
                is_in_body = True

            if line.startswith("</body>"):
                is_in_body = False

            if is_in_body:
                for content in line.split("</script>"):
                    match = summary_re.findall(content)
                    if match:
                        summary_json = json.loads(match[0])
                        summary = Summary(summary_json)
                    match = detail_re.findall(content)
                    if match:
                        detail_json = json.loads(match[0])
                        event_list = EventList(detail_json['result'])

        return summary, event_list
