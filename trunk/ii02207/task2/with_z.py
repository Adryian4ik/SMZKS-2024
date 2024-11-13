import numpy as np

# Исходное сообщение
message = "100110001110011000111001"

# Функция для разделения сообщения на части и формирования матриц
def split_message_into_matrices(message, matrix_size=(3, 2)):
    matrices = []
    step = matrix_size[0] * matrix_size[1]
    for i in range(0, len(message), step):
        part = message[i:i+step]
        if len(part) < step:
            # Если последняя часть меньше, дополним нулями
            part += '0' * (step - len(part))
        matrix = create_matrix(part)
        matrices.append(matrix)
    return matrices

# Функция для создания матрицы из бинарной строки
def create_matrix(binary_str):
    matrix = []
    for i in range(0, len(binary_str), 2):
        if i + 1 < len(binary_str):
            matrix.append([int(binary_str[i]), int(binary_str[i + 1])])
    return np.array(matrix)

# Функции для вычисления паритетов
def calculate_parities(matrix, n_parities):
    parities = {}
    if n_parities >= 2:
        parities['row'] = np.sum(matrix, axis=1) % 2
        parities['col'] = np.sum(matrix, axis=0) % 2
    if n_parities >= 3:
        parities['diag_down'] = calculate_diagonal_parity_down(matrix)
    if n_parities >= 4:
        parities['diag_up'] = calculate_diagonal_parity_up(matrix)
    return parities

def calculate_diagonal_parity_up(matrix):
    rows, cols = matrix.shape
    parities = []
    for offset in range(-(rows - 1), cols):
        diag = np.diagonal(matrix, offset=offset)
        parity = np.sum(diag) % 2
        parities.append(parity)
    return np.array(parities)

def calculate_diagonal_parity_down(matrix):
    flipped_matrix = np.fliplr(matrix)
    rows, cols = flipped_matrix.shape
    parities = []
    for offset in range(-(rows - 1), cols):
        diag = np.diagonal(flipped_matrix, offset=offset)
        parity = np.sum(diag) % 2
        parities.append(parity)
    return np.array(parities)[::-1]

def calculate_parity_of_parities(parities_list):
    total_parity = 0
    for parities in parities_list:
        for parity in parities.values():
            total_parity ^= np.sum(parity) % 2  # XOR всех паритетов
    return total_parity

# Функция для вычисления паритетов для n матриц
def calculate_parities_for_matrices(matrices, n_parities):
    parities_list = []
    for matrix in matrices:
        parities = calculate_parities(matrix, n_parities)
        parities_list.append(parities)
    return parities_list

# Функция для вычисления общего итеративного кода (конкатенация или поэлементное сложение по модулю 2)
def calculate_iterative_code(matrices):
    if len(matrices) < 2:
        return matrices[0]
    # Начинаем с первой матрицы и складываем все по модулю 2
    iterative_code = matrices[0]
    for matrix in matrices[1:]:
        iterative_code = (iterative_code + matrix) % 2
    return iterative_code

# Функция для конкатенации паритетов в строку
def parities_to_string(parities):
    parity_str = ''
    if 'row' in parities:
        parity_str += ''.join(map(str, parities['row']))
    if 'col' in parities:
        parity_str += ''.join(map(str, parities['col']))
    if 'diag_down' in parities:
        parity_str += ''.join(map(str, parities['diag_down']))
    if 'diag_up' in parities:
        parity_str += ''.join(map(str, parities['diag_up']))
    return parity_str

# Функция для формирования кодового слова
def form_codeword(message, parities_list, parity_of_parities, iterative_code):
    # Конкатенация всех элементов
    codeword = message
    for parities in parities_list:
        codeword += parities_to_string(parities)
    codeword += str(parity_of_parities)
    # Преобразуем общий итеративный код в строку и добавляем к кодовому слову
    iterative_code_str = ''.join(map(str, iterative_code.flatten()))
    codeword += iterative_code_str
    return codeword

# Шаг 1: Формируем матрицы из сообщения
matrix_size = (3, 2)
matrices = split_message_into_matrices(message, matrix_size)

# Проверка размеров матриц
for idx, matrix in enumerate(matrices):
    print(f"Матрица {idx + 1}:\n", matrix)

# Шаг 2: Вычисление паритетов для каждой матрицы
n_parities = 4  # Вычисляем паритеты строк, столбцов и диагоналей
parities_list = calculate_parities_for_matrices(matrices, n_parities)

# Вывод паритетов для каждой матрицы
for idx, parities in enumerate(parities_list):
    print(f"\nПаритеты для Матрицы {idx + 1}:")
    print(f"Паритеты строк: {parities.get('row')}")
    print(f"Паритеты столбцов: {parities.get('col')}")
    print(f"Паритеты диагонали (вправо): {parities.get('diag_down')}")
    print(f"Паритеты диагонали (влево): {parities.get('diag_up')}")

# Шаг 3: Нахождение паритета паритетов для всех матриц
parity_of_parities = calculate_parity_of_parities(parities_list)
print(f"Паритет паритетов для всех матриц: {parity_of_parities}")

# Шаг 4: Вычисление общего итеративного кода
iterative_code = calculate_iterative_code(matrices)
print("\nОбщий итеративный код:\n", iterative_code)

# Шаг 5: Формирование кодового слова
codeword = form_codeword(message, parities_list, parity_of_parities, iterative_code)
print("\nКодовое слово:", codeword)
print("\nДлина кодового слова:", len(codeword))