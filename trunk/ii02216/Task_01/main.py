import math


def check_verf_b(M):
    return int(math.log(len(M), 2))


def insert_error(M, index):
    M[index - 1] ^= 1
    return M


def sum_p_bts(p_index, M):
    for i in p_index:
        sum_index = 0
        step = i + 1
        for j in range(i, len(M), 2 * step):
            sum_index += sum(M[j: j + step])
        M[i] = sum_index % 2


def encode(M):
    print("Кодирование...")
    print("Исходный код:", M)
    p_index = []
    for i in range(check_verf_b(M) + 1):
        index = 2 ** i - 1
        p_index.append(index)
        M.insert(index, 0)

    print("Код с нулевыми контрольными битами:", M)

    sum_p_bts(p_index, M)

    print("Код Хэмминга:", M)


def decode(M):
    print("Декодирование...")
    p_index = []
    M_cp = M.copy()
    fls_ind = []

    for i in range(check_verf_b(M) + 1):
        index = 2 ** i - 1
        p_index.append(index)
        M[index] = 0

    sum_p_bts(p_index, M)

    for i in p_index:
        if M[i] != M_cp[i]:
            fls_ind.append(i + 1)
    return sum(fls_ind)


def main():
    M_bnr = 0b1011101010
    M = list(map(int, bin(M_bnr)[2:]))
    encode(M)
    error_ind = 2
    print("Код хэмминга с ошибкой в позиции:", error_ind, insert_error(M, error_ind))
    er_ind = decode(M)
    print("Ошибка в позиции:", er_ind)


if __name__ == "__main__":
    main()
