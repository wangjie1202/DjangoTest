import csv
import json
import re

import xlsxwriter
from io import StringIO
from time import sleep
import requests
from django.http import HttpResponse
from django.shortcuts import render

from common.basic import get_filePath, timeStampToStyleTime, timeToStamp, getUTCStamp, getNowStrfTime
from common.log import Log
from DjangoTest.get_Url import Url

log = Log()

# Create your views here.

##### 首页 #####
def index(request):
    return render(request, 'index.html')

##### 大app选择接口页面 #####
def bigApp_ApiList(request):
    return render(request, 'bigApp_ApiList.html')

##### 大App获取app基本信息页面 #####
def bigApp_getBasicInfo(request):
    """
    TODO 大App获取app基本信息页面
    """
# 判断前端请求类型
    if(request.method=='GET'):
        return render(request, 'bigApp_getBasicInfo.html')
    else:
        parameter_type = request.POST
        log.info(parameter_type)
        # 选择要访问的服务器
        if parameter_type['gatewayt_type'] == '1':
            website = Url().bigApp_Host_ch + Url().bigApp_getBasicInfo
            log.info(website)
        elif parameter_type['gatewayt_type'] == '2':
            website = Url().bigApp_Host_eu + Url().bigApp_getBasicInfo
            log.info(website)
        else:
            return HttpResponse("地区选择错误！")

        ##### 判断入参条件
        if(parameter_type['btn_longin']=='发送请求'):
            if(parameter_type['parameter']!=''):
                data_json = json.loads(request.POST['parameter'])
                response = requests.post(url=website, data=data_json)
                log.info(response.json())
                if response.status_code != 200:
                    return render(request, 'error.html')
                else:
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
                    resp = requests.post(url=website, data=data)
                    log.info(resp.request.body)
                    sleep(2)
                    count +=1
                    temp = '第'+str(count)+'条case响应结果：' + str(resp.json()) + ' '
                    log.info(resp.json())
                    resp_list.append(temp)
                log.info(resp_list)
                return HttpResponse(resp_list)

            else:
                return HttpResponse("请上传文件后再提交！")

##### 大app登录接口测试 #####
def bigApp_login(request):
    """
    TODO 大app登录接口测试
    """
    # 判断前端请求类型
    if(request.method=='GET'):
        return render(request, 'bigApp_login.html')
    else:
        parameter_type = request.POST
        log.info(parameter_type)
        # 选择要访问的服务器
        if parameter_type['gatewayt_type'] == '1':
            website = Url().bigApp_Host_ch + Url().bigApp_login
            log.info(website)
        elif parameter_type['gatewayt_type'] == '2':
            website = Url().bigApp_Host_eu + Url().bigApp_login
            log.info(website)
        else:
            return HttpResponse("地区选择错误！")

        ##### 判断入参条件
        if(parameter_type['btn_longin']=='发送请求'):
            if(parameter_type['parameter']!='' and parameter_type['content_type']!=''):
                data_json = json.loads(request.POST['parameter'])
                headers = json.loads(request.POST['content_type'])
                response = requests.post(url=website, headers=headers, json=data_json)
                log.info(response.json())
                if response.status_code != 200:
                    return render(request, 'error.html')
                else:
                    if response.json()['code']==0:
                        token = response.json()['data']['token']
                        userAuth = get_filePath("common/user_auth.txt")
                        with open(userAuth, 'w') as f:
                            f.write('token ' + token)
                        f.close()
                        return HttpResponse(response)
                    else:
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
                    resp = requests.post(url=website, data=data)
                    log.info(resp.request.body)
                    sleep(2)
                    count +=1
                    temp = '第'+str(count)+'条case响应结果：' + str(resp.json()) + ' '
                    resp_list.append(temp)
                log.info(HttpResponse(resp_list))
                return HttpResponse(resp_list)

            else:
                return HttpResponse("请上传文件后再提交！")

