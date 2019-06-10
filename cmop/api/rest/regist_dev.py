from cmop.api.base import RestApi
class regist_dev(RestApi):
    def __init__(self,register_code):
        RestApi.__init__(self,
                         n_rest='/register_de',
                         port=80,
                         method='POST',
                         sys_parameters={'register_code':register_code})
        self.sn = None
        self.mac = None
        self.title = None
        '''
        [注册设备]
        请求方式：POST
        URL: http(s)://api.heclouds.com/register_de
        
        url参数
        参数名称 	        格式 	是否必须 	    说明
        register_code 	string 	是 	        注册码，产品下唯一
        
        http请求参数
        参数名称 	    格式 	是否必须 	    说明
        sn 	    string 	    与mac二选一 	用户自定义产品序列号，最大长度512
        mac 	string 	    与sn二选一 	用户自定义mac地址，最大长度32
        title 	string 	    否 	        设备名称，最大长度32，若为空，平台会默认分配设备名为“auto_register”
        '''
    def getapiname(self):
        return 'regist_dev'
