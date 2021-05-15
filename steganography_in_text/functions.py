def various_items_in_lists(first, second):
    if len(first) != len(second):
        return True
    for i in first:
        if i not in second:
            return True
    return False


class Functions:
    def chr_check(self, a, b, flag=1):
        if type(b) != int:
            b = ord(b)
        # защита от выхода за края + шифр Цезаря
        if type(a) != int:
            a = ord(a)
        a = a + (b * flag)
        if a > 1114111:
            return a % 1114112
        elif a < 0:
            return a % 1114112
        return a

    def crete_key(self, password=0, arr=None):
        normal_arr = ["‌", "‍", "⁡", "⁣", "⁢", "⁤"]
        if arr is None or various_items_in_lists(arr, normal_arr):
            arr = normal_arr
        return_arr = []
        if type(password) == int:
            num = password
        else:
            num = 0
            for i in password:
                num += ord(i)
        for i in range(6, 0, -1):
            return_arr.append(arr[num % i])
            arr.remove(arr[num % i])
            num = num // i
        return return_arr

    def password_check(self, secret, key):
        # увеличение длины ключа до длины доп сообщения
        password = key
        if len(key) > len(secret):
            password = key[:len(secret)]
        elif len(secret) > len(key):
            password = key * (int((len(secret) - len(key)) / len(key)) + 1)
        num = 0
        while len(secret) > len(password):
            password = password + key[num]
            num += 1
        return password

    def crypt_first(self, word):
        # перетасовка текста
        variable_1 = ''
        variable_2 = ''
        for i in range(len(word)):
            if i % 2 == 0:
                variable_1 += word[i]
            else:
                variable_2 += word[i]
        return variable_1 + variable_2

    def decrypt_first(self, word):
        # перетасовка текста обратно
        txt = ''
        if len(word) % 2 == 0:
            for i in range(len(word) // 2):
                txt += word[i]
                txt += word[len(word) // 2 + i]
        else:
            for i in range(len(word) // 2):
                txt += word[i]
                txt += word[len(word) // 2 + i + 1]
            txt += word[len(word) // 2]
        return txt

    def crypt_second(self, word, num=0, flag=1, step=1):
        # num первое значение изменения
        # flag 1 шифровка, -1 расшифровка
        # step шаг шифровки
        # модифицированный шифр Цезаря
        num = num * flag
        txt = ''
        for i in word:
            num += step * flag
            txt += chr(self.chr_check(i, num))
        return txt

    def return_el(self, sms, arr):
        # необходимо для расшифровки невидимых символов
        n, x = 0, 1
        for i in sms:
            n += arr[i] * x
            x = x * 5
        return chr(self.chr_check(n, 0))

    def coding_invisible(self, txt, arr):
        # перевод шифра в невидимые символы
        x = arr[5]
        for i in txt:
            y = ord(i)
            while y != 0:
                z = y % 5
                x += arr[z]
                y = y // 5
            x += arr[5]
        return x

    def decoding_invisible(self, massage, arr):
        # перевод невидимых символов в шифр
        keys = {}
        for i in range(5):
            keys[f'{arr[i]}'] = i
        words = massage.split(arr[5])
        txt = ''
        for i in words:
            txt += self.return_el(i, keys)
        return txt
