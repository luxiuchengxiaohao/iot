import time
from django.utils.deprecation import MiddlewareMixin
MAX_REQUEST_PER_SECOND=10 #每秒访问次数
class RequestBlockingMiddleware(MiddlewareMixin):
    def process_request(self,request):
        now=time.time()
        queue_count = len(request.session.get('request_queue',[]))
        if queue_count < MAX_REQUEST_PER_SECOND:
            if queue_count == 0:
                request.session['request_queue'] = []
            request.session['request_queue'].append(now)
        else:
            if (now-request.session['request_queue'][0])<1:
                time.sleep(5)
            if request.path != '/logout':
                del request.session['request_queue'][0]
                request.session['request_queue'].append(time.time())
