# connect to the database, read the first 1000 entries
# then perform 1000 queries retrieving each one of the entries
# one by one. Measure the time requiered for the 1000 queries

import psycopg2
import time
import os
import django

# Configuracion de la base de datos
db_config = {
    'dbname': 'voto',
    'user': 'alumnodb',
    'password': 'alumnodb',
    'host': 'localhost',
    'port': '15432',
}

DB_URI="postgresql://neondb_owner:npg_pXukNK7EOw4Q@ep-curly-hall-a9z21sjf-pooler.gwc.azure.neon.tech/neondb?sslmode=require"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'votoSite.settings')
django.setup()

from votoAppRPCServer.models import Censo

try:
    # # Conexion a la base de datos
    # conn = psycopg2.connect(DB_URI)
    # cursor = conn.cursor()
    
    # # Leer las primeras 1000 entradas de la tabla censo
    # query_fetch_1000 = "SELECT * FROM censo LIMIT 1000"
    # cursor.execute(query_fetch_1000)
    # rows = cursor.fetchall()
    
    # # Preparar las busquedas individuales
    # search_query = 'SELECT * FROM censo WHERE "numeroDNI" = %s' # Asumiendo que hay una columna 'id' para identificar las filas
    
    rows = Censo.objects.all()[:1000]
    
    # Medir el tiempo de inicio
    start_time = time.time()
    
    # # Realizar las busquedas una a una
    # for row in rows:
    #     id_value = row[0] # Suponiendo que la primera columna es el ID
    #     cursor.execute(search_query, (id_value,))
    #     cursor.fetchone() # Obtener la fila encontrada
    
    for row in rows:
        voto = Censo.objects.get(numeroDNI=row.numeroDNI)
        
    # Medir el tiempo de finalizacion
    end_time = time.time()
    
    # Mostrar los resultados
    print(f"Tiempo invertido en buscar las 1000 entradas una a una: {end_time - start_time:.6f} segundos")
    
except Exception as e:
    print(f"Error: {e}")
    
# finally:
#     # Cerrar el cursor y la conexion
#     if 'cursor' in locals():
#         cursor.close()
#     if 'conn' in locals():
#         conn.close()