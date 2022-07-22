#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: wangjie
# datetime: 2022/7/22 5:05 下午
# software: PyCharm
from common.basic import get_config,get_path


class Url():

    def __init__(self):
        # 大app地址
        self.bigApp_Host = get_config(name='bigAppHost', key='url')

        # 大app登录接口
        self.bigApp_login = get_config(name='bigAppHost', key='bigApp_login')

        # 大app注册接口
        self.bigApp_userRegister = get_config(name='bigAppHost', key='bigApp_userRegister')

        # 大app用户反馈接口
        self.bigApp_feedback = get_config(name='bigAppHost', key='bigApp_feedback')