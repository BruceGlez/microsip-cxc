import pandas as pd

def generar_resumen_por_cliente_base(df_raw):
    df = df_raw.copy()
    df['MONEDA_ID'] = pd.to_numeric(df['MONEDA_ID'], errors='coerce')

    def pesos(row):
        return row['REMISIONES_PENDIENTES'] if row['MONEDA_ID'] == 1 else 0

    def dolares(row):
        return row['REMISIONES_PENDIENTES'] if row['MONEDA_ID'] == 620 else 0

    def saldo_pesos(row):
        return row['SALDO_CXC'] if row['MONEDA_ID'] == 1 else 0

    def saldo_dolares(row):
        return row['SALDO_CXC'] if row['MONEDA_ID'] == 620 else 0

    df['REMISIONES_PESOS'] = df.apply(pesos, axis=1)
    df['REMISIONES_DOLARES'] = df.apply(dolares, axis=1)
    df['CXC_PESOS'] = df.apply(saldo_pesos, axis=1)
    df['CXC_DOLARES'] = df.apply(saldo_dolares, axis=1)

    resumen = df.groupby('CLIENTE').agg({
        'REMISIONES_PESOS': 'sum',
        'CXC_PESOS': 'sum',
        'REMISIONES_DOLARES': 'sum',
        'CXC_DOLARES': 'sum'
    }).reset_index()

    return resumen
