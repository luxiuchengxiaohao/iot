from cmop.api.base import RestApi


class send_cmd(RestApi):
    def __init__(self,device_id,cmd,qos=0,timeout=0):
        RestApi.__init__(self,
                         n_rest='/cmds',
                         port=80,
                         method='POST',
                         sys_parameters={'device_id':device_id,'qos':qos,'timeout':timeout},
                         body=cmd)
        '''
        [发送命令]
        请求方式：POST

        URL:http(s)://api.heclouds.com/cmds
        URL参数
        参数名称 	    格式 	是否必须 	说明
        device_id 	string 	是 	    接收该数据的设备ID
        qos 	    int 	否 	    是否需要设备应答，默认为0。
                                    0：最多发送一次，不关心设备是否响应
                                    1：至少发送一次，如果设备收到命令后没有应答，则会在下一次设备登陆时若命令在有效期内（有效期定义参见timeout参数）则会重发该命令
        timeout 	int 	否 	    命令有效时间，默认0。
                                    0：在线命令，若设备在线,下发给设备，若设备离线，直接丢弃
                                    >0： 离线命令，若设备在线，下发给设备，若设备离线，在当前时间加timeout时间内为有效期，有效期内，若设备上线，则下发给设备
                                    单位：秒
                                    有效范围：0~2678400
        HTTP头部
        参数名称 	    格式 	是否必须 	说明
        api-key 	string 	是 	    必须为masterkey或者具备该设备访问权限的apikey
        http请求内容
        > 用户自定义数据：json、string、二进制数据（小于64K）
        '''

    def getapiname(self):
        return 'send_cmd'