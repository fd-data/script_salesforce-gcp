#!/bin/bash

# Ativa o ambiente virtual
echo "Ativando o ambiente virtual..."
source .venv/Scripts/activate

# Executa o script Python
echo "Iniciando processamento..."
python -u main.py

# Finaliza execução
echo "Execução concluída."

# Pergunta se deseja fechar o terminal
read -p "Pressione qualquer tecla para fechar ou Ctrl+C para manter aberto..."