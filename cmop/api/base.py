# -*- coding: utf-8 -*-
'''
Created on 2018-12-17

@author: 陆秀成
'''

try:
    import httplib
except ImportError:
    import http.client as httplib
import urllib, urllib.parse
import json
import cmop

'''
定义一些系统变量
'''

SYSTEM_GENERATE_VERSION = "china-mobile-iot-sdk-python3-2018-12-17"




P_CODE = 'code'
P_SUB_CODE = 'sub_code'
P_MSG = 'msg'
P_SUB_MSG = 'sub_msg'
DOMAIN = 'api.heclouds.com'
MASTER_APIKEY = 'TfLkfaUN=E9zgDSHk3mr9R7h760='




def mixStr(pstr):
    if (isinstance(pstr, str)):
        return pstr
    else:
        return str(pstr)




class cmop_exception(Exception):
    # ===========================================================================
    # 业务异常类
    # ===========================================================================
    def __init__(self):
        self.errorcode = None
        self.message = None
        self.application_host = None
        self.service_host = None

    def __str__(self, *args, **kwargs):
        sb = "errorcode=" + mixStr(self.errorcode) + \
             " message=" + mixStr(self.message) + \
             " application_host=" + mixStr(self.application_host) + \
             " service_host=" + mixStr(self.service_host)
        return sb


class RequestException(Exception):
    # ===========================================================================
    # 请求连接异常类
    # ===========================================================================
    pass


class RestApi(object):
    # ===========================================================================
    # Rest api的基类
    # ===========================================================================

    def __init__(self,n_rest,port,method,sys_parameters=None,body=None):
        # =======================================================================
        # 初始化基类
        # Args @param domain: 请求的域名或者ip
        #      @param port: 请求的端口
        # =======================================================================
        self.__domain = DOMAIN
        self.__port = port
        self.__httpmethod = method
        self.__n_rest = n_rest
        self.__sys_parameters = sys_parameters
        self.__body = body

        if (cmop.getDefaultAppInfo()):
            self.__app_key = cmop.getDefaultAppInfo().appkey

    def get_request_header(self):
        return {
            'Content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            "Cache-Control": "no-cache",
            "Connection": "Keep-Alive",
            'api-key': self.__app_key,
        }

    # 目前不用
    # def set_app_info(self, appinfo):
    #     # =======================================================================
    #     # 设置请求的app信息
    #     # @param appinfo: import cmop
    #     #                 appinfo cmop.appinfo(appkey,secret)
    #     # =======================================================================
    #     self.__app_key = appinfo.appkey
    #     self.__secret = appinfo.secret

    def getapiname(self):
        return ""


    def getTranslateParas(self):
        return {}

    def _check_requst(self):
        pass

    def getResponse(self, timeout=30):
        # =======================================================================
        # 获取response结果
        # =======================================================================
        connection = httplib.HTTPConnection(host=self.__domain, port=self.__port, timeout=timeout)
        connection.connect()

        header = self.get_request_header()
        if self.__body:
            body = self.__body
        else:
            application_parameter = self.getApplicationParameters()
            # body = urllib.parse.urlencode(application_parameter)
            body = json.dumps(application_parameter)
        # print(self.__sys_parameters)
        if self.__sys_parameters:
            url = self.__n_rest + "?" + urllib.parse.urlencode(self.__sys_parameters)
        else:
            url = self.__n_rest
        # print(url)
        # print(header)
        # print(body)
        connection.request(self.__httpmethod, url, body=body, headers=header)
        response = connection.getresponse()
        if response.status is not 200:
            raise RequestException('invalid http status ' + str(response.status) + ',detail body:' + response.read())
        result = response.read().decode('utf-8')
        # print(result)
        jsonobj = json.loads(result)
        # if "errno" in jsonobj and jsonobj['errno'] != 0:
        #     error = cmop_exception()
        #     error.errorcode = jsonobj["errno"]
        #     error.message = jsonobj["error"]
        #     error.application_host = response.getheader("Application-Host", "")
        #     error.service_host = response.getheader("Location-Host", "")
        #     raise error
        return jsonobj

    def getApplicationParameters(self):
        application_parameter = {}
        for key, value in self.__dict__.items():
            if not key.startswith("__") and not key.startswith(
                    "_RestApi__") and value is not None:
                if (key.startswith("_")):
                    application_parameter[key[1:]] = value
                else:
                    application_parameter[key] = value
        # 查询翻译字典来规避一些关键字属性
        translate_parameter = self.getTranslateParas()
        for key, value in application_parameter.items():
            if key in translate_parameter:
                application_parameter[translate_parameter[key]] = application_parameter[key]
                del application_parameter[key]
        return application_parameter
