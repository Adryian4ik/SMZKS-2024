from sympy import mod_inverse
from math import isqrt

def int_to_ascii(number):
    bin_str = bin(number)[2:]
    bytes_array = []
    for i in range(0, len(bin_str), 8):
        byte_str = bin_str[i:i + 8].zfill(8)
        byte = int(byte_str, 2)
        bytes_array.append(byte)

    ascii_chars = bytes(bytes_array).decode('windows-1251', errors='ignore')
    return ascii_chars


def main():
    N = 65815671868057
    e = 7423489
    C = 38932868535359

    n = isqrt(N) + 1

    i = 2
    D = 0  
    while True:
        t = n + i  
        w = pow(t, 2) - N
        D = isqrt(w)

        if D * D == w:  
            break
        
        i += 1

    p = t + D
    q = t - D
    AB = (p - 1) * (q - 1)  
    d = mod_inverse(e, AB)  

    M = pow(C, d, N)
    text = int_to_ascii(M)

    print(f"Дешифрованное значение (M) = {M}")
    print(f"Дешифрованный текст: {text}")


if __name__ == "__main__":
    main()
