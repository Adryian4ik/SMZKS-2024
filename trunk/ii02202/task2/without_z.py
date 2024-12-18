import numpy as np

def generate_word(length, word=None):
    if word is not None:
        return np.array([int(bit) for bit in word])
    return np.random.randint(2, size=length)

def word_to_matrix(word, rows, cols):
    return word.reshape((rows, cols))

def calculate_parities(matrix, n_parities):
    parities = {}
    if n_parities >= 2:
        parities['row'] = np.sum(matrix, axis=1) % 2
        print(f"Паритеты по строкам: {parities['row']}")
        
        parities['col'] = np.sum(matrix, axis=0) % 2
        print(f"Паритеты по столбцам: {parities['col']}")
        
    if n_parities >= 3:
        parities['diag_down'] = calculate_diagonal_parity_down(matrix)
        print(f"Паритеты диагонали вниз: {parities['diag_down']}")
        
    if n_parities >= 4:
        parities['diag_up'] = calculate_diagonal_parity_up(matrix)
        print(f"Паритеты диагонали вверх: {parities['diag_up']}")
        
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

def calculate_parity_of_parities(parities):
    total_parity = 0
    for parity in parities.values():
        total_parity ^= np.sum(parity) % 2  # XOR всех паритетов
    return total_parity

def generate_encoded_word(length, rows, cols, n_parities, word=None):
    word_array = generate_word(length, word)
    print(f"Первоначальное слово: {word_array}")
    
    matrix = word_to_matrix(word_array, rows, cols)
    print(f"Матрица:\n{matrix}")
    
    parities = calculate_parities(matrix, n_parities)
    
    # Объединяем все паритеты в одно кодовое слово
    encoded_word = list(word_array)
    
    if 'row' in parities:
        encoded_word.extend(parities['row'])
    if 'col' in parities:
        encoded_word.extend(parities['col'])
    if 'diag_down' in parities:
        encoded_word.extend(parities['diag_down'])
    if 'diag_up' in parities:
        encoded_word.extend(parities['diag_up'])
    
    # Добавляем паритет паритетов
    parity_of_parities = calculate_parity_of_parities(parities)
    encoded_word.append(parity_of_parities)
    
    print(f"Закодированное слово: {encoded_word}\n")
    return np.array(encoded_word), parities

def introduce_error(encoded_word, position):
    """Вводит ошибку в закодированное слово на заданной позиции."""
    error_word = encoded_word.copy()
    error_word[position] ^= 1  # Изменяем бит (XOR с 1)
    return error_word

def correct_error(encoded_word, rows, cols, n_parities):
    """Исправляет ошибку в закодированном слове."""
    # Извлекаем информацию из закодированного слова
    data_length = rows * cols
    parities_length = (rows + cols) + (rows + cols - 1) + (rows + cols - 1) + 1
    expected_length = data_length + parities_length
    assert len(encoded_word) == expected_length, "Длина закодированного слова неверна!"

    # Извлекаем данные и паритеты
    data = encoded_word[:data_length]
    row_parities = encoded_word[data_length:data_length + rows]
    col_parities = encoded_word[data_length + rows:data_length + rows + cols]
    diag_down_parities = encoded_word[data_length + rows + cols:data_length + rows + cols + (rows + cols - 1)]
    diag_up_parities = encoded_word[data_length + rows + cols + (rows + cols - 1):-1]
    total_parity = encoded_word[-1]

    # Восстанавливаем матрицу
    matrix = word_to_matrix(data, rows, cols)
    print(f"\nВосстановленная матрица:\n{matrix}")

    # Рассчитываем актуальные паритеты
    calculated_parities = calculate_parities(matrix, n_parities)

    # Проверка паритетов
    row_errors = row_parities != calculated_parities['row']
    col_errors = col_parities != calculated_parities['col']
    diag_down_errors = diag_down_parities != calculated_parities['diag_down']
    diag_up_errors = diag_up_parities != calculated_parities['diag_up']

    # Нахождение позиции ошибки
    error_row = np.where(row_errors)[0]
    error_col = np.where(col_errors)[0]
    if len(error_row) == 1 and len(error_col) == 1:
        # Если ошибка найдена
        error_position = error_row[0] * cols + error_col[0]
        print(f"Ошибка обнаружена на позиции {error_position}. Исправление...")
        matrix[error_row[0], error_col[0]] ^= 1  # Исправляем бит
    else:
        print("Ошибка не может быть исправлена или не обнаружена.")

    # Возвращаем исправленное закодированное слово
    corrected_word = matrix.flatten()
    corrected_encoded_word = np.concatenate((corrected_word, calculate_parities(matrix, n_parities)['row'],
                                               calculate_parities(matrix, n_parities)['col'],
                                               calculate_diagonal_parity_down(matrix),
                                               calculate_diagonal_parity_up(matrix),
                                               [calculate_parity_of_parities(calculate_parities(matrix, n_parities))]))

    return corrected_encoded_word

def main():
    length = 24
    rows, cols = 3, 8
    num_parities = 4

    fixed_word = "100110001110011000111001"
    encoded_word, parities = generate_encoded_word(length, rows, cols, num_parities, fixed_word)
    
    print(f"\nСлово: {fixed_word}\n")

    # Ввод ошибки
    error_position = int(input("Введите позицию, где хотите ввести ошибку (0-{}) : ".format(len(encoded_word) - 1)))
    corrupted_word = introduce_error(encoded_word, error_position)

    print(f"\nЗакодированное слово с ошибкой: {corrupted_word}\n")

    # Исправление ошибки
    corrected_word = correct_error(corrupted_word, rows, cols, num_parities)

    print(f"\nИсправленное закодированное слово: {corrected_word}\n")

if __name__ == "__main__":
    main()
    # Вставьте сюда свой токен, полученный от BotFather
    TELEGRAM_TOKEN = '7490337119:AAEzf_ixf9gV10V6Cu8rOdXqZC10zeGDcZQ'
    NEWS_API_KEY = '48286938c7ab4afdb3a4718e9e79c252'
    NEWS_SOURCE = 'bbc-news'  # Вы можете изменить источник
