from paho.mqtt.client import Client
from time import sleep
import sys
from sympy import isprime
    

def on_connect(client, userdata, rc):
    print("Conectado con código de resultado: " + str(rc))
    client.subscribe("numbers")

def on_message(client, userdata, msg):
    data = msg.payload.decode()
        
    try:
        num = int(data)
        num_str = str(num)
        if num_str in userdata['frecuencias']:
            userdata['frecuencias'][num_str] += 1
        else:
            userdata['frecuencias'][num_str] = 1
            
        userdata['enteros'].append(num)
        if isprime(num):
            print(f"Número entero primo: {num}")
        else:
            print("Número entero:", num)
            
    except ValueError:
        try:
            num = float(data)
            num_str = str(num)
            if num_str in userdata['frecuencias']:
                userdata['frecuencias'][num_str] += 1
            else:
                userdata['frecuencias'][num_str] = 1
                
            userdata['coma_flotante'].append(num)
            print("Número flotante:", num)
        except ValueError:
            print("No se pudo convertir el dato a número")
    
    for key, value in userdata.items():
        print(key, value)
            
            
def main(hostname):
    userdata = {
        'enteros': [],
        'coma_flotante': [],
        'frecuencias': {}
    }
    client = Client(userdata = userdata)
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set('num_client', password=None)
    client.connect(hostname)
    client.loop_start()
    
    while True:
        sleep(1)


if __name__ == '__main__':
    hostname = 'simba.fdi.ucm.es'
    if len(sys.argv)>1:
        hostname = sys.argv[1]
    main(hostname)


