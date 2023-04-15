from paho.mqtt.client import Client
from time import sleep
import sys

t1_temperatures = [] #Variables globales para realizar los calculos solicitados
t2_temperatures = []

def calculate_statistics():
    t1_max = max(t1_temperatures)
    t1_min = min(t1_temperatures)
    t1_media = sum(t1_temperatures) / len(t1_temperatures)
    t2_max = max(t2_temperatures)
    t2_min = min(t2_temperatures)
    t2_media = sum(t2_temperatures) / len(t2_temperatures)
    print(f'SENSOR 1 - Max: {t1_max}, Min: {t1_min}, Media: {t1_media}')
    print(f'SENSOR 2 - Max: {t2_max}, Min: {t2_min}, Media: {t2_media}')
    # Vaciamos las listas
    t1_temperatures.clear()
    t2_temperatures.clear()

def on_connect(client, rc):
    print("Conectado con código de resultado: " + str(rc))
    client.subscribe('temperature/t1')
    client.subscribe('temperature/t2')

def on_message(client, userdata, msg):
    data = msg.payload.decode()
    topic = msg.topic
    if topic == 'temperature/t1':
        t1_temperatures.append(float(data))
    elif topic == 'temperature/t2':
        t2_temperatures.append(float(data))

# función principal
def main(hostname):
    client = Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set('temperature_client', password=None)
    client.connect(hostname)
    client.loop_start()

    while True:
        sleep(5) #Esperamos 5 segundos
        calculate_statistics()


if __name__ == '__main__':
    hostname = 'simba.fdi.ucm.es'
    if len(sys.argv)>1:
        hostname = sys.argv[1]
    main(hostname)
