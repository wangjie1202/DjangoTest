import csv
import json
from io import StringIO
from time import sleep
from turtle import pd

import requests
from django.http import HttpResponse
from django.shortcuts import render
from common.log import Log

log = Log()

# Create your views here.

##### 首页 #####
from DjangoTest.get_Url import Url


def index(request):
    return render(request, 'index.html')

##### 大app选择接口页面 #####
def bigApp_ApiList(request):
    return render(request, 'bigApp_ApiList.html')

##### 大App获取app基本信息页面 #####
def bigApp_getBasicInfo(request):
# 判断前端请求类型
    if(request.method=='GET'):
        return render(request, 'bigApp_getBasicInfo.html')
    else:
        bigApp_getBasicInfo = Url().bigApp_Host + Url().bigApp_getBasicInfo
        log.warning(bigApp_getBasicInfo)
        parameter_type = request.POST
        log.warning(parameter_type)

        ##### 判断入参条件
        if(parameter_type['btn_longin']=='发送json'):
            if(parameter_type['parameter']!=''):
                data_json = json.loads(request.POST['parameter'])
                response = requests.post(url=bigApp_getBasicInfo, data=data_json)
                log.info(response.json())
                return HttpResponse(response)
            else:
                return HttpResponse("请求参数不可为空！")

        if(parameter_type['btn_longin']=='发送文件'):
            if(len(parameter_type)==1):
                # 读取上传的csv文件
                file_input = request.FILES.get('file_csv', '')
                file_data = file_input.read().decode("utf-8")
                csv_data = csv.reader(StringIO(file_data), delimiter=',')
                list_csv = []
                for read in csv_data:
                    list_csv.append(read)
                resp_list = []

                # 遍历入参数量并批量执行请求测试，合并输出返回结果
                count = 0
                for i in list_csv:
                    data = json.loads(i[0])
                    resp = requests.post(url=bigApp_getBasicInfo, data=data)
                    log.info(resp.request.body)
                    sleep(2)
                    count +=1
                    temp = '第'+str(count)+'条case响应结果：' + str(resp.json()) + ' '
                    log.info(resp.json())
                    resp_list.append(temp)
                log.warning(resp_list)
                return HttpResponse(resp_list)

            else:
                return HttpResponse("请上传文件后再提交！")


##### 大app登录接口测试 #####
def bigApp_login(request):
    # 判断前端请求类型
    if(request.method=='GET'):
        return render(request, 'bigApp_login.html')
    else:
        login_url_bigApp = Url().bigApp_Host + Url().bigApp_login
        log.warning(login_url_bigApp)
        parameter_type = request.POST
        log.warning(parameter_type)

        ##### 判断入参条件
        if(parameter_type['btn_longin']=='发送json'):
            if(parameter_type['parameter']!=''):
                data_json = json.loads(request.POST['parameter'])
                response = requests.post(url=login_url_bigApp, data=data_json)
                log.info(response.json())
                return HttpResponse(response)
            else:
                return HttpResponse("请求参数不可为空！")

        if(parameter_type['btn_longin']=='发送文件'):
            if(len(parameter_type)==1):
                # 读取上传的csv文件
                file_input = request.FILES.get('file_csv', '')
                file_data = file_input.read().decode("utf-8")
                csv_data = csv.reader(StringIO(file_data), delimiter=',')
                list_csv = []
                for read in csv_data:
                    list_csv.append(read)
                resp_list = []

                # 遍历入参数量并批量执行请求测试，合并输出返回结果
                count = 0
                for i in list_csv:
                    data = json.loads(i[0])
                    resp = requests.post(url=login_url_bigApp, data=data)
                    log.info(resp.request.body)
                    sleep(2)
                    count +=1
                    temp = '第'+str(count)+'条case响应结果：' + str(resp.json()) + ' '
                    resp_list.append(temp)
                log.info(HttpResponse(resp_list))
                return HttpResponse(resp_list)

            else:
                return HttpResponse("请上传文件后再提交！")