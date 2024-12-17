class ExtendedHammingCode:
    def __init__(self, message):
        if len(message) != 7:
            raise ValueError("Длина сообщения должна быть ровно 7 бит.")
        self.message = message
        self.n = 12  # Полная длина закодированного слова: 7 информационных битов + 4 проверочных + 1 бит четности
        self.code = [0] * self.n

    def encode(self):
        # Устанавливаем информационные биты в кодовом слове
        j = 0
        for i in range(1, self.n):
            if (i & (i - 1)) != 0:  # Проверяем, что позиция не является степенью 2 (1, 2, 4, 8)
                self.code[i - 1] = int(self.message[j])
                j += 1

        # Вычисляем проверочные биты
        for i in range(4):
            pos = 1 << i  # Позиции проверочных битов: 1, 2, 4, 8
            parity = 0
            for j in range(1, self.n):
                if j & pos:
                    parity ^= self.code[j - 1]
            self.code[pos - 1] = parity

        # Вычисляем общий бит четности
        self.code[-1] = sum(self.code[:-1]) % 2
        print("Сформированный код:", ''.join(map(str, self.code)))
        return self.code

    def introduce_errors(self, positions):
        # Внесение ошибок на указанные позиции
        for pos in positions:
            if 1 <= pos <= self.n:
                self.code[pos - 1] ^= 1
        print("Код с ошибками на позициях", positions, ":", ''.join(map(str, self.code)))

    def detect_and_correct(self):
        # Проверяем позиции проверочных битов для обнаружения ошибки
        error_position = 0
        for i in range(4):
            pos = 1 << i
            parity = 0
            for j in range(1, self.n):
                if j & pos:
                    parity ^= self.code[j - 1]
            if parity != 0:
                error_position += pos

        # Проверка общего бита четности
        parity_check = sum(self.code) % 2

        # Интерпретация результатов
        if error_position == 0 and parity_check == 0:
            print("Ошибок не обнаружено.")
        elif error_position != 0 and parity_check == 1:
            print("Обнаружена одиночная ошибка в позиции:", error_position)
            self.code[error_position - 1] ^= 1
            print("Исправленный код:", ''.join(map(str, self.code)))
        elif error_position != 0 and parity_check == 0:
            print("Обнаружена двойная ошибка. Исправление невозможно.")
        else:
            print("Обнаружена ошибка в бите четности. Исправление невозможно.")

    def decode(self):
        # Извлекаем только информационные биты
        decoded_message = []
        for i in range(1, self.n):
            if (i & (i - 1)) != 0:  # Информационные биты (позиции не являются степенями двойки)
                decoded_message.append(str(self.code[i - 1]))
        decoded_message = ''.join(decoded_message)
        print("Расшифрованное сообщение:", decoded_message)
        return decoded_message


# Пример использования
message = "1101001"  # Исходное сообщение длиной 7 бит
hamming = ExtendedHammingCode(message)
encoded_code = hamming.encode()  # Кодирование
hamming.introduce_errors([3,5])  # Внесение одиночной ошибки на позиции 3
hamming.detect_and_correct()  # Обнаружение и исправление ошибки
decoded_message = hamming.decode()  # Расшифровка исходного сообщения
