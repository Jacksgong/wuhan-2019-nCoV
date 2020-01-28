# 获取武汉 2019nCov信息

[![](https://img.shields.io/badge/pip-v0.1.3%20Wuhan2019nCoV-yellow.svg)](https://pypi.python.org/pypi/Wuhan2019nCoV)

> 算是基本满足我的基本需求，要的自取，欢迎PR。

## 直接加入飞书接收通知

我和“武汉2019nCoV情况通知”的小伙伴都在飞书等你，用这个专属链接加入我们吧！https://go.feishu.cn/gYyh9M/

![](https://github.com/Jacksgong/wuhan-2019-nCoV/raw/master/arts/lark-invite-3.png)

## 安装

```
sudo pip install Wuhan2019nCoV
```

如果你是Mac OS，请通过Ruby安装`terminal-notifier`来接收通知:

```
sudo gem install terminal-notifier
```

## 升级

```
sudo pip install Wuhan2019nCoV --upgrade
```


## 使用

```
whncov
```

![](https://github.com/Jacksgong/wuhan-2019-nCoV/raw/master/arts/demo-v0.0.8.png)

```
=======================================================
<总数量变化>
=======================================================
<新增新闻>
--------------
<新增新闻>
--------------
<新增新闻>
--------------
[  =    ] [Last Refresh Success] waiting next check less 0s
```

```
$ whncov --help
-------------------------------------------------------
                  WuHan 2019nCov v0.1.3

     https://github.com/Jacksgong/wuhan-2019-nCoV
    This tool is used for crawl Wuhan 2019nCov Info

                   Hope You Safe!
-------------------------------------------------------
usage: whncov [-h] [-lark-url LARK_URL] [--hide-terminal-process]
              [--ignore-first-two-note]
              [dimension [dimension ...]]

This tool is used for crawl Wuhan 2019nCov Info

positional arguments:
  dimension             output dimensions: lark, terminal, all, mac

optional arguments:
  -h, --help            show this help message and exit
  -lark-url LARK_URL, --lark-url LARK_URL
                        the webhook or lark url for lark dimension for lark
                        notify
  --hide-terminal-process
                        whether need to hide process waiting output
  --ignore-first-two-note
                        whether need to ignore first two output
```


## LICENSE

```
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
```
