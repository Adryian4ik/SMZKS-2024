def inverse_value(m: int, p: int):
    P = [1]
    q = [None]
    m = m % p
    p1 = p
    q.append(p1 // m)
    P.append(p1 // m)
    temp = p1
    p1 = m
    m = temp % m
    while m != 0:
        q.append(p1 // m)
        P.append(P[-1] * q[-1] + P[-2])
        temp = p1
        p1 = m
        m = temp % m
    return ((-1) ** (len(q) - 2) * P[-2]) % p

c1 = [
400967861722,
402921963995,
345366187498,
170749944344,
398474550143,
14128843304,
525338681306,
553357177665,
554714202377,
378737847392,
241207247252,
330231009566]



c2 = [
400511331925,
359110439723,
156672928720,
81237697207,
446268495117,
567101402400,
380678770261,
405322363448,
250349383856,
480141604318,
201068876886,
160562856485]


c3 = [
365230039044,
503139848290,
452112473725,
98832137945,
16750539498,
496867432761,
98372266130,
349596187748,
172522293935,
161623878001,
405142270947,
404286756199]


def main():

    N1 = 570206339323
    N2 = 572010531679
    N3 = 573673162471

    m0 = N1 * N2 * N3
    m1 = N2 * N3
    m2 = N1 * N3
    m3 = N1 * N2

    n1 = inverse_value(m1, N1)
    n2 = inverse_value(m2, N2)
    n3 = inverse_value(m3, N3)

    byte_sequence = []

    print('Исходные блоки:')
    for index in range(len(c1)):

        y1 = c1[index]
        y2 = c2[index]
        y3 = c3[index]

        s = (y1 * n1 * m1 + y2 * n2 * m2 + y3 * n3 * m3) % m0

        x = round(s ** (1. / 3))

        for i in range(4):
            y = (x >> (8* (3 - i))) & 0xff
            byte_sequence.append(y)
            print(f'{y:#010b} ', end='')

        print()

    print('Исходный текст:')
    print(bytes(byte_sequence).decode('windows-1251'))



if __name__ == "__main__":
    main()