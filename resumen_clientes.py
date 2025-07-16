import pandas as pd
import re

def generar_resumen_por_cliente_base(df_raw):
    def limpiar_nombre(nombre):
        if not nombre:
            return ""
        nombre = nombre.strip().upper()
        return re.sub(r"^[12]\s*", "", nombre)

    df_raw['CLIENTE_BASE'] = df_raw['CLIENTE'].apply(limpiar_nombre)
    df_raw['MONEDA_ID'] = pd.to_numeric(df_raw['MONEDA_ID'], errors='coerce').fillna(0).astype(int)

    resumen = (
        df_raw.groupby('CLIENTE_BASE', group_keys=False)
        .apply(
            lambda g: pd.Series({
                'REMISIONES_PESOS': g.loc[g['MONEDA_ID'] == 1, 'REMISIONES_PENDIENTES'].sum(),
                'CXC_PESOS': g.loc[g['MONEDA_ID'] == 1, 'SALDO_CXC'].sum(),
                'REMISIONES_DOLARES': g.loc[g['MONEDA_ID'] == 620, 'REMISIONES_PENDIENTES'].sum(),
                'CXC_DOLARES': g.loc[g['MONEDA_ID'] == 620, 'SALDO_CXC'].sum(),
            }),
            include_groups=False
        )
        .reset_index()
        .fillna(0)
    )

    return resumen