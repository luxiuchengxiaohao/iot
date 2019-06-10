import pyb,json,time,re,ubinascii,machine
MCU_ID = ubinascii.hexlify(machine.unique_id()).decode('utf-8','ignore')
VERSION = '1.0.0'
u4 = pyb.UART(4,115200)
u4.init(115200,bits=8,parity=None,stop=1)
relay_1 = pyb.Pin('X5',pyb.Pin.OUT_PP)
relay_2 = pyb.Pin('X6',pyb.Pin.OUT_PP)
relay_3 = pyb.Pin('X7',pyb.Pin.OUT_PP)
relay_4 = pyb.Pin('X8',pyb.Pin.OUT_PP)
relay_5 = pyb.Pin('Y11',pyb.Pin.OUT_PP)
relay_6 = pyb.Pin('Y12',pyb.Pin.OUT_PP)
relay_7 = pyb.Pin('X17',pyb.Pin.OUT_PP)
relay_8 = pyb.Pin('X18',pyb.Pin.OUT_PP)
led_red = pyb.LED(1)
led_green = pyb.LED(2)
led_yellow = pyb.LED(3)
led_blue = pyb.LED(4)
led_red.on()
led_green.on()
led_yellow.on()
led_blue.on()
time.sleep(1)
led_red.off()
led_green.off()
led_yellow.off()
led_blue.off()

def log(text):
    print_text = '[%s]:%s\r\n' % (int(pyb.millis()/1000),text.replace('\r\n',' ').replace('\r',' '))
    print(print_text)
    # if MCU_ID == '2c0033001451363130373931':
    #     try:
    #         with open('/sd/log.txt','a') as f:
    #             f.write(print_text)
    #     except Exception as e:
    #         print(repr(e))
def write(text):
    log('WRITE->%s' % text)
    u4.write(text)
def control_relay(relay,second):
    if second == 0:
        relay.high()
    elif second == -1:
        relay.low()
    else:
        relay.high()
        time.sleep(second)
        relay.low()
    u4.read()
def connect_gprs():
    led_blue.off()
    while True:
        log(ok())
        log(send_cmd('AT+CIPCLOSE\r\n'))   #主动关闭TCP连接
        log(send_cmd('AT+CIPSHUT\r\n'))    #关闭移动场景
        time.sleep(0.5)
        while True:
            ret = send_cmd('AT+CREG?\r\n')
            log(ret)
            if ret.find('+CREG: 0,1') == -1:
                log('gsm模块网络未注册,等待...')
                time.sleep(1)
            else:
                break
        while True:
            ret = send_cmd('AT+CGATT?\r\n')   #检查 GPRS 附着状态
            log(ret)
            if ret.find('+CGATT: 1') != -1:
                log('网络已附着。')
                break
            else:
                log('gsm模块网络未附着,等待...')
                time.sleep(1)
        log(send_cmd('AT+CIPMODE=1\r\n'))  #设置链路模式为透传模式
        log(send_cmd('AT+CSTT="CMNET"\r\n')) #设置 APN
        log(send_cmd('AT+CIICR\r\n'))  #建立无线链路
        log(send_cmd('AT+CIFSR\r\n'))  #获取本机IP地址
        

        if connect_server():
            led_blue.on()
            for i in range(3):
              write('*185207#%s#sample*' % MCU_ID)
              time.sleep(0.5)
            break
        
def connect_server():
    write('AT+CIPSTART="TCP","183.230.40.40","1811"\r\n')
    for i in range(60):
        time.sleep(0.1)
        if u4.any() > 0:
            ret_byte = u4.read()
            try:
              ret = ret_byte.decode('utf-8','ignore')
            except Exception as e:
              log(repr(e))
              print(ret_byte)
              ret = ''
            log(ret)
            if ret.find('CLOSED') != -1 or ret.find('FAIL') != -1:
                return False
            elif ret.find('CONNECT') != -1 or ret.find('ALREADY') != -1:
                return True
                
    return False
def restart():
    while True:
        log(send_cmd('AT+CFUN=1,1\r\n'))
        for i in range(10):
            ret = send_cmd('AT+CGATT?\r\n')   #检查 GPRS 附着状态
            log(ret)
            if ret.find('+CGATT: 1') == -1:
                log('gsm模块网络未附着,等待...')
                time.sleep(3)
            else:
                return True
        log('等待30秒网络附着失败，再次重启射频!!')
def send_cmd(cmd):
    while True:
        write(cmd)
        for i in range(30):
            if u4.any() > 0:
                ret_byte = u4.read()
                try:
                    return ret_byte.decode('utf-8','ignore')
                except Exception as e:
                    log(repr(e))
                    print(ret_byte)
                    return ''
            time.sleep(0.1)
        log('命令[%s]3秒无响应，重试！' % cmd)
        # else:
        #     log(u4.read())

def send_cmd_wait(cmd,res):
    while True:
          write(cmd)
          for i in range(30):
              if u4.any() > 0:
                    ret_byte = u4.read()
                    try:
                        ret = ret_byte.decode('utf-8','ignore')
                        if ret.find(res) != -1:
                            return(ret)
                        else:
                          break
                    except Exception as e:
                        log(repr(e))
                        print(ret_byte)
              time.sleep(0.1)
          log('等待命令[%s]3秒无响应，重试！' % cmd)
def ok():
    while True:
        write('+++')
        for i in range(30):
            if u4.any() > 0:
                ret_byte = u4.read()
                try:
                    ret = ret_byte.decode('utf-8','ignore')
                    if ret.find('OK') != -1:
                        return '+++->' + ret
                except Exception as e:
                    log(repr(e))
                    print(ret_byte)
            time.sleep(0.1)
        write('AT\r\n')
        for i in range(30):
            if u4.any() > 0:
                ret_byte = u4.read()
                try:
                    ret = ret_byte.decode('utf-8','ignore')
                    if ret.find('OK') != -1:
                        return 'AT->' + ret
                except Exception as e:
                    log(repr(e))
                    print(ret_byte)
            time.sleep(0.1)
def main():
    log(ok())
    log(send_cmd('ATE0\r\n'))
    log(send_cmd_wait('AT\r\n','OK'))
    log(send_cmd_wait('AT+CSQ\r\n','OK'))
    log(send_cmd_wait('AT+CPIN?\r\n','OK'))
    connect_gprs()
    keep_alive_data = '!'
    heart_beat = time.time()
    while True:
        time.sleep(0.1)
        if time.time() - heart_beat > 180:
            log('3分钟未收到心跳，重新连接服务器！')
            connect_gprs()
            heart_beat = time.time()
        if u4.any() > 0:
            ret_byte = u4.read()
            led_green.on()
            time.sleep(0.2)
            led_green.off()
            if ret_byte:
                try:
                    ret = ret_byte.decode('utf-8','ignore')
                    log('READ->->%s' %  ret)
                    if ret.find('?') != -1:
                        heart_beat = time.time()
                        write(keep_alive_data)
                    elif ret.find('CLOSED') != -1:
                        log('与服务器断开连接，重新连接服务器！')
                        connect_gprs()
                        heart_beat = time.time()
                    elif ret.find('+CGATT: 0') != -1:
                        log('网络剥离，重启射频!')
                        restart()
                        connect_gprs()
                        heart_beat = time.time()
                    for cmd in ret.split(','):
                        result = re.search('\[(\d+)\]\((-?\d+\.?\d*)\)',cmd)
                        if result:
                            relay_num = int(result.group(1))
                            delay_time = float(result.group(2))
                            if 0 < relay_num <= 8 and delay_time <= 10:
                                if relay_num == 1: control_relay(relay_1,delay_time)
                                elif relay_num == 2: control_relay(relay_2,delay_time)
                                elif relay_num == 3: control_relay(relay_3,delay_time)
                                elif relay_num == 4: control_relay(relay_4,delay_time)
                                elif relay_num == 5: control_relay(relay_5,delay_time)
                                elif relay_num == 6: control_relay(relay_6,delay_time)
                                elif relay_num == 7: control_relay(relay_7,delay_time)
                                elif relay_num == 8: control_relay(relay_8,delay_time)

                except Exception as e:
                    log(repr(e))
                    print(ret_byte)
try:
    # with open('/sd/log.txt','w') as f:
    #     f.write('[%s]:start\n' % int(pyb.millis()/1000))
    main()
except Exception as e:
    log(repr(e))