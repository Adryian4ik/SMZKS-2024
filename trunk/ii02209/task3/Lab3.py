N = 357114156277
e1 = 1025537
e2 = 722983
C1 = 68639736967
C2 = 204258645263

r = 286243
s = 406030

result_check = e1 * r - e2 * s
print("Проверка уравнения e1 * r - e2 * s =", result_check)

result1 = pow(C1, r, N)
print("C1^r mod N =", result1)

result2 = pow(C2, -s, N)
print("C2^(-s) mod N =", result2)

m = (result1 * result2) % N
print("Результат дешифрации (m mod N) =", m)

try:
    decoded_message = m.to_bytes((m.bit_length() + 7) // 8, 'big').decode()
    print("Сообщение в текстовом виде:", decoded_message)
except UnicodeDecodeError:
    print("Сообщение не может быть корректно преобразовано в текст.")
