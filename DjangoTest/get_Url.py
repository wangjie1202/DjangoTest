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
        # 大app获取app基本信息
        self.bigApp_getBasicInfo = get_config(name='bigAppHost', key='bigApp_getBasicInfo')
        # 大app登录接口
        self.bigApp_login = get_config(name='bigAppHost', key='bigApp_login')
        # 验证码查询接口
        self.bigApp_getCode = get_config(name='bigAppHost', key='bigApp_getCode')
        # 大app用户反馈接口
        self.bigApp_feedback = get_config(name='bigAppHost', key='bigApp_feedback')

        # Lilly地址
        self.lilly_Host = get_config(name='lillyHost_online', key='url')
        # Lilly登录接口
        self.lilly_AppLogin = get_config(name='iot_api', key='iot_login')

        # 冷链地址
        self.lenglian_Host = get_config(name='lenglianHost_online', key='url')
        # 冷链登录接口
        self.lenglian_login = get_config(name='iot_api', key='iot_login')