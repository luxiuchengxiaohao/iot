from cmop.api.base import RestApi


class update_dev_register_attr(RestApi):
    def __init__(self, register_code):
        RestApi.__init__(self,
                         n_rest='/register_attr',
                         port=80,
                         method='POST')
        self.allow_dup = None

        '''
        

        '''

    def getapiname(self):
        return 'register_dev'
