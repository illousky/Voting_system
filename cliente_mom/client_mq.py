import pika
import sys

def cancelar_voto(hostname, port, id_voto): 

    try:
        # TODO: conectar con rabbitMQ
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port, credentials=pika.PlainCredentials('alumnomq', 'alumnomq')))
    except Exception as e:
        print("Error al conectar al host remoto:", e)
        exit()

    # TODO: declarar cola y publicar mensaje
    channel = connection.channel()
    
    channel.queue_declare(queue='voto_cancelacion')
    
    channel.basic_publish(exchange='', routing_key='voto_cancelacion', body=id_voto)
    
    print(f"[x] Enviada solicitud de cancelación para el voto ID: {id_voto}")

    # TODO: cerrar conexion
    connection.close()

def main():

    if len(sys.argv) != 4:
        print("Debe indicar el host, el numero de puerto, y el ID del voto a cancelar como un argumento.")
        exit()

    cancelar_voto(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
    main()
