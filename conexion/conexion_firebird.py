from config import DB_CONFIG
import fdb

def conectar_firebird():
    try:
        conn = fdb.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        raise ConnectionError(f"No se pudo conectar a la base de datos: {e}")