##### 大app用户反馈接口 #####
def bigApp_feedBack(request):
    """
    TODO 大app用户反馈接口
    """
    # 判断前端请求类型
    if(request.method=='GET'):
        return render(request, 'bigApp_feedBack.html')
    else:
        parameter_type = request.POST
        log.info(parameter_type)
        # 选择要访问的服务器
        if parameter_type['gatewayt_type'] == '1':
            website = Url().bigApp_Host_ch + Url().bigApp_feedback
            log.info(website)
        elif parameter_type['gatewayt_type'] == '2':
            website = Url().bigApp_Host_eu + Url().bigApp_feedback
            log.info(website)
        else:
            return HttpResponse("地区选择错误！")

        ##### 判断入参条件
        if(parameter_type['btn_longin']=='发送请求'):
            if(parameter_type['parameter']!='' and parameter_type['content_type']!=''):
                data_json = json.loads(request.POST['parameter'])
                headers = json.loads(request.POST['content_type'])

                # token使用判断
                if(parameter_type['token']==''):
                    with open(get_filePath('common/user_auth.txt')) as f:
                        token = f.read()
                        f.close()
                    headers['AUTHORIZATION'] = token
                else:
                    headers['AUTHORIZATION'] = 'token '+ json.loads(json.dumps(request.POST['token']))

                log.debug(headers)
                response = requests.post(url=website, headers=headers, json=data_json)
                log.info(response.json())
                if response.status_code != 200:
                    return render(request, 'error.html')
                else:
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
                    resp = requests.post(url=website, data=data)
                    log.info(resp.request.body)
                    sleep(2)
                    count +=1
                    temp = '第'+str(count)+'条case响应结果：' + str(resp.json()) + ' '
                    resp_list.append(temp)
                log.info(HttpResponse(resp_list))
                return HttpResponse(resp_list)

            else:
                return HttpResponse("请上传文件后再提交！")

##### 大app验证码查询接口 #####
def bigApp_getCode(request):
    """
    TODO 大app验证码查询接口
    """
    # 判断前端请求类型
    if(request.method=='GET'):
        return render(request, 'bigApp_getCode.html')
    else:
        parameter_type = request.POST
        log.info(parameter_type)

        # 选页面要使用的功能
        if parameter_type['func_type'] == '1':
            api = Url().bigApp_sendSmsCode
        elif parameter_type['func_type'] == '2':
            api = Url().bigApp_getCode
        else:
            return HttpResponse("功能选择错误！")

        # 选择要访问的服务器
        if parameter_type['gatewayt_type'] == '1':
            website = Url().bigApp_Host_ch + api
            log.info(website)
        elif parameter_type['gatewayt_type'] == '2':
            website = Url().bigApp_Host_eu + api
            log.info(website)
        else:
            return HttpResponse("地区选择错误！")

        ##### 判断入参
        if(parameter_type['btn_longin']=='发送请求'):

            # 判断入参类型
            if(parameter_type['acc_type']=="acc_phone" and parameter_type['acc_type']!="" ):

                # 判断入参参数
                if(parameter_type['perTelphone']!='' and parameter_type['telphone']!=''):
                    perTelphone = json.loads(json.dumps(request.POST['perTelphone']))
                    telphone = json.loads(json.dumps(request.POST['telphone']))

                    # 判断请求是否为注册
                    if parameter_type['func_type'] == '1':
                        sendCode_type = parameter_type['sendCode_type']
                        data_json = {"telphone": telphone, "pretelphone": perTelphone, "type": sendCode_type}
                    elif parameter_type['func_type'] == '2':
                        data_json ={"telphone": telphone, "pretelphone": perTelphone}
                    log.info(data_json)
                    headers = json.loads(request.POST['content_type'])
                    response = requests.post(url=website, headers=headers, json=data_json)
                    log.info(response.json())

                    # 断言系统code码
                    if response.status_code != 200:
                        return render(request, 'error.html')
                    else:
                        if response.json()['code'] != 0:
                            return HttpResponse(response)
                        else:
                            # 判断请求是否为注册决定返回的数据
                            if parameter_type['func_type'] == '1':
                                return HttpResponse(response)
                            elif parameter_type['func_type'] == '2':
                                code = response.json()['data']['code']
                                return HttpResponse("验证码：" + str(code))
                else:
                    return HttpResponse("请求参数不可为空！")

            elif(parameter_type['acc_type']=="acc_email" and parameter_type['acc_type']!="" ):
                if (parameter_type['email'] != ''):
                    email = json.loads(json.dumps(request.POST['email']))

                    # 判断请求是否为注册
                    if parameter_type['func_type'] == '1':
                        sendCode_type = parameter_type['sendCode_type']
                        data_json = {"email": email, "type": sendCode_type}
                    elif parameter_type['func_type'] == '2':
                        data_json = {"email": email}
                    log.info(data_json)
                    headers = json.loads(request.POST['content_type'])
                    response = requests.post(url=website, headers=headers, json=data_json)
                    log.info(response.json())
                    if response.status_code != 200:
                        return render(request, 'error.html')
                    else:
                        if response.json()['code'] != 0:
                            return HttpResponse(response)
                        else:
                            # 判断请求是否为注册决定返回的数据
                            if parameter_type['func_type'] == '1':
                                return HttpResponse(response)
                            elif parameter_type['func_type'] == '2':
                                code = response.json()['data']['code']
                                return HttpResponse("验证码：" + str(code))
                else:
                    return HttpResponse("请求参数不可为空！")
            else:
                return HttpResponse("请求参数不可为空！")

##### lilly选择接口页面 #####
def lilly_ApiList(request):
    return render(request, 'lilly_ApiList.html')

##### Lilly 登录接口测试 #####
def lilly_login(request):
    """
    TODO Lilly 登录接口测试
    """
    # 判断前端请求类型
    if(request.method=='GET'):
        return render(request, 'lilly_login.html')
    else:
        website = Url().lilly_Host + Url().lilly_AppLogin
        log.info(website)
        parameter_type = request.POST
        log.info(parameter_type)

        ##### 判断入参条件
        if(parameter_type['btn_longin']=='发送请求'):
            if(parameter_type['parameter']!='' and parameter_type['content_type']!=''):
                data_json = json.loads(request.POST['parameter'])
                headers = json.loads(request.POST['content_type'])
                response = requests.post(url=website, headers=headers, json=data_json)
                log.info(response.json())
                log.info(response.headers)
                if response.status_code != 200:
                    return render(request, 'error.html')
                else:
                    if response.json()['result'] != 200:
                        return HttpResponse(response)
                    else:
                        # 正则提取csrftoken和sessionid
                        temp = response.headers['Set-Cookie']
                        csrftoken = re.findall('csrftoken=(.*?); expires', temp)
                        csrftoken = csrftoken[0]
                        sessionid = re.findall('sessionid=(.*?); expires=', temp)
                        sessionid = sessionid[0]

                        # 写入cookie
                        userAuth = get_filePath("common/lilly_cookie.txt")
                        with open(userAuth, 'w') as f:
                            f.write('csrftoken=' + csrftoken + ';sessionid=' + sessionid)
                        f.close()
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
                    resp = requests.post(url=website, data=data)
                    log.info(resp.request.body)
                    sleep(2)
                    count +=1
                    temp = '第'+str(count)+'条case响应结果：' + str(resp.json()) + ' '
                    resp_list.append(temp)
                log.info(HttpResponse(resp_list))
                return HttpResponse(resp_list)

            else:
                return HttpResponse("请上传文件后再提交！")

