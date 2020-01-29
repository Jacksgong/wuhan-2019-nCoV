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
from os import mknod
from os.path import exists

import requests

from wuhanncov.output_helper import notify_event, notify_summary
from wuhanncov.terminalcolor import colorize, YELLOW


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
        self.summary = event_json['summary'].strip()
        self.data_desc = event_json['pubDateStr']
        self.origin_json = event_json

    def dump_json(self):
        return json.dumps(self.origin_json, ensure_ascii=False)

    def get_title(self):
        return u"%s - %s %s" % (self.title, self.source_name, datetime.fromtimestamp(self.timestamp_ms / 1000))

    def is_same(self, event):
        # return self.title == event.title and self.source_name == event.source_name \
        #        and self.timestamp_ms / 1000 == event.timestamp_ms / 1000
        return self.get_title().__eq__(event.get_title()) or \
               (self.summary == event.summary and self.timestamp_ms == event.timestamp_ms)

    def __hash__(self):
        return hash(self.get_title())

    def __gt__(self, other):
        return self.timestamp_ms > other.timestamp_ms


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
    last_top_event_cache = None

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
            change_list.append(event)
            index += 1

        self.print_list(change_list)
        return change_list

    def print_desc_with_compare(self, last_event_list):
        if len(self.event_list) <= 0:
            return list()

        last_top_event = last_event_list.event_list[0]
        last_second_event = last_event_list.event_list[1]
        last_third_event = last_event_list.event_list[3]
        new_top_event = self.event_list[0]
        if new_top_event.timestamp_ms < last_top_event.timestamp_ms:
            # print "time not match, cache new[" + new_top_event.get_title() + "] older than last[" + last_top_event.get_title() + "]"
            return list()

        change_list = list()
        for event in self.event_list:
            if event.is_same(last_second_event) or event.is_same(last_third_event):
                # 这种情况是最新的居然比旧的旧数据一样
                break

            if not event.is_same(last_top_event):
                change_list.append(event)
            else:
                break

        if len(change_list) > 0:
            last_top = last_top_event.get_title()
            change_top = change_list[0].get_title()
            new_top = self.event_list[0].get_title()
            # print "test--------------"
            # print "last top: " + last_top + " last size: " + len(last_event_list.event_list).__str__()
            # print "change top: " + change_top + " change size: " + len(change_list).__str__()
            # print "new top: " + new_top + " new size: " + len(self.event_list).__str__()
            # print "test--------------"

            if self.last_top_event_cache is not None and self.last_top_event_cache == change_top:
                print "wrong last[%s] change[%s] == " % (self.last_top_event_cache, new_top)
                discard_event = None
                for change_event in change_list:
                    if change_event.get_title() == self.last_top_event_cache:
                        discard_event = change_event
                        break
                if discard_event is not None:
                    change_list.remove(discard_event)
            self.last_top_event_cache = last_top
        elif len(self.event_list) < len(last_event_list.event_list):
            # print "test-----------------"
            # print "length not match, cache new[" + new_top_event.get_title() + "] " + len(
            #     self.event_list).__str__() + " older than last[" + last_top_event.get_title() + "]" + len(
            #     last_event_list.event_list).__str__()
            # print "new: "
            # for event in self.event_list:
            #     print event.get_title()
            # print "old: "
            # for event in last_event_list.event_list:
            #     print event.get_title()
            # print "test-----------------"
            return list()

        self.print_list(change_list)

        return change_list

    @staticmethod
    def print_list(news_event_list):
        old_to_new_list = reversed(news_event_list)
        for event in old_to_new_list:
            notify_event(event)


class Summary:
    def __init__(self, summary_json=None):
        self.confirm_count = 0
        self.suspect_count = 0
        self.dead_count = 0
        self.survive_count = 0

        self.deleted = False

        # 确诊 2823 例，疑似 5794 例 死亡 81 例，治愈 58 例
        self.content = u"确诊 %d 例，疑似 %d 例，死亡 %d 例，治愈 %d 例" % (
            self.confirm_count, self.suspect_count, self.dead_count, self.survive_count)

        # 传播进展：疫情扩散中，存在病毒变异可能
        self.proceed = ''
        # 尚不明确；病毒：新型冠状病毒 2019-nCoV
        self.source = ''
        self.map_url = ''
        # 未完全掌握，存在人传人、医务人员感染、一定范围社区传播
        self.passWay = ''
        self.origin_json = summary_json

        if summary_json is not None:
            self.restore_from_json(summary_json)

    def dump_json(self):
        return json.dumps(self.origin_json, ensure_ascii=False)

    def print_desc(self, last_summary=None):
        if last_summary is None or (
                last_summary.content != self.content and self.confirm_count >= last_summary.confirm_count
                and self.survive_count >= last_summary.survive_count):
            increase_confirm_count = 0
            increase_survive_count = 0
            increase_dead_count = 0
            if last_summary is not None:
                increase_confirm_count = self.confirm_count - last_summary.confirm_count
                increase_survive_count = self.survive_count - last_summary.survive_count
                increase_dead_count = self.dead_count - last_summary.dead_count
            notify_summary(self, increase_confirm_count, increase_dead_count, increase_survive_count)
            return self.content
        return None

    def write_to_file(self, path):
        summary_path = path + '/summary'

        # with open(summary_path, 'w') as outfile:
        #     json.dumps(self.origin_json, outfile, ensure_ascii=False)

    def restore_from_file(self, path):
        summary_path = path + '/summary'
        if not exists(summary_path):
            return None

        print 'restore summary from ' + summary_path
        with open(summary_path) as json_file:
            origin_json = json.load(json_file, ensure_ascii=False)
            self.restore_from_json(origin_json)

        return self

    def restore_from_json(self, summary_json):
        self.confirm_count = int(summary_json['confirmedCount'])
        self.suspect_count = int(summary_json['suspectedCount'])
        self.dead_count = int(summary_json['deadCount'])
        self.survive_count = int(summary_json['curedCount'])

        self.deleted = summary_json['deleted'] != 'false'

        # 确诊 2823 例，疑似 5794 例 死亡 81 例，治愈 58 例
        self.content = u"确诊 %d 例，疑似 %d 例，死亡 %d 例，治愈 %d 例" % (
            self.confirm_count, self.suspect_count, self.dead_count, self.survive_count)

        # 传播进展：疫情扩散中，存在病毒变异可能
        self.proceed = summary_json['summary']
        # 尚不明确；病毒：新型冠状病毒 2019-nCoV
        self.source = summary_json['virus']
        self.map_url = summary_json['imgUrl']
        # 未完全掌握，存在人传人、医务人员感染、一定范围社区传播
        self.passWay = summary_json['passWay']
        self.origin_json = summary_json


class DingXiangYuan:
    def __init__(self):
        print colorize("丁香园实时: ", fg=YELLOW) + "https://3g.dxy.cn/newh5/view/pneumonia"

    @staticmethod
    def fetch():

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

        response = requests.get('https://3g.dxy.cn/newh5/view/pneumonia', headers=headers)
        # print response.content

        summary_re = re.compile(r'try *\{ *window\.getStatisticsService *=(.*)\}catch\(e\)')
        detail_re = re.compile(r'try *\{ *window\.getTimelineService *=(.*)\}catch\(e\)')

        is_in_body = False
        lines = response.content.splitlines()
        summary = None
        event_list = None
        for line in lines:
            if line.startswith("<body"):
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
                        event_list = EventList(detail_json)

        return summary, event_list
