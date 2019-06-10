from cmop.api.base import RestApi


class query_dev_desc(RestApi):
    def __init__(self,device_id):
        RestApi.__init__(self,
                         n_rest='/devices/%s' % device_id,
                         port=80,
                         method='GET')

        '''
        请求方式：GET

        URL: http(s)://api.heclouds.com/devices/_device_id_
        
        > device_id：需要替换为设备ID
        http头部
        参数名称 	    格式 	是否必须 	    说明
        api-key     string 	是 	        必须为masterkey或者具备该设备访问权限的apikey            

        '''

    def getapiname(self):
        return 'query_dev_desc'
