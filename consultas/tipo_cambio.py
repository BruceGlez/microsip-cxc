def obtener_tipo_cambio_hoy(conn):
    query = """
    SELECT 
        TIPO_CAMBIO
    FROM 
        HISTORIA_CAMBIARIA 
    WHERE 
        FECHA = CURRENT_DATE
        AND MONEDA_ID = 620
    """
    cursor = conn.cursor()
    cursor.execute(query)
    row = cursor.fetchone()
    cursor.close()

    if row:
        return float(row[0])
    else:
        return None
