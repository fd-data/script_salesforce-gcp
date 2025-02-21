import sys
import time

def print_progress_bar(x, y, bar_length=40):
    # Calcula a porcentagem de progresso
    percent = float(x) / y
    # Calcula o número de blocos completos na barra
    block = int(round(bar_length * percent))
    
    # Cria a barra de carregamento
    progress_bar = ">" * block + " " * (bar_length - block)
    progress_text = f"\r[{progress_bar}] {percent * 100:.2f}% ({x}/{y})"
    
    # Printa a barra de carregamento na mesma linha
    sys.stdout.write(progress_text)
    sys.stdout.flush()

# # Exemplo de uso
# X = 0
# Y = 200

# while X <= Y:
#     print_progress_bar(X, Y)
#     time.sleep(0.1)  # Simula tempo de processamento
#     X += 1

# print("\nProcesso concluído!")
