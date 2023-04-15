import time
import random
import statistics
from paho.mqtt.client import Client
import sys

# Función para determinar si un número es primo
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Función para calcular el valor medio de una lista de valores
def calculate_mean(values):
    if len(values) == 0:
        return 0
    return sum(values) / len(values)

def on_connect(client, rc):
    print("Conectado con código de resultado: " + str(rc))
    client.subscribe("numbers")
    
# Función que se ejecutará cuando se reciba un mensaje en el topic "numbers"
def on_message_numbers(client, userdata, message):
    number = int(message.payload.decode())
    print(f"Received number: {number}")
    if is_prime(number):
        print("Number is prime, listening to humidity for 5 seconds...")
        client.subscribe("humidity")
        time.sleep(5) # Esperamos 5 segundos
        client.unsubscribe("humidity")

# Función que se ejecutará cuando se reciba un mensaje en el topic "humidity"
def on_message_humidity(client, userdata, message):
    humidity = float(message.payload.decode())
    print(f"Received humidity: {humidity}")
    values = []
    values.append(humidity)
    if len(values) >= 5:
        mean = calculate_mean(values)
        print(f"Mean humidity over 5 seconds: {mean}")
        values = []



def main(hostname):
    client = Client()
    client.on_connect = on_connect
    client.on_message = on_message_numbers
    client.message_callback_add("humidity", on_message_humidity)
    client.username_pw_set('cadena_client', password=None)
    client.connect(hostname)
    client.loop_start()


if __name__ == '__main__':
    hostname = 'simba.fdi.ucm.es'
    if len(sys.argv)>1:
        hostname = sys.argv[1]
    main(hostname)


