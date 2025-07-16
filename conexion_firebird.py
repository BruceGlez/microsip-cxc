import fdb

def conectar_firebird():
    try:
        conn = fdb.connect(
            host='192.168.2.8',  # Cambia esta IP al servidor real
            database='C:/Microsip datos/ALGODONERA.FDB',  # Ruta local en el servidor
            user='SYSDBA',
            password='masterkey',
            charset='UTF8'
        )
        return conn
    except Exception as e:
        raise ConnectionError(f"No se pudo conectar a la base de datos: {e}")