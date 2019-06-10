


class appinfo(object):
    def __init__(self, appkey):
        self.appkey = appkey
        # self.secret = secret


def getDefaultAppInfo():
    pass


def setDefaultAppInfo(appkey):
    default = appinfo(appkey)
    global getDefaultAppInfo
    getDefaultAppInfo = lambda: default