##### Lilly 网关实时数据下载接口 #####
def lilly_getOneTemp(request):
    """
    TODO Lilly 网关实时数据下载接口
    """
    # 判断前端请求类型
    if(request.method=='GET'):
        return render(request, 'lilly_getOneTemp.html')
    else:
        website_getOrders = Url().lilly_Host + Url().lilly_selectOrders
        website_getOneTemp = Url().lilly_Host + Url().lilly_getOneTemp
        log.info('请求地址：' + website_getOrders)
        parameter_type = request.POST
        log.info(parameter_type)

        ##### 判断入参条件
        if (parameter_type['order'] != '' and parameter_type['mmcid'] != '' and parameter_type['content_type'] != ''):
            order = json.loads(json.dumps(parameter_type['order']))
            mmc_id = json.loads(json.dumps(parameter_type['mmcid']))
            data_json = {"number": order}
            headers = json.loads(request.POST['content_type'])

            # token使用判断
            if (parameter_type['token'] == ''):
                with open(get_filePath('common/lilly_cookie.txt')) as f:
                    token = f.read()
                    f.close()
                headers['Cookie'] = token
            else:
                headers['Cookie'] =json.loads(json.dumps(request.POST['token']))
            log.info('请求参数：' + str(data_json))
            response = requests.post(url=website_getOrders, headers=headers, json=data_json)
            log.info(response.json())
            log.info(response.headers)
            if response.status_code != 200:
                return render(request, 'error.html')
            else:
                if response.json()['result'] != 0 or response.json()['orders'] == []:
                    return HttpResponse('运单号：' + order + '查询无结果，请检查运单号是否正确。')
                else:
                    get_orderId = None
                    get_Start_time = None
                    get_End_time = None
                    gw_resp_data = response.json()['orders']
                    for i in range(0, len(gw_resp_data)):
                        get_tagId = gw_resp_data[i]['mac']
                        if (mmc_id == get_tagId):
                            get_orderId = gw_resp_data[i]['order_id']
                            get_Start_time = gw_resp_data[i]['start_time']
                            get_End_time = gw_resp_data[i]['end_time']
                            break
                        elif (i + 1 == len(gw_resp_data)):
                            log.error('未找到 ' + mmc_id)
                            return HttpResponse('未找到秒秒测ID：' + mmc_id + '相关温度数据。')
                    if get_End_time == '':
                        get_Start_time = timeToStamp(get_Start_time)
                        get_End_time = getUTCStamp()
                    else:
                        get_Start_time = timeToStamp(get_Start_time)
                        get_End_time = timeToStamp(get_End_time)

                    log.info(mmc_id + ' 查询指定温度标签成功')

                    order_data = {
                        "start_time": get_Start_time,
                        "end_time": get_End_time,
                        "order_id": get_orderId
                    }
                    log.info('请求地址：' + website_getOneTemp)
                    log.info('请求参数：' + str(order_data))
                    resp = requests.post(url=website_getOneTemp, headers=headers, json=order_data)
                    if response.status_code != 200:
                        return render(request, 'error.html')
                    else:
                        resp_data = resp.json()['data']
                        tempExcel = get_filePath('common/data/' + mmc_id + '.xls')
                        writebook = xlsxwriter.Workbook(tempExcel)
                        writesheet = writebook.add_worksheet(mmc_id)

                        # 从A1单元格开始填充rowTitle的数据
                        rowTitle = ['time', 'temp', 'rssi', 'location', 'tag_battery']
                        writesheet.write_row('A1', rowTitle)
                        for i in range(0, len(rowTitle)):
                            writesheet.write(0, i, rowTitle[i])

                        # 写入Excel单元格
                        for col in range(0, len(resp_data)):
                            # 写入时间
                            utc8 = (int(resp_data[col]['scan_time']) + 8 * 60 * 60)
                            writesheet.write(col + 1, 0, timeStampToStyleTime(utc8))
                            # 写入温度
                            writesheet.write(col + 1, 1, resp_data[col]['temperature'])
                            # 写入信号
                            writesheet.write(col + 1, 2, resp_data[col]['rssi'])
                            # 写入GPS
                            writesheet.write(col + 1, 3, resp_data[col]['scan_location'])
                            # 写入Battery
                            writesheet.write(col + 1, 4, int(resp_data[col]['battery']))
                        writebook.close()
                        log.info('excel生成完毕，开始下载文件...')
                        with open(tempExcel, 'rb') as model_excel:
                            result = model_excel.read()
                        response = HttpResponse(result)
                        response['Content-Disposition'] = 'attachment; filename='+ mmc_id + '.xlsx'
                        return response
        else:
            return HttpResponse("请求参数不可为空！")

