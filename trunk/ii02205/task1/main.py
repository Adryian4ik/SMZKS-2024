from math import log2


def indexes(num: int):
    result = []
    i = 1
    while num != 0:
        if num & 0x01:
            result.append(i)
        num = num >> 1
        i *= 2
    return result


class HamingCode:
    r: int = 3

    @staticmethod
    def encode_block(bits: list):
        bits = [*bits]
        m = len(bits)
        n = m + HamingCode.r

        if (m + HamingCode.r + 1) > 2 ** HamingCode.r:
            raise Exception("Invalid block size")

        result = []

        for i in range(n):
            if log2(i + 1).is_integer():
                result.append(0)
            else:
                result.append(bits.pop(0))

        for i in range(n):
            index_list = indexes(i + 1)
            for index in index_list:
                result[index-1] ^= result[i]
                pass
        return result

    @staticmethod
    def decode_block(bits: list):
        bits = [*bits]
        n = len(bits)
        m = n - HamingCode.r

        if (m + HamingCode.r + 1) > 2 ** HamingCode.r:
            raise Exception("Invalid block size")

        bits_for_check = [*bits]

        for i in range(HamingCode.r):
            index = 2 ** i
            bits_for_check[index - 1] = 0

        for i in range(n):
            index_list = indexes(i + 1)
            for index in index_list:
                bits_for_check[index - 1] ^= bits_for_check[i]

        index_for_fix = -1

        for i in range(HamingCode.r):
            index = 2 ** i
            if bits_for_check[index - 1] != bits[index - 1]:
                index_for_fix += index

        if index_for_fix != -1:
            bits[index_for_fix] ^= 1

        for i in range(HamingCode.r - 1, -1, -1):
            bits.pop(2 ** i - 1)
        return bits


def main():

    x = [1,0,1,0]
    print(f'Эталонный код: {HamingCode.encode_block(x)}')
    for i in range(7):

        enc = HamingCode.encode_block(x)
        enc[i] = enc[i] ^ 1
        dec = HamingCode.decode_block(enc)
        print(enc, x == dec)


    HamingCode.r = 4

    x = [1,1,0,1,1,1,1]
    print(f'Эталонный код: {HamingCode.encode_block(x)}')
    for i in range(11):
        enc = HamingCode.encode_block(x)
        enc[i] = enc[i] ^ 1
        dec = HamingCode.decode_block(enc)
        print(enc, x == dec)


if __name__ == "__main__":
    main()
