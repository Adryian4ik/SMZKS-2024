from math import ceil, isqrt


def find_p_q(N):
    x = ceil(isqrt(N))
    while True:
        y2 = x * x - N
        if y2 >= 0:
            y = isqrt(y2)
            if y * y == y2:
                break
        x += 1

    p = x - y
    q = x + y
    return p, q

def mod_inverse(e, phi):
    t, new_t = 0, 1
    r, new_r = phi, e
    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r
    if r > 1:
        raise ValueError(f"e ({e}) и phi ({phi}) не взаимно просты!")
    if t < 0:
        t = t + phi
    return t


def main():
    N = 59046883376179
    e = 4044583
    C = 32279109612093178386291829644165776716262130932846358952004865131300854626454832531128010537439035467533200364345449119792793192837356457079894549551319569174668782

    p, q = find_p_q(N)
    fN = (p - 1)*(q - 1)
    d = mod_inverse(e, fN)
    print(f"p = {p}, q = {q}, phi_N = {fN}\nЗакрытый ключ d = {d}\n")

    message = pow(C, d, N)
    print(f"Исходное сообщение: {message}")

if __name__ == "__main__":
    main()