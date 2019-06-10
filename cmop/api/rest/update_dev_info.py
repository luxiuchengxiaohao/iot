from cmop.api.base import RestApi
class update_dev_info(RestApi):
    def __init__(self,device_id):
        RestApi.__init__(self,
                         n_rest='/devices/%s' % device_id,
                         port=80,
                         method='PUT')

        self.title = None
        self.desc = None
        self.tags = None
        self.location = None
        self.private = None
        self.auth_info= None
        self.other = None
        '''
        [更新设备信息]
        请求方式：PUT

        URL: http(s)://api.heclouds.com/devices/_device_id_
        
        > device_id：需要替换为设备ID
        
        http头部
        参数名称 	    格式 	是否必须 	    说明
        api-key 	string 	是 	        必须为masterkey或者具备该设备访问权限的apikey
        
        http请求参数
        参数名称 	    格式 	        是否必须 	    说明
        title 	    string 	        否 	        设备名称
        desc 	    string 	        否 	        设备描述
        tags 	    array-string 	否 	        设标签，可为一个或者多个，见示例
        location 	json 	        否 	        设备位置坐标信息，以经纬度键值对表示:{"lon":xx,"lat":xx}
        private 	bool 	        否 	        设备私密性，决定应用编辑器分享链接中设备信息的可见度，默认为true
        auth_info 	string 	        否 	        鉴权信息，建议携带，并设置为设备的产品序列号
        other 	    json 	        否 	        其他设备自定义信息，以键值对格式表示，见示例
        '''
    def getapiname(self):
        return 'update_dev_info'