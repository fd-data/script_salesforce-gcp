import json
import pandas as pd
from src.controller.get_var import get_data_handle

def processar_todas_as_bases(var: str, cast_df: bool):
    """
    Percorre todas as bases definidas no arquivo handle-config.json e executa get_data_handle
    para cada uma, alterando dinamicamente o campo "nome".

    Retorna um dicionário com os resultados de cada base.
    """
    with open('./config/handle-config.json', 'r') as file:
        config = json.load(file)

    resultados = {}

    for item in config:
        nome_base = item.get("nome")
        if not nome_base:
            continue  # Pula caso não tenha um nome válido

        try:
            resultado = get_data_handle(nome_base, var, cast_df)
            resultados[nome_base] = resultado
        except Exception as e:
            resultados[nome_base] = f"Erro: {str(e)}"

    return resultados
