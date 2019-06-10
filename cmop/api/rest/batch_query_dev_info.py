from cmop.api.base import RestApi


class batch_query_dev_info(RestApi):
    def __init__(self,**kwargs):
        RestApi.__init__(self,
                         n_rest='/devices',
                         port= 80,
                         method='GET')
        if kwargs:
            self.__sys_parameters = kwargs

        '''
        批量查询设备信息
        请求方式：GET

        URL: http(s)://api.heclouds.com/devices
        URL参数
        参数名称    	格式 	        是否必须 	    说明
        key_words 	string 	        否 	        匹配关键字，从id和title字段中左匹配
        auth_info 	string 	        否 	        鉴权信息
        tag 	    array-string 	否 	        设备标签
        online 	    bool 	        否 	        设备在线状态
        private 	bool 	        否 	        设备私密性
        page 	    int 	        否 	        指定页码，最大页数为10000
        per_page 	int 	        否 	        指定每页输出设备个数，默认30，最多100
        device_id 	string 	        否 	        指定设备ID，多个用逗号分隔，最多100个
        begin 	    string 	        否 	        起始时间，北京时间，示例：2016-06-20
        end 	    string 	        否 	        结束时间，北京时间，示例：2016-06-20
        http头部
        参数名称 	格式 	是否必须 	说明
        api-key 	string 	是 	必须为masterkey            

        '''

    def getapiname(self):
        return 'batch_query_dev_info'
