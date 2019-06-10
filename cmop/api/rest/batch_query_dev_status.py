from cmop.api.base import RestApi


class batch_query_dev_status(RestApi):
    def __init__(self,devIds):
        RestApi.__init__(self,
                         n_rest='/devices/status',
                         port= 80,
                         method='GET',
                         sys_parameters={'devIds':devIds})

        '''
        批量查询设备状态

        请求方式：GET
        
        URL: http(s):api.heclouds.com/devices/status
        URL请求参数
        参数名称 	    格式 	是否必须 	说明
        devIds 	    string 	否 	    指定设备ID，多个用逗号分隔，最多1000个
        http头部
        参数名称 	    格式 	是否必须 	说明
        api-key 	string 	是 	    必须为masterkey
        '''

    def getapiname(self):
        return 'batch_query_dev_status'
