def obtener_adeudos_por_fecha(conn, fecha_inicio, fecha_fin):
    query = """
    WITH SALDOS_VALIDOS AS (
        SELECT
            S.CLIENTE_ID,
            S.ANO,
            S.MES,
            S.ULTIMO_DIA,
            S.CARGOS_CXC,
            S.CARGOS_XACR,
            S.CREDITOS_CXC,
            S.CREDITOS_XACR,
            CAST(
                S.ANO || '-' ||
                SUBSTRING('00' || S.MES FROM CHAR_LENGTH('00' || S.MES) - 1 FOR 2) || '-' ||
                SUBSTRING('00' || S.ULTIMO_DIA FROM CHAR_LENGTH('00' || S.ULTIMO_DIA) - 1 FOR 2)
            AS DATE) AS FECHA
        FROM SALDOS_CC S
        WHERE
            S.ANO BETWEEN 1900 AND 2100
            AND S.MES BETWEEN 1 AND 12
            AND S.ULTIMO_DIA BETWEEN 1 AND 31
    )

    SELECT 
        C.CLIENTE_ID,
        C.NOMBRE AS CLIENTE,
        C.MONEDA_ID,
        SUM(
            CASE 
                WHEN SV.FECHA BETWEEN ? AND ?
                THEN SV.CARGOS_CXC + SV.CARGOS_XACR - SV.CREDITOS_CXC - SV.CREDITOS_XACR
                ELSE 0
            END
        ) AS SALDO_CXC,

        (SELECT 
            SUM(D.IMPORTE_NETO + D.TOTAL_IMPUESTOS)
         FROM DOCTOS_VE D
         WHERE 
            D.CLIENTE_ID = C.CLIENTE_ID
            AND D.TIPO_DOCTO = 'R'
            AND D.ESTATUS = 'P'
            AND D.MONEDA_ID = C.MONEDA_ID
            AND D.FECHA BETWEEN ? AND ?
        ) AS REMISIONES_PENDIENTES

    FROM SALDOS_VALIDOS SV
    JOIN CLIENTES C ON SV.CLIENTE_ID = C.CLIENTE_ID

    GROUP BY C.CLIENTE_ID, C.NOMBRE, C.MONEDA_ID

    HAVING SUM(
        CASE 
            WHEN SV.FECHA BETWEEN ? AND ?
            THEN SV.CARGOS_CXC + SV.CARGOS_XACR - SV.CREDITOS_CXC - SV.CREDITOS_XACR
            ELSE 0
        END
    ) <> 0
    OR (SELECT 
            SUM(D.IMPORTE_NETO + D.TOTAL_IMPUESTOS)
        FROM DOCTOS_VE D
        WHERE 
            D.CLIENTE_ID = C.CLIENTE_ID
            AND D.TIPO_DOCTO = 'R'
            AND D.ESTATUS = 'P'
            AND D.MONEDA_ID = C.MONEDA_ID
            AND D.FECHA BETWEEN ? AND ?
    ) IS NOT NULL
    """
    cursor = conn.cursor()
    params = [
        fecha_inicio, fecha_fin,  # Para SALDOS
        fecha_inicio, fecha_fin,  # Para subquery 1 (REMISIONES)
        fecha_inicio, fecha_fin,  # Para HAVING SALDOS
        fecha_inicio, fecha_fin   # Para subquery 2 en HAVING
    ]
    cursor.execute(query, params)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    return rows, columns
