#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: wangjie
# datetime: 2022/7/22 5:05 下午
# software: PyCharm
from common.basic import get_config


class Url():

    def __init__(self):
        # 大app地址海外
        self.bigApp_Host_eu = get_config(name='bigAppHost', key='eu_url')
        # 大app地址国内
        self.bigApp_Host_ch = get_config(name='bigAppHost', key='ch_url')
        # 大app获取app基本信息
        self.bigApp_getBasicInfo = get_config(name='bigAppHost', key='bigApp_getBasicInfo')
        # 大app登录接口
        self.bigApp_login = get_config(name='bigAppHost', key='bigApp_login')
        # 验证码查询接口
        self.bigApp_getCode = get_config(name='bigAppHost', key='bigApp_getCode')
        # 大app用户反馈接口
        self.bigApp_feedback = get_config(name='bigAppHost', key='bigApp_feedback')
        # 大app验证码发送接口
        self.bigApp_sendSmsCode = get_config(name='bigAppHost', key='bigApp_sendSmsCode')

        # Lilly地址
        self.lilly_Host = get_config(name='lillyHost_online', key='url')
        # Lilly登录接口
        self.lilly_AppLogin = get_config(name='iot_api', key='iot_login')
        # Lilly网关实时数据接口
        self.lilly_getOneTemp = get_config(name='iot_api', key='iot_onetemp')
        # Lilly运单号查询接口
        self.lilly_selectOrders = get_config(name='iot_api', key='iot_selectOrders')
        # Lilly运单号查询接口
        self.lilly_orderDetail = get_config(name='iot_api', key='iot_orderDetail')

        # 冷链地址
        self.lenglian_Host = get_config(name='lenglianHost_online', key='url')
        # 冷链登录接口
        self.lenglian_login = get_config(name='iot_api', key='iot_login')

        # lora（中国）地址
        self.lora_CHN_Host = get_config(name='loraHost_online', key='CHNurl')
        # lora（中国）登录接口
        self.lora_CHN_login = get_config(name='iot_api', key='iot_login')
        # lora（中国）实时数据查询接口
        self.lora_CHN_relTimeTemp = get_config(name='iot_api', key='iot_realTimeTemp')