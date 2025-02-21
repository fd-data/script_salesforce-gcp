import pandas as pd
from src.controller.get_var import get_data_handle

def convert_data(df: pd.DataFrame, nome_base: str) -> pd.DataFrame:
    """
    Converte as colunas especificadas para os tipos de dados indicados.

    Parâmetros:
    - df: DataFrame do pandas.
    - column_mapping: Dicionário com o formato {'coluna': 'tipo'}.

    Tipos suportados: 'int', 'float', 'str', 'date', 'datetime'.

    Retorna:
    - DataFrame com as colunas convertidas.
    """
    type_map = {
        'int': 'int64',
        'float': 'float64',
        'str': 'string',
        'date': 'datetime64[D]',
        'datetime': 'datetime64[ns]'
    }

    column_mapping = get_data_handle(nome_base, var='column_mapping', cast_df=False)

    for column, dtype in column_mapping.items():
        if column not in df.columns:
            raise ValueError(f"Coluna '{column}' não encontrada no DataFrame.")
        if dtype not in type_map:
            raise ValueError(f"Tipo '{dtype}' não é suportado. Use um dos seguintes: {', '.join(type_map.keys())}")

        try:
            df[column] = pd.to_datetime(df[column]) if dtype in ['date', 'datetime'] else df[column].astype(type_map[dtype])
        except Exception as e:
            raise ValueError(f"Erro ao converter a coluna '{column}' para '{dtype}': {e}")

    return df
    