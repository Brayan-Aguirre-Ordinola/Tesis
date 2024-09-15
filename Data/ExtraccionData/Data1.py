import numpy as np
import pandas as pd

file_path = 'data05-09-24.csv'

# Leer el archivo para inspeccionarlo manualmente
with open(file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Definir el índice de la línea donde empiezan los nombres de las columnas
header_line = 12  

data_lines = lines[header_line:] 


columns = data_lines[0].strip().split(',')
data = [line.strip().split(',') for line in data_lines[1:]]

data_dict = {col: np.array([row[i] for row in data], dtype=object) for i, col in enumerate(columns)}

print({key: data_dict[key][:5] for key in list(data_dict.keys())[:5]})
