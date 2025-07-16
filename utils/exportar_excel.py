import pandas as pd

def exportar_df_excel(df, path):
    try:
        df.to_excel(path, index=False, float_format="%.2f")
        return True, None
    except Exception as e:
        return False, str(e)
