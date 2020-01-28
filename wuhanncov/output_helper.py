# coding=utf-8
from wuhanncov.lark import notify_lark
from wuhanncov.osx import notify_mac
from wuhanncov.terminalcolor import colorize, YELLOW, GREEN


def notify_event(event):
    title = event.get_title()
    if OutputHelper.is_terminal_output:
        colorized = colorize(title, fg=YELLOW) + "\n" + event.summary + "\n" + event.source_url
        desc = "--------------                                               \n" + colorized
        print(u' '.join([desc]).encode('utf-8').strip())

    if OutputHelper.is_lark_output:
        msg = u"%s\\n%s" % (event.summary, event.source_url)
        notify_lark(title, msg, OutputHelper.lark_url)


def notify_summary(summary, increase_confirm_count, increase_dead_count, increase_survive_count):
    title = ''
    if increase_confirm_count > 0:
        title = u"%s 新增确诊 %d 例" % (title, increase_confirm_count)
    if increase_dead_count > 0:
        title = u"%s 新增死亡 %d 例" % (title, increase_dead_count)
    if increase_survive_count > 0:
        title = u"%s 新增痊愈 %d 例" % (title, increase_survive_count)

    if OutputHelper.is_terminal_output:
        print("=======================================================")
        terminal_info = colorize(summary.content, fg=GREEN)
        if len(title) > 0:
            terminal_info = "[" + title + "] " + terminal_info

        print(u' '.join([terminal_info]).encode('utf-8').strip())
        print("=======================================================")
    if OutputHelper.is_lark_output:
        notify_lark(title=title, msg=summary.content, lark_url=OutputHelper.lark_url)


def notify_mac_msg(notify_title, notify_message_list):
    if not OutputHelper.is_mac_output:
        return

    if notify_title is None:
        if len(notify_message_list) > 0:
            OutputHelper.last_mac_title = notify_message_list[0].get_title()
            notify_title = OutputHelper.last_mac_title
        else:
            notify_title = None
    else:
        if len(notify_message_list) > 0:
            OutputHelper.last_mac_title = notify_message_list[0].get_title()
        else:
            OutputHelper.last_mac_title = "无新闻只有总数变化"

    if notify_title is not None:
        try:
            message = u"最后一条: %s" % OutputHelper.last_mac_title
        except UnicodeDecodeError:
            message = u"最后一条: <未知>"

        subtitle = u"包含更新%d条" % len(notify_message_list)
        notify_mac(title=notify_title,
                   subtitle=subtitle,
                   message=message)


class OutputHelper:
    is_terminal_output = True
    is_lark_output = False
    is_mac_output = True
    last_mac_title = None
    lark_url = None

    def __init__(self):
        pass
