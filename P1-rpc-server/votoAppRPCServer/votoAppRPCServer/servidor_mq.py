# Uses RabbitMQ as the server

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

    if len(sys.argv) != 3:
        print("Debe indicar el host y el puerto")
        exit()

    hostname = sys.argv[1]
    port = sys.argv[2]

    # TODO: completar segun las indicaciones

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port, credentials=pika.PlainCredentials('alumnomq', 'alumnomq')))
    channel = connection.channel()

    channel.queue_declare(queue='voto_cancelacion')

    def callback(ch, method, properties, body):
        try:
            # Procesar el mensaje
            voto_id = body.decode('utf-8')
            print(f" [x] Recibida solicitud para cancelar voto con ID: {voto_id}")
            
            # Buscar el voto y cambiar su código a '111' para marcarlo como cancelado
            try:
                voto = Voto.objects.get(id=voto_id)
                voto.codigoRespuesta = '111'
                voto.save()
                print(f" [x] Voto con ID {voto_id} cancelado correctamente")
            except Voto.DoesNotExist:
                print(f" [x] Voto con ID {voto_id} no encontrado, cancelación fallida")
            except Exception as e:
                print(f" [x] Error al cancelar el voto: {e}")
            
            # Confirmar el mensaje
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f" [x] Error al procesar el mensaje: {e}")

    # Establecer QoS para procesar mensajes uno a uno
    channel.basic_qos(prefetch_count=1)

    # Asociar la función callback a la cola
    channel.basic_consume(queue='voto_cancelacion', on_message_callback=callback)

    print(' [*] Esperando mensajes. Para salir presione CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":

    main()