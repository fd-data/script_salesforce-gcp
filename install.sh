#!/bin/bash

# Instala a versão correta do Python
echo "Instalando Python 3.12 via pyenv..."
pyenv install 3.12

# Cria um ambiente virtual
echo "Criando ambiente virtual..."
python -m venv .venv

# Ativa o ambiente virtual
echo "Ativando o ambiente virtual..."
source .venv/Scripts/activate

# Instala as dependências do projeto
echo "Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

# Finaliza a instalação
echo "Instalação concluída."
