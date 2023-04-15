from paho.mqtt.client import Client
import sys

K0 = 25
K1 = 60
listening_humidity = False

def on_connect(mqttc, userdata, flags, rc):
    print("CONNECT:", userdata, flags, rc)

def on_message(mqttc, userdata, msg):
    global listening_humidity
    print("MESSAGE:", userdata, msg.topic, msg.qos, msg.payload, msg.retain)
    
    if msg.topic == 'temperature/t1' or msg.topic == 'temperature/t2':
        temperature = int(msg.payload.decode())
        
        if temperature > K0 and not listening_humidity:
            print("Listening to humidity")
            mqttc.subscribe('humidity')
            listening_humidity = True
        elif (temperature <= K0 or listening_humidity) and listening_humidity:
            print("Not listening to humidity")
            mqttc.unsubscribe('humidity')
            listening_humidity = False
        
    elif msg.topic == 'humidity':
        humidity = int(msg.payload.decode())
        
        if humidity > K1 and not listening_humidity:
            print("Listening to humidity")
            mqttc.subscribe('humidity')
            listening_humidity = True
        elif humidity <= K1 and listening_humidity:
            print("Not listening to humidity")
            mqttc.unsubscribe('humidity')
            listening_humidity = False

def on_publish(mqttc, userdata, mid):
    print("PUBLISH:", userdata, mid)

def on_subscribe(mqttc, userdata, mid, granted_qos):
    print("SUBSCRIBED:", userdata, mid, granted_qos)

def on_log(mqttc, userdata, level, string):
    print("LOG", userdata, level, string)


def main(hostname):
    mqttc = Client(userdata="data (of any type) for user")
    mqttc.enable_logger()

    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    mqttc.on_log = on_log

    mqttc.connect(hostname)

    mqttc.subscribe('temperature/t1')
    mqttc.subscribe('temperature/t2')

    mqttc.loop_forever()


if __name__ == '__main__':
    hostname = 'simba.fdi.ucm.es'
    if len(sys.argv)>1:
        hostname = sys.argv[1]
    main(hostname)

