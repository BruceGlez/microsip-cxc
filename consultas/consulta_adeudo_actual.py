def obtener_adeudos_actuales(conn, fecha_corte):
    query = """
    SELECT
        C.CLIENTE_ID,
        C.NOMBRE AS CLIENTE,
        C.MONEDA_ID,

        -- Saldo actual en SALDOS_CC
        SUM(S.CARGOS_CXC + S.CARGOS_XACR - S.CREDITOS_CXC - S.CREDITOS_XACR) AS SALDO_CXC,

        -- Remisiones pendientes hasta la fecha seleccionada
        (SELECT 
            SUM(D.IMPORTE_NETO + D.TOTAL_IMPUESTOS)
         FROM DOCTOS_VE D
         WHERE 
            D.CLIENTE_ID = C.CLIENTE_ID
            AND D.TIPO_DOCTO = 'R'
            AND D.ESTATUS = 'P'
            AND D.MONEDA_ID = C.MONEDA_ID
            AND D.FECHA <= ?
        ) AS REMISIONES_PENDIENTES

    FROM SALDOS_CC S
    JOIN CLIENTES C ON S.CLIENTE_ID = C.CLIENTE_ID

    GROUP BY C.CLIENTE_ID, C.NOMBRE, C.MONEDA_ID

    HAVING
        SUM(S.CARGOS_CXC + S.CARGOS_XACR - S.CREDITOS_CXC - S.CREDITOS_XACR) +
        COALESCE(
            (SELECT 
                SUM(D.IMPORTE_NETO + D.TOTAL_IMPUESTOS)
             FROM DOCTOS_VE D
             WHERE 
                D.CLIENTE_ID = C.CLIENTE_ID
                AND D.TIPO_DOCTO = 'R'
                AND D.ESTATUS = 'P'
                AND D.MONEDA_ID = C.MONEDA_ID
                AND D.FECHA <= ?
            ), 0
        ) > 0
    """
    cursor = conn.cursor()
    params = [fecha_corte, fecha_corte]
    cursor.execute(query, params)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    return rows, columns
