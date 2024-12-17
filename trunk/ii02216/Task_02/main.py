import numpy as np


class Code:
    def __init__(self, k1, k2, z, parity_groups):
        self.k1 = k1
        self.k2 = k2
        self.z = z
        self.parity_groups = parity_groups  #

    def encode(self, message):

        message_bits = np.array([int(bit) for bit in message])

        if len(message_bits) != 20:
            raise ValueError("Длина сообщения должна быть 20 бит.")

        parity_bits = []
        for group in self.parity_groups:
            parity = 0
            for i in range(0, len(message_bits), group):
                parity ^= message_bits[i:i + group].sum() % 2
            parity_bits.append(parity)

        coded_message = np.concatenate((message_bits, parity_bits))
        return coded_message

    def decode(self, received):

        message_bits = received[:20]
        received_parity_bits = received[20:]

        error_detected = False
        for i, group in enumerate(self.parity_groups):
            expected_parity = 0
            for j in range(0, len(message_bits), group):
                expected_parity ^= message_bits[j:j + group].sum() % 2

            if received_parity_bits[i] != expected_parity:
                error_detected = True
                print(f"Ошибка в группе паритета {i + 1}")

        if not error_detected:
            print("Ошибок не обнаружено.")
        else:
            print("Обнаружены ошибки в принятых данных.")

        return message_bits


k1 = 4
k2 = 2
z = 10
parity_groups = [2, 3, 4, 5]

codec = Code(k1, k2, z, parity_groups)

message = "11010111011101010101"

encoded_message = codec.encode(message)
print("Закодированное сообщение:", encoded_message)

received_message = np.copy(encoded_message)
received_message[3] = (received_message[3] + 1) % 2

decoded_message = codec.decode(received_message)
print("Декодированное сообщение:", decoded_message)
