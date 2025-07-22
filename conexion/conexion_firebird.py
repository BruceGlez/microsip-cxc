# conexion/conexion_firebird.py
import fdb

def conectar_firebird(config):
    try:
        return fdb.connect(**config)
    except Exception as e:
        raise ConnectionError(f"No se pudo conectar a la base de datos: {e}")
