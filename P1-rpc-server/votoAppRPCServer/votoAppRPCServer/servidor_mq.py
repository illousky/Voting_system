# Uses RabbitMQ as the server
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# author: Ignacio González Porras (github.com/illousky)

import os
import sys
import django
import pika

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "votoSite.settings")
django.setup()

from votoAppRPCServer.models import Censo, Voto

def main():
    """
        Main function to set up the RabbitMQ consumer for vote cancellation requests.
        It connects to the RabbitMQ server, declares the 'voto_cancelacion' queue,
        and processes messages from the queue to cancel votes based on their ID.
        
        Usage:
            python servidor_mq.py <hostname> <port>
                <hostname>: The hostname of the RabbitMQ server.
                <port>: The port number of the RabbitMQ server.
                
            The script listens for messages on the 'voto_cancelacion' queue and processes them
            to cancel votes by changing their status code to '111'.
    """

    if len(sys.argv) != 3:
        print("Debe indicar el host y el puerto")
        exit()

    hostname = sys.argv[1]
    port = sys.argv[2]

    # Connect to RabbitMQ server
    
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port, credentials=pika.PlainCredentials('alumnomq', 'alumnomq')))
        channel = connection.channel()
    except Exception as e:
        print(f" [!] Error al conectar con RabbitMQ: {e}")
        exit()
    print(f" [*] Conectado a RabbitMQ en {hostname}:{port}")

    # Declare the queue for vote cancellation requests
    try:
        channel.queue_declare(queue='voto_cancelacion')
    except Exception as e:
        print(f" [!] Error al declarar la cola 'voto_cancelacion': {e}")
        exit()
    print(" [*] Cola 'voto_cancelacion' declarada correctamente")

    # Callback function to process messages from the queue
    def callback(ch, method, properties, body):
        try:
            # Process the message to cancel a vote
            voto_id = body.decode('utf-8')
            print(f" [x] Recibida solicitud para cancelar voto con ID: {voto_id}")
            
            # Look up the vote by ID and cancel it by changing its status code to '111'
            try:
                voto = Voto.objects.get(id=voto_id)
                voto.codigoRespuesta = '111'
                voto.save()
                print(f" [x] Voto con ID {voto_id} cancelado correctamente")
            except Voto.DoesNotExist:
                print(f" [x] Voto con ID {voto_id} no encontrado, cancelación fallida")
            except Exception as e:
                print(f" [x] Error al cancelar el voto: {e}")
            
            # Confirm message processing
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f" [x] Error al procesar el mensaje: {e}")

    # Set QoS to ensure fair distribution of messages
    channel.basic_qos(prefetch_count=1)

    # Attach the callback function to the queue
    channel.basic_consume(queue='voto_cancelacion', on_message_callback=callback)

    print(' [*] Esperando mensajes. Para salir presione CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":

    main()