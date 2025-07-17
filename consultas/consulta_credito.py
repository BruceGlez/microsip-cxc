def obtener_saldos_credito(conn):
    query = """
    SELECT 
        C.CLIENTE_ID,
        C.NOMBRE AS CLIENTE,
        C.MONEDA_ID,
        SUM(S.CARGOS_CXC + S.CARGOS_XACR - S.CREDITOS_CXC - S.CREDITOS_XACR) AS SALDO_CXC,
        (SELECT 
            SUM(D.IMPORTE_NETO + D.TOTAL_IMPUESTOS)
         FROM DOCTOS_VE D
         WHERE 
            D.CLIENTE_ID = C.CLIENTE_ID
            AND D.TIPO_DOCTO = 'R'
            AND D.ESTATUS = 'P'
            AND D.MONEDA_ID = C.MONEDA_ID
        ) AS REMISIONES_PENDIENTES
    FROM SALDOS_CC S
    JOIN CLIENTES C ON S.CLIENTE_ID = C.CLIENTE_ID
    GROUP BY C.CLIENTE_ID, C.NOMBRE, C.MONEDA_ID
    HAVING SUM(S.CARGOS_CXC + S.CARGOS_XACR - S.CREDITOS_CXC - S.CREDITOS_XACR) <> 0
        OR (SELECT 
                SUM(D.IMPORTE_NETO + D.TOTAL_IMPUESTOS)
            FROM DOCTOS_VE D
            WHERE 
                D.CLIENTE_ID = C.CLIENTE_ID
                AND D.TIPO_DOCTO = 'R'
                AND D.ESTATUS = 'P'
                AND D.MONEDA_ID = C.MONEDA_ID
        ) IS NOT NULL
    """
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    return rows, columns

def obtener_detalle_cliente(conn, cliente_id):
    cursor = conn.cursor()

    # SALDOS_CC
    cursor.execute("""
        SELECT * FROM SALDOS_CC WHERE CLIENTE_ID = ?
    """, (cliente_id,))
    saldos = cursor.fetchall()
    columnas_saldos = [desc[0] for desc in cursor.description]

    # REMISIONES PENDIENTES
    cursor.execute("""
        SELECT * FROM DOCTOS_VE 
        WHERE CLIENTE_ID = ? AND TIPO_DOCTO = 'R' AND ESTATUS = 'P'
    """, (cliente_id,))
    remisiones = cursor.fetchall()
    columnas_rem = [desc[0] for desc in cursor.description]

    cursor.close()
    return (
        pd.DataFrame(saldos, columns=columnas_saldos),
        pd.DataFrame(remisiones, columns=columnas_rem)
    )

