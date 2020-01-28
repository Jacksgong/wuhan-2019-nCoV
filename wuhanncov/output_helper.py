# coding=utf-8
from wuhanncov.lark import notify_lark
from wuhanncov.osx import notify_mac
from wuhanncov.terminalcolor import colorize, YELLOW, GREEN


def notify_event(event):
    title = event.get_title()
    if OutputHelper.is_terminal_output:
        colorized = colorize(title, fg=YELLOW) + "\n" + event.summary
        desc = "--------------                                               \n" + colorized
        print desc

    if OutputHelper.is_lark_output:
        notify_lark(title, event.summary, OutputHelper.lark_url)


def notify_summary(summary):
    if OutputHelper.is_terminal_output:
        print("=======================================================")
        print(colorize(summary.content, fg=GREEN))
        print("=======================================================")
    if OutputHelper.is_lark_output:
        notify_lark(msg=summary.content, lark_url=OutputHelper.lark_url)


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
