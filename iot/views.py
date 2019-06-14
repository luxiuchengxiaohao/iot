from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from django.utils import timezone
from iot.form import *
from iot.models import *
import json,hashlib,time,urllib.request,urllib.parse,os,random
from random import Random
from iot.products import starry_sky_box,switch

def alibaba_aliqin_fc_sms_num_send(code_arg,rec_num_arg):
    while True:
        appsecret = 暂时去掉
        # 以下参数名称已按ASCII码表顺序排序
        parame = {'app_key': "24567764",
                  'format': "json",
                  'method': "alibaba.aliqin.fc.sms.num.send",
                  'sms_type': 'normal',
                  'sms_free_sign_name': 暂时去掉,
                  'rec_num': rec_num_arg,
                  'sms_param': '{"code":"' + code_arg + '","product":"星空物联"}',
                  'sms_template_code': 'SMS_48975023',
                  'sign_method': "md5",
                  'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                  'v': "2.0"}
        # 按照a-z字符顺序排列并拼接字符串
        sign = ''
        for k in sorted(parame.keys()):
            sign += k + parame[k]
        m = hashlib.md5()
        m.update((appsecret + sign + appsecret).encode('utf-8'))
        parame['sign'] = m.hexdigest().upper()
        apiurl = 暂时去掉
        data = urllib.parse.urlencode(parame).encode('utf-8')
        req = urllib.request.Request(apiurl, data)
        try:
            response = urllib.request.urlopen(req)
            response = response.read().decode('utf-8')
            if os.path.exists('/var/www/iot'):
                with open("/var/www/untitled1/sms.log",'a',encoding='utf-8') as f:
                    f.write(time.strftime('%Y-%m-%d %H:%M:%S:') + '手机号：'+ rec_num_arg + '---' + str(response) +'\n')
            print(rec_num_arg + response)
            return response
        except Exception as ErrMsg:
            if os.path.exists('/var/www/iot'):
                with open("/var/www/untitled1/sms.log",'a',encoding='utf-8') as f:
                    f.write(time.strftime('%Y-%m-%d %H:%M:%S:') + '手机号：'+ rec_num_arg + '---' + str(ErrMsg) +'\n')
            break
def verify_code():
    random = Random()
    code = ''
    for i in range(6):
        code += str(random.randint(0,9))
    return code
def view_verifycode(request):
    if request.method == 'POST':
        form = verifycode_form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['n']
            if len(request.session.get('verify_code', [])) > 3:
                request.session.set_expiry(86400)
                return HttpResponse(json.dumps({'status':4,'message': ['获取验证码频繁，请24小时后再来注册。']}),content_type="application/json")
            code = verify_code()
            if len(request.session.get('verify_code', [])) > 0:
                request.session['verify_code'].append(code)
            else:
                request.session['verify_code'] = [code]
            request.session['username'] = username
            response = alibaba_aliqin_fc_sms_num_send(code, username)
            if response.find('isv.BUSINESS_LIMIT_CONTROL') != -1:
                return HttpResponse(json.dumps({'status': 5,'message':['您今日接收验证码频繁，已被运营商限制，24小时后再试']}),content_type="application/json")
            else:
                return HttpResponse(json.dumps({'status': 0 ,'message':['验证码已发送，请注意查收。']}),content_type="application/json")
        else:
            error_list = re.findall('<li>.*?<ul class="errorlist"><li>(.*?)</li></ul>', str(form.errors))
            return HttpResponse(json.dumps({'status':2,'message':error_list}),content_type="application/json")

    else:
        return HttpResponse(json.dumps({'status': 1,'message':['method error!']}),content_type="application/json")
def view_login(request):
    if request.method == 'POST':
        form = loginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_list = user.objects.filter(username=username)
            if len(user_list) == 1:
                user_object = user_list[0]
            elif len(user_list) > 1:
                return HttpResponse(json.dumps({'status': 6, 'message': ['该账号异常，请联系管理员!']}),content_type="application/json")
            else:
                return HttpResponse(json.dumps({'status': 2, 'message': ['手机号未注册!']}),content_type="application/json")
            if check_password(password, user_object.password):
                user_object.login_numbers += 1
                user_object.last_login_datetime = timezone.now()
                user_object.save()
                request.session['IS_LOGIN'] = True
                request.session['USRNAME'] = username
                request.session.set_expiry(1800)
                return HttpResponse(json.dumps({'status':0,'message':['登陆成功。']}),content_type="application/json")
            else:
                return HttpResponse(json.dumps({'status':3,'message':['手机号或密码不正确!']}),content_type="application/json")

        else:
            error_list = re.findall(r'<li>.*?<ul class="errorlist"><li>(.*?)</li></ul>', str(form.errors))
            return HttpResponse(json.dumps({'status': 1, 'message': error_list}),content_type="application/json")
    else:
        return render(request,'login.html')
def view_regist(request):
    if request.method == 'POST':
        if not request.POST['verify_code'] or not request.session.get('verify_code', []) or request.POST['verify_code'] not in request.session.get('verify_code',[]):
            return HttpResponse(json.dumps({'status':3,'message':['验证码不正确，请重新输入!']}),content_type="application/json")
        elif not request.session.get('username','') or request.session.get('username','') != request.POST['username']:
            return HttpResponse(json.dumps({'status': 4, 'message': ['手机号与验证码不匹配，请重新输入!']}),content_type="application/json")
        request.session.clear()
        form = registerForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            type = form.cleaned_data['type']
            user_list = user.objects.filter(username=username)
            if len(user_list) == 1:
                if type == 0:
                    return HttpResponse(json.dumps({'status': 5, 'message': ['该手机号已注册，请直接登陆，或更换手机号注册。']}),content_type="application/json")
                elif type == 1:
                    user_list[0].password = make_password(password)
                    user_list[0].save()
                    return HttpResponse(json.dumps({'status': 0, 'message': ['密码重置成功。']}),content_type="application/json")
                else:
                    return HttpResponse(json.dumps({'status': 7, 'message': ['请求类型异常！']}),content_type="application/json")
            elif len(user_list) > 1:
                return HttpResponse(json.dumps({'status': 6, 'message': ['该账号异常，请联系管理员。']}),content_type="application/json")

            else:
                if type == 1:
                    return HttpResponse(json.dumps({'status': 8, 'message': ['该手机号未注册!。']}),content_type="application/json")
                elif type ==0:
                    while True:
                        api_key = ''.join(random.choice('0123456789') for i in range(8))
                        if len(user.objects.filter(api_key=api_key)) == 0:
                            break
                    while True:
                        api_secret = ''.join(random.choice('0123456789abcdef') for i in range(32))
                        if len(user.objects.filter(api_secret=api_secret)) == 0:
                            break
                    user.objects.create(username=username,
                                                    password=make_password(password),
                                                    login_numbers=0,
                                                    regist_datetime=timezone.now(),
                                                    last_login_datetime=timezone.now(),
                                                    api_key=api_key,
                                                    api_secret = api_secret
                                                    )

                    return HttpResponse(json.dumps({'status': 0, 'message': ['注册成功。']}),content_type="application/json")
                else:
                    return HttpResponse(json.dumps({'status': 7, 'message': ['请求类型异常！']}),content_type="application/json")
        else:
            error_list = re.findall('<li>.*?<ul class="errorlist"><li>(.*?)</li></ul>', str(form.errors))
            return HttpResponse(json.dumps({'status': 2, 'message': error_list}),content_type="application/json")
    else:
        return HttpResponse(json.dumps({'status': 1, 'message': ['method error!']}),content_type="application/json")

def view_user(request):
    if request.session.get('IS_LOGIN', False):
        if request.method == 'GET':
            username = request.session.get('USRNAME', False)
            user_list = user.objects.filter(username=username)
            if len(user_list) == 1:
                request.session.set_expiry(1800)
                return render(request, 'user.html', {'username': username})
            elif len(user_list) > 1:
                return HttpResponse(json.dumps({'status': 6, 'message': ['该账号异常，请联系管理员。']}),content_type="application/json")
            else:
                return redirect('/login/')
        else:
            return HttpResponse(json.dumps({'status': 1, 'message': ['method error!']}),content_type="application/json")
    else:
        return redirect('/login/')
def view_devices_info(request):
    if request.session.get('IS_LOGIN', False) and request.session.get('USRNAME', False):
        if request.method == 'POST':
            username = request.session.get('USRNAME', False)
            user_list = user.objects.filter(username=username)
            if len(user_list) == 1:
                request.session.set_expiry(1800)
                device_list = devices.objects.filter(bind_user=username)
                data = []
                for device in device_list:
                    data.append([device.device_id,device.device_name,device.group,device.device_type])
                return HttpResponse(json.dumps({'status': 0, 'message': ['设备信息获取成功。'],'data':data}),content_type="application/json")
            elif len(user_list) > 1:
                return HttpResponse(json.dumps({'status': 6, 'message': ['该账号异常，请联系管理员。']}),content_type="application/json")
            else:
                return redirect('/login/')
        else:
            return HttpResponse(json.dumps({'status': 1, 'message': ['method error!']}),content_type="application/json")
    else:
        return redirect('/login/')
def view_logout(request):
    #request.session.clear()
    sessionKey = request.session.session_key
    if request.session.exists(sessionKey):
        request.session.delete(sessionKey)
        #删除所有过期session
        request.session.clear_expired()
    return redirect('/login/')
def view_starry_sky_box_api(request):
    if request.session.get('IS_LOGIN', False) and request.session.get('USRNAME', False):
        if request.method == 'POST':
            username = request.session.get('USRNAME', False)
            user_list = user.objects.filter(username=username)
            if len(user_list) == 1:
                request.session.set_expiry(1800)
                # param_dict = request.POST.pop['sign']
                # param = '&'.join('%s=%s' % (k, param_dict[k]) for k in sorted(param_dict))
                # privkey_object = OpenSSL.crypto.load_publickey(OpenSSL.crypto.FILETYPE_PEM, open('public.pem').read())
                # res = OpenSSL.crypto.verify(privkey_object, base64.b64decode(request.POST['sign']), param, 'sha1')
                # if res:
                # else:
                #     return HttpResponse(json.dumps({'status': 2, 'message': ['sign error!']}),content_type="application/json")
                if request.POST['api_name']:
                    api_name = request.POST['api_name']
                    ssb = starry_sky_box(暂时去掉敏感信息, 暂时去掉敏感信息)
                    if api_name == 'regist_dev':
                        devices_filter = devices.objects.filter(sn_code=str(request.POST['sn']))
                        if len(devices_filter) == 0:
                            res = ssb.add_dev(title='星空宝盒',
                                              auth_info=request.POST['sn'])
                            if res['status'] == 0:
                                if res['data']['errno'] == 0 or res['data']['errno'] == 6:
                                    if res['data']['errno'] == 6:
                                        res = ssb.regist_dev(str(request.POST['sn']))
                                        if res['status'] != 0:
                                            return HttpResponse(json.dumps(res))
                                    devices.objects.create(
                                                            device_type=1,
                                                           device_id=res['data']['data']['device_id'],
                                                           device_name='星空宝盒',
                                                           sn_code=request.POST['sn'],
                                                           key='',
                                                           bind_user=username,
                                                            group=0,
                                                           add_datetime=timezone.now(),
                                                           last_register_datetime=timezone.now(),
                                                           register_count=1,
                                                           )
                                    return HttpResponse(json.dumps({'status': 0, 'message': ['设备首次注册成功。']}),content_type="application/json")
                                else:
                                    return HttpResponse(json.dumps({'status': 11, 'message': ['添加设备未知异常！']}),content_type="application/json")
                            else:
                                return HttpResponse(json.dumps(res))
                        elif len(devices_filter) == 1:
                            devices_filter[0].bind_user=username
                            devices_filter[0].group = 0
                            devices_filter[0].last_register_datetime = timezone.now()
                            devices_filter[0].register_count += 1
                            devices_filter[0].save()
                            return HttpResponse(json.dumps({'status': 0, 'message': ['设备注册成功。']}),content_type="application/json")
                        elif len(devices_filter) > 1:
                            return HttpResponse(json.dumps({'status': 7, 'message': ['该设备异常，请联系技术人员解决。']}),content_type="application/json")

                    elif api_name == 'send_cmd':
                        devices_filter = devices.objects.filter(device_id=str(request.POST['device_id']),bind_user=username)
                        if len(devices_filter) == 0:
                            return HttpResponse(json.dumps({'status': 8, 'message': ['设备信息错误。']}),content_type="application/json")
                        elif len(devices_filter) == 1:
                            btn_num = int(request.POST['btn_num'])
                            if  btn_num == 1:cmd = '[1](0.5)'
                            elif btn_num == 2:cmd = '[1](0.5)'
                            elif btn_num == 3:cmd = '[1](0.5)'
                            elif btn_num == 4: cmd = '[1](0.5)'
                            elif btn_num == 5: cmd = '[1](0.5)'
                            elif btn_num == 6: cmd = '[1](0.5)'
                            elif btn_num == 7: cmd = '[1](0.5)'
                            elif btn_num == 8: cmd = '[1](0.5)'
                            else:
                                return HttpResponse(json.dumps({'status': 9, 'message': ['按键信息错误！。']}),content_type="application/json")
                            res = ssb.send_cmd(request.POST['device_id'],cmd)
                            if res['status'] == 0:
                                if res['data']['errno'] == 0:
                                    return HttpResponse(json.dumps({'status': 0, 'message': ['命令发送成功。']}),content_type="application/json")
                                elif res['data']['errno'] == 10:
                                    return HttpResponse(json.dumps({'status': 10, 'message': ['设备不在线。']}),content_type="application/json")
                                else:
                                    return HttpResponse(json.dumps({'status': 11, 'message': ['设备未知异常！']}),content_type="application/json")
                            else:
                                return HttpResponse(json.dumps(res))
                        elif len(devices_filter) > 1:
                            return HttpResponse(json.dumps({'status': 7, 'message': ['该设备控制异常，请联系技术人员解决。']}),content_type="application/json")
                    elif api_name == 'batch_query_dev_status':
                        dil = json.loads(request.POST['dev_id_list'])
                        res = ssb.batch_query_dev_status(','.join(str(id) for id in dil))
                        if res['status'] == 0:
                            if res['data']['errno'] == 0:
                                return HttpResponse(json.dumps({'status': 0, 'message': ['批量查询设备状态成功。'],'data':res['data']['data']['devices']}),content_type="application/json")
                            elif res['data']['errno'] == 3:
                                return HttpResponse(json.dumps({'status': 12, 'message': ['批量查询设备状态失败！设备ID错误!']}),content_type="application/json")
                            else:
                                return HttpResponse(json.dumps({'status': 11, 'message': ['设备未知异常！']}),content_type="application/json")
                        else:
                            return HttpResponse(json.dumps(res))
                    else:
                        return HttpResponse(json.dumps({'status': 4, 'message': ['api error!']}),content_type="application/json")
                else:
                    return HttpResponse(json.dumps({'status': 3, 'message': ['Parameter error!']}),content_type="application/json")

            elif len(user_list) > 1:
                return HttpResponse(json.dumps({'status': 6, 'message': ['该账号异常，请联系管理员。']}),content_type="application/json")
            else:
                return redirect('/login/')
        else:
            return HttpResponse(json.dumps({'status': 1, 'message': ['method error!']}),content_type="application/json")
    else:
        return redirect('/login/')
def view_switch_device_api(request):
    if request.method == 'GET':
        if request.GET.get('sn'):
            sn_code = request.GET.get('sn')
            devices_filter = devices.objects.filter(sn_code=str(sn_code))
            if len(devices_filter) == 1:
                if not devices_filter[0].key:
                    s = switch(暂时去掉敏感信息, 暂时去掉敏感信息)
                    res = s.regist_dev(sn_code)
                    if res['status'] == 0:
                        devices_filter[0].key = res['data']['data']['key']
                        devices_filter[0].save()
                        return HttpResponse(json.dumps({'status': 0,
                                                    'message': ['设备注册成功。'],
                                                    'data':{'device_id':res['data']['data']['device_id'],
                                                            'key':res['data']['data']['key']}
                                                    }),content_type="application/json")
                    else:
                        return HttpResponse(json.dumps({'status': 11, 'message': ['注册设备未知异常！']}),content_type="application/json")
                else:
                    return HttpResponse(json.dumps({'status': 0,
                                                    'message': ['设备信息获取成功。'],
                                                    'data': {'device_id': devices_filter[0].device_id,
                                                             'key': devices_filter[0].key}
                                                    }),content_type="application/json")
            elif len(devices_filter) == 0:
                # s = switch('3yf8gBZPvN=UMFvHAIyQxM6mIVk=', '0G5WG6hSd9nS6xsd')
                # res = s.add_dev(title='智能开关', auth_info=sn_code)
                # # print(res)
                # if res['status'] == 0:
                #     devices.objects.create(
                #         device_type=2,
                #         device_id=res['data']['data']['device_id'],
                #         device_name='智能开关',
                #         sn_code=sn_code,
                #         key='',
                #         bind_user='',
                #         group=0,
                #         add_datetime=timezone.now(),
                #         last_register_datetime=timezone.now(),
                #         register_count=0,
                #     )
                return HttpResponse(json.dumps({'status': 2, 'message': ['该这设备不存在。']}),content_type="application/json")
            elif len(devices_filter) > 1:
                return HttpResponse(json.dumps({'status': 7, 'message': ['该设备异常，请联系技术人员解决。']}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({'status': 3, 'message': ['Parameter error!']}),content_type="application/json")
    else:
        return HttpResponse(json.dumps({'status': 1, 'message': ['method error!']}),content_type="application/json")