##### Lilly 网关实时数据最新查询 #####
def lilly_getCurrentOneTemp(request):
    """
    TODO Lilly 网关实时数据最新查询
    """
    # 判断前端请求类型
    if(request.method=='GET'):
        return render(request, 'lilly_getCurrentOneTemp.html')
    else:
        website_getOrders = Url().lilly_Host + Url().lilly_selectOrders
        website_getOneTemp = Url().lilly_Host + Url().lilly_getOneTemp
        log.info('请求地址：' + website_getOrders)
        parameter_type = request.POST
        log.info(parameter_type)

        ##### 判断入参条件
        if (parameter_type['order'] != '' and parameter_type['mmcid'] != '' and parameter_type['content_type'] != ''):
            order = json.loads(json.dumps(parameter_type['order']))
            mmc_id = json.loads(json.dumps(parameter_type['mmcid']))
            data_json = {"number": order}
            headers = json.loads(request.POST['content_type'])

            # token使用判断
            if (parameter_type['token'] == ''):
                with open(get_filePath('common/lilly_cookie.txt')) as f:
                    token = f.read()
                    f.close()
                headers['Cookie'] = token
            else:
                headers['Cookie'] =json.loads(json.dumps(request.POST['token']))
            log.info('请求参数：' + str(data_json))
            response = requests.post(url=website_getOrders, headers=headers, json=data_json)
            log.info(response.json())
            log.info(response.headers)
            if response.status_code != 200:
                return render(request, 'error.html')
            else:
                if response.json()['result'] != 0 or response.json()['orders'] == []:
                    return HttpResponse('运单号：' + order + '查询无结果，请检查运单号是否正确。')
                else:
                    get_orderId = None
                    get_Start_time = None
                    get_End_time = None
                    gw_resp_data = response.json()['orders']
                    for i in range(0, len(gw_resp_data)):
                        get_tagId = gw_resp_data[i]['mac']
                        if (mmc_id == get_tagId):
                            get_orderId = gw_resp_data[i]['order_id']
                            get_Start_time = gw_resp_data[i]['start_time']
                            get_End_time = gw_resp_data[i]['end_time']
                            break
                        elif (i + 1 == len(gw_resp_data)):
                            log.error('未找到 ' + mmc_id)
                            return HttpResponse('未找到秒秒测ID：' + mmc_id + '相关温度数据。')
                    if get_End_time == '':
                        get_Start_time = timeToStamp(get_Start_time)
                        get_End_time = getUTCStamp()
                    else:
                        get_Start_time = timeToStamp(get_Start_time)
                        get_End_time = timeToStamp(get_End_time)

                    log.info(mmc_id + ' 查询指定温度标签成功')

                    order_data = {
                        "start_time": get_Start_time,
                        "end_time": get_End_time,
                        "order_id": get_orderId
                    }
                    log.info('请求地址：' + website_getOneTemp)
                    log.info('请求参数：' + str(order_data))
                    resp = requests.post(url=website_getOneTemp, headers=headers, json=order_data)
                    if response.status_code != 200:
                        return render(request, 'error.html')
                    else:
                        resp_data = resp.json()['data']
                        utc8 = int(resp_data[-1]['scan_time']) + 8 * 60 * 60
                        temperature = resp_data[-1]['temperature']
                        location = resp_data[-1]['scan_location']
                        return HttpResponse("当前时间：" + timeStampToStyleTime(utc8)+"，当前温度：" + temperature +"，当前经纬度：" + location)
        else:
            return HttpResponse("请求参数不可为空！")

##### 冷链选择接口页面 #####
def lenglian_ApiList(request):
    return render(request, 'lenglian_ApiList.html')

##### 冷链 登录接口测试 #####
def lenglian_login(request):
    """
    TODO 冷链 登录接口测试
    """
    # 判断前端请求类型
    if(request.method=='GET'):
        return render(request, 'lenglian_login.html')
    else:
        website = Url().lenglian_Host + Url().lenglian_login
        log.info(website)
        parameter_type = request.POST
        log.info(parameter_type)

        ##### 判断入参条件
        if(parameter_type['btn_longin']=='发送请求'):
            if(parameter_type['parameter']!='' and parameter_type['content_type']!=''):
                data_json = json.loads(request.POST['parameter'])
                headers = json.loads(request.POST['content_type'])
                response = requests.post(url=website, headers=headers, json=data_json)
                log.info(response.json())
                log.info(response.headers)
                if response.status_code != 200:
                    return render(request, 'error.html')
                else:
                    if response.json()['result'] != 200:
                        return HttpResponse(response)
                    else:
                        # 正则提取csrftoken和sessionid
                        temp = response.headers['Set-Cookie']
                        csrftoken = re.findall('csrftoken=(.*?); expires', temp)
                        csrftoken = csrftoken[0]
                        sessionid = re.findall('sessionid=(.*?); expires=', temp)
                        sessionid = sessionid[0]

                        # 写入cookie
                        userAuth = get_filePath("common/lilly_cookie.txt")
                        with open(userAuth, 'w') as f:
                            f.write('csrftoken=' + csrftoken + ';sessionid=' + sessionid)
                        f.close()
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
                    resp = requests.post(url=website, data=data)
                    log.info(resp.request.body)
                    sleep(2)
                    count +=1
                    temp = '第'+str(count)+'条case响应结果：' + str(resp.json()) + ' '
                    resp_list.append(temp)
                log.info(HttpResponse(resp_list))
                return HttpResponse(resp_list)

            else:
                return HttpResponse("请上传文件后再提交！")

##### lora选择接口页面 #####
def lora_ApiList(request):
    return render(request, 'lora_ApiList.html')

##### Lora 登录接口测试 #####
def lora_login(request):
    """
    TODO Lora 登录接口测试
    """
    # 判断前端请求类型
    if(request.method=='GET'):
        return render(request, 'lora_login.html')
    else:
        website = Url().lora_CHN_Host + Url().lora_CHN_login
        log.info(website)
        parameter_type = request.POST
        log.info(parameter_type)

        ##### 判断入参条件
        if(parameter_type['btn_longin']=='发送请求'):
            if(parameter_type['parameter']!='' and parameter_type['content_type']!=''):
                data_json = json.loads(request.POST['parameter'])
                headers = json.loads(request.POST['content_type'])
                response = requests.post(url=website, headers=headers, json=data_json)
                log.info(response.json())
                log.info(response.headers)
                if response.status_code != 200:
                    return render(request, 'error.html')
                else:
                    if response.json()['result'] != 200:
                        return HttpResponse(response)
                    else:
                        # 正则提取csrftoken和sessionid
                        temp = response.headers['Set-Cookie']
                        csrftoken = re.findall('csrftoken=(.*?); expires', temp)
                        csrftoken = csrftoken[0]
                        sessionid = re.findall('sessionid=(.*?); expires=', temp)
                        sessionid = sessionid[0]

                        # 写入cookie
                        userAuth = get_filePath("common/lora_cookie.txt")
                        with open(userAuth, 'w') as f:
                            f.write('csrftoken=' + csrftoken + ';sessionid=' + sessionid)
                        f.close()
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
                    resp = requests.post(url=website, data=data)
                    log.info(resp.request.body)
                    sleep(2)
                    count +=1
                    temp = '第'+str(count)+'条case响应结果：' + str(resp.json()) + ' '
                    resp_list.append(temp)
                log.info(HttpResponse(resp_list))
                return HttpResponse(resp_list)

            else:
                return HttpResponse("请上传文件后再提交！")

##### Lora 网关实时数据下载接口 #####
def lora_getrealTimeTemp(request):
    """
    TODO Lora 网关实时数据下载接口
    """
    # 判断前端请求类型
    if(request.method=='GET'):
        return render(request, 'lora_getRealTimeTemp.html')
    else:
        website = Url().lora_CHN_Host + Url().lora_CHN_relTimeTemp
        log.info('请求地址：' + website)
        parameter_type = request.POST
        log.info(parameter_type)

        ##### 判断入参条件
        if (parameter_type['device_mac'] != '' and parameter_type['days']):
            deviceId = json.loads(json.dumps(parameter_type['device_mac']))
            days = int(json.loads(json.dumps(parameter_type['days'])))
            headers = json.loads(request.POST['content_type'])

            # token使用判断
            if (parameter_type['token'] == ''):
                with open(get_filePath('common/lora_cookie.txt')) as f:
                    token = f.read()
                    f.close()
                headers['Cookie'] = token
            else:
                headers['Cookie'] =json.loads(json.dumps(request.POST['token']))
            seconds = days * 24 * 60 * 60
            nowStrfTime = int(timeToStamp(getNowStrfTime()))
            startTime = int(nowStrfTime - seconds)

            order_data = "/?device_mac=" + deviceId + "&start_time=" + str(startTime) + "&end_time=" + str(nowStrfTime)
            log.info('请求参数：' + str(order_data))
            response = requests.get(url=website + order_data, headers=headers)
            if response.status_code != 200:
                    return render(request, 'error.html')
            else:
                if response.json()['result'] != 200:
                    return HttpResponse(response)
                else:
                    resp_data = response.json()['data']
                    tempExcel = get_filePath('common/data/' + deviceId + '.xls')
                    log.info('正在生成excel数据，请稍后')

                    # 创建excel，xlsxwriter支持大文件写入（解决256行以上报错问题）
                    writebook = xlsxwriter.Workbook(tempExcel)
                    writesheet = writebook.add_worksheet(deviceId)

                    # 获取如参key name，删除不需要的key
                    # keys = list(parameter_type.keys())
                    # keys.remove('device_mac')
                    # keys.remove('days')
                    # keys.remove('token')
                    # keys.remove('content_type')
                    # keys.remove('btn_longin')

                    rowTitle = ['time', 'rssi', 'temp', 'humidity', 'co2', 'battery']
                    # 从A1单元格开始填充rowTitle的数据
                    writesheet.write_row('A1', rowTitle)
                    for i in range(0, len(rowTitle)):
                        writesheet.write(0, i, rowTitle[i])

                    # 写入Excel单元格
                    for col in range(0, len(resp_data)):
                        # 写入时间
                        utc8 = (int(resp_data[col]['time']) + 8 * 60 * 60)
                        writesheet.write(col + 1, 0, timeStampToStyleTime(utc8))
                        # 写入信号
                        writesheet.write(col + 1, 1, resp_data[col]['rssi'])
                        # 写入温度
                        writesheet.write(col + 1, 2, resp_data[col]['temperature'])
                        # 写入湿度
                        writesheet.write(col + 1, 3, resp_data[col]['humidity'])
                        # 写入co2
                        # writesheet.write(col + 1, 4, int(resp_data[col]['co2']))
                        # 写入Battery
                        writesheet.write(col + 1, 5, int(resp_data[col]['battery']))
                    writebook.close()
                    log.info('excel生成完毕，开始下载文件...')

                    with open(tempExcel, 'rb') as model_excel:
                        result = model_excel.read()
                    response = HttpResponse(result)
                    response['Content-Disposition'] = 'attachment; filename=' + deviceId + '.xlsx'
                    return response
        else:
            return HttpResponse("请求参数不可为空！")