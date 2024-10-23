import numpy as np

def encode(data, k1, k2, g, z = 1):
    rows = k1
    cols = k2
    depth = z

    encoded_data = np.zeros((depth, rows + 1, cols + 1), dtype='int8')

    encoded_data[:depth, :rows, :cols] = np.reshape(data, (depth, rows, cols))

    for k in range(depth):
        for i in range(rows):
            encoded_data[k, i, cols] = np.bitwise_xor.reduce(encoded_data[k, i, :cols])

        for j in range(cols):
            encoded_data[k, rows, j] = np.bitwise_xor.reduce(encoded_data[k, :rows, j])

    return encoded_data


def decode(encoded_data, k1, k2, g, z=1):
    rows = k1
    cols = k2
    depth = z

    data_matrix = encoded_data[:depth, :rows, :cols].copy()

    for k in range(depth):
        row_errors = np.zeros(rows, dtype='int8')
        for i in range(rows):
            row_xor = np.bitwise_xor.reduce(data_matrix[k, i, :])
            if row_xor != encoded_data[k, i, cols]:
                row_errors[i] = 1

        col_errors = np.zeros(cols, dtype='int8')
        for j in range(cols):
            col_xor = np.bitwise_xor.reduce(data_matrix[k, :, j])
            if col_xor != encoded_data[k, rows, j]:
                col_errors[j] = 1

        if np.sum(row_errors) == 1 and np.sum(col_errors) == 1:
            error_row = np.where(row_errors == 1)[0][0]
            error_col = np.where(col_errors == 1)[0][0]
            print(f"Обнаружена и исправлена ошибка в позиции: ({k}, {error_row}, {error_col})")
            data_matrix[k, error_row, error_col] ^= 1
        else:
            if np.sum(row_errors) > 0 or np.sum(col_errors) > 0:
                print("Обнаружены ошибки в строках или столбцах, исправить невозможно.")

    return data_matrix


k1 = 2
k2 = 2
z = 3
g = 2

print(f"Настройки: k1 = {k1} | k2 = {k2} | z = {z} | g = {g}")

# data = [1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0]
data = [1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0]
print("Исходные данные:")
print(data)

encoded = encode(data, k1, k2, g, z=z)
print("Закодированные данные:")
print(encoded)

# Вносим ошибку
encoded[1, 1, 1] ^= 1
print("\nДанные с ошибкой:")
print(encoded)

decoded = decode(encoded, k1, k2, g, z)
print("\nДекодированные данные:")
print(decoded.flatten())
