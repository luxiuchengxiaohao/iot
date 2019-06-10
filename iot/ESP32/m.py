from simple import *
from urequests import *
import machine,ubinascii,json,sys,time
MCU_ID = ubinascii.hexlify(machine.unique_id()).decode('utf-8','ignore')
while True:
    try:
        response = get('http://192.168.2.102:8000/sa/?sn=%s' % MCU_ID)
        res = json.loads(response.content.decode('utf-8'))
        break
    except Exception as e:
        print(repr(e))
        print('request faild retry in 3 second.')
        time.sleep(3)
if res['status'] != 0:
    sys.exit()
DEVICE_ID = res['data']['device_id']
PRODUCT_ID = '203568'
API_KEY = res['data']['key']
SERVER = "183.230.40.39"
TOPIC = b"esp32"


def pub_data(self, t):
    self.dht11.measure()
    value = {'datastreams': [{"id": "temp", "datapoints": [{"value": self.dht11.temperature()}]},
                             {"id": "humi", "datapoints": [{"value": self.dht11.humidity()}]}]}
    jdata = json.dumps(value)
    jlen = len(jdata)
    bdata = bytearray(jlen + 3)
    bdata[0] = 1  # publish data in type of json
    bdata[1] = int(jlen / 256)  # data lenght 固定两字节长度高位字节，值为0x00
    bdata[2] = jlen % 256  # data lenght  固定两字节长度低位字节，值为0x41
    bdata[3:jlen + 4] = jdata.encode('ascii')  # json data
    # print(bdata)
    print('publish data', str(self.pid + 1))
    self.mqttClient.publish('$dp', bdata)
    self.pid += 1
#端口号为：6002
def sub_cb(topic, msg):
    print((topic, msg))
def main():
    c = MQTTClient(DEVICE_ID, SERVER,6002,PRODUCT_ID,API_KEY)
    c.set_callback(sub_cb)
    c.connect()
    # tim = machine.Timer(-1)
    # tim.init(period=30000, mode=Timer.PERIODIC, callback=pub_data)  # Timer.PERIODIC   Timer.ONE_SHOT
    c.subscribe(TOPIC)
    print("Connected to %s, subscribed to %s topic" % (SERVER, TOPIC))
    try:
        while True:
            c.wait_msg()
    finally:
        c.disconnect()

main()
