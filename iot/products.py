import cmop.api,time
from cmop.api.base import RequestException,cmop_exception
class starry_sky_box:
    def __init__(self,api_key,register_code):
        cmop.setDefaultAppInfo(api_key)
        self.__register_code = register_code
    def send_request(self,req):
        http_err = 0
        while True:
            try:
                response = req.getResponse()
                return {'status':0,'message':'请求发送成功。','data':response}
            except RequestException:
                print('http请求异常!')
                if http_err <= 3:
                    http_err += 1
                    time.sleep(300)
                else:
                    return {'status': 1, 'message': '请求未知异常!'}
            except Exception as e:
                print('命令发送未知异常：%s。' % str(e))
                return {'status':3,'message':str(e)}
    def add_dev(self,title,desc=None,tags=None,location=None,private=None,auth_info=None,other=None):
        req = cmop.api.add_dev()
        req.title = title
        req.desc = desc
        req.tags = tags
        req.location = location
        req.private = private
        req.auth_info = auth_info
        req.other = other
        return self.send_request(req)
    def regist_dev(self,sn,title=None):
        req = cmop.api.regist_dev(self.__register_code)
        req.sn= sn
        req.title = title
        return self.send_request(req)
    def send_cmd(self,device_id,cmd):
        req = cmop.api.send_cmd(device_id,cmd)
        return self.send_request(req)

    def query_dev_desc(self,device_id):
        req = cmop.api.query_dev_desc(device_id)
        return self.send_request(req)
    def batch_query_dev_status(self,devIds):
        req = cmop.api.batch_query_dev_status(devIds)
        return self.send_request(req)
class switch:
    def __init__(self,api_key,register_code):
        cmop.setDefaultAppInfo(api_key)
        self.__register_code = register_code
    def send_request(self,req):
        http_err = 0
        while True:
            try:
                response = req.getResponse()
                return {'status':0,'message':'请求发送成功。','data':response}
            except RequestException:
                print('http请求异常!')
                if http_err <= 3:
                    http_err += 1
                    time.sleep(300)
                else:
                    return {'status': 1, 'message': '请求未知异常!'}
            except Exception as e:
                print('命令发送未知异常：%s。' % str(e))
                return {'status':3,'message':str(e)}
    def add_dev(self,title,desc=None,tags=None,location=None,private=None,auth_info=None,other=None):
        req = cmop.api.add_dev()
        req.title = title
        req.desc = desc
        req.tags = tags
        req.location = location
        req.private = private
        req.auth_info = auth_info
        req.other = other
        return self.send_request(req)
    def regist_dev(self,sn,title=None):
        req = cmop.api.regist_dev(self.__register_code)
        req.sn= sn
        req.title = title
        return self.send_request(req)
if __name__ == '__main__':
    ssb = starry_sky_box('TfLkfaUN=E9zgDSHk3mr9R7h760=', 'ZlyJ1u5JuGmukdXi')
    # print(ssb.add_dev(title='星空宝盒',
    #                   desc='星空宝盒详情',
    #                   tags=['ssb'],
    #                   private=True,
    #                   auth_info='123456798'))
    # print(ssb.regist_dev(sn='123456798',title='星空宝盒2'))
    # {'message': '注册成功。', 'status': 0, 'data': {'data': {'device_id': '509150838', 'key': 'varQ8nE=xR1GyIf60VcaOX=ZtjQ='}, 'error': 'succ', 'errno': 0}}
    # print(ssb.send_cmd('512395415', '[1](0),[2](0),[3](0),[4](0),[5](0),[6](0),[7](0),[8](0)'))
    # time.sleep(30)
    # print(ssb.send_cmd('512395415', '[1](-1),[2](-1),[3](-1),[4](-1),[5](-1),[6](-1),[7](-1),[8](-1)'))
