import numpy as np
from functools import reduce


class IterCode:

    k: int = 40
    k1: int
    k2: int
    z: int
    g: int # group of paritets

    def __init__(self, k1: int, k2: int, g: int, z: int = 1):
        self.k1 = k1
        self.k2 = k2
        self.z = z
        self.g = g

        if self.g > 5:
            raise  Exception("g is invalid")

    def decode(self, bits: list):
        h = 0
        v = 0
        z_a = 0

        if self.g >= 3:
            z_a = 1
        if self.g >= 4:
            h = 1
        if self.g == 5:
            v = 1
        if len(bits) != (self.z + z_a) * (self.k1 + 1 + v) * (self.k2 + 1 + h):
            raise  Exception("Size is invalid")

        input = np.reshape(np.array(bits, dtype='int8'), (self.z + z_a, self.k1 + 1 + v, self.k2 + 1 + h))

        data = input[: self.z, v: v + self.k1, h: h + self.k2]
        data = np.reshape(data, data.size).tolist()

        result = np.reshape(np.array(self.encode(data), dtype='int8'), (self.z + z_a, self.k1 + 1 + v, self.k2 + 1 + h))

        delta = np.abs(input - result)
        m_fix = np.zeros_like(input)


        for i in range(self.g):
            if self.g >= 3:
                match i:
                    case 0:
                        m_fix += delta[self.z]
                    case 1:
                        m_fix[0:self.z, v: v + self.k1, h: h + self.k2] += delta[: self.z, v: v + self.k1, h + self.k2:]
                    case 2:
                        m_fix[0:self.z, v: v + self.k1, h: h + self.k2] += delta[: self.z, v + self.k1:, h: h + self.k2]
                    case 3:
                        for j in range(0, self.z):
                            for k in range(self.k1):
                                for l in range(self.k2):
                                    m_fix[j, v + (k + l) % self.k1, h + (self.k2 - 1 - l) % self.k2] += delta[
                                        j, k + 1, 0]
                    case 4:
                        for j in range(0, self.z):
                            for k in range(self.k2):
                                for l in range(self.k1):
                                    m_fix[j, v + l % self.k1, h + (k + l) % self.k2] += delta[j, 0, k + 1]
            else:
                match i:
                    case 0:
                        m_fix[0:self.z, v: v + self.k1, h: h + self.k2] += delta[: self.z, v: v + self.k1, h + self.k2:]
                    case 1:
                        m_fix[0:self.z, v: v + self.k1, h: h + self.k2] += delta[: self.z, v + self.k1:, h: h + self.k2]

        max_val = np.max(m_fix)
        mask = (m_fix == max_val)
        input[mask] ^= 1

        data = input[: self.z, v: v + self.k1, h: h + self.k2]
        data = np.reshape(data, data.size).tolist()
        return data

    def encode(self, bits: list):
        if len(bits) != self.k:
            raise  Exception("Size is invalid")

        h = 0
        v = 0
        z_a = 0

        if self.g >= 3:
            z_a = 1

        if self.g >= 4:
            h = 1
        if self.g == 5:
            v = 1

        result = np.zeros((self.z + z_a, self.k1 + 1 + v, self.k2 + 1 + h), dtype='int8')

        data = np.array(bits, dtype='int8')
        data = np.reshape(data, (self.z, self.k1, self.k2))

        result[: self.z, v: v + self.k1, h: h + self.k2] = data


        for i in range(self.g):

            if self.g >= 3:
                match i:
                    case 0:
                        for j in range(0, self.z):
                            result[self.z] ^= result[j]
                    case 1:
                        for j in range(self.k2 - 1):
                            result[0: self.z, v: v + self.k1, h + self.k2:] ^= result[0: self.z, v: v +self.k1, j: j + 1]
                    case 2:
                        for j in range(self.k1 - 1):
                            result[0: self.z, v + self.k1:, h: h + self.k2] ^= result[0: self.z, j: j + 1, h: h + self.k2]
                    case 3:
                        for j in range(0, self.z):
                            layer = result[j, v: v+self.k1, h: h + self.k2]
                            for k in range(self.k1):
                                arr = np.array([layer[(k + l) % self.k1, (self.k2 - 1 - l) % self.k2] for l in range(self.k2)])
                                result[j, k + 1, 0] = reduce(np.bitwise_xor, arr)
                    case 4:
                        for j in range(0, self.z):
                            layer = result[j, v: v + self.k1, h: h + self.k2]
                            for k in range(self.k2):
                                arr = np.array([layer[l % self.k1, (k + l) % self.k2 ] for l in range(self.k1)])
                                result[j, 0, k + 1] = reduce(np.bitwise_xor, arr)
            else:
                match i:
                    case 0:
                        for j in range(self.k2 - 1):
                            result[0: self.z, 0: self.k1, self.k2: ] ^= result[0: self.z, 0: self.k1, j: j+1]
                    case 1:
                        for j in range(self.k1 - 1):
                            result[0: self.z, self.k1:, 0: self.k2] ^= result[0: self.z, j: j + 1, 0: self.k2]

        control_bit = reduce(np.bitwise_xor, np.reshape(result, result.size))
        result[-1, -1, -1] = control_bit
        return np.reshape(result, result.size).tolist()


def main():
    codec = IterCode(2, 4, 5, z=5)
    arg = [1 if (i % 3) <= 1 else 0  for i in range(40)]
    enc = codec.encode(arg)

    enc[8 + 3] ^= 1
    enc[8 + 30] ^= 1
    enc[8 + 20] ^= 1
    enc[35] ^= 1
    enc[20] ^= 1

    dec = codec.decode(enc)
    print(f'Конфигурация: k_1={codec.k1}, k_2={codec.k2}, z={codec.z}, кол-во паритетов={codec.g}')
    print(f'{{"Входные данные:":30s       }}', *arg)
    print(f'{{"Восстановленне данные:":30s}}',*dec)


if __name__ == "__main__":
    main()