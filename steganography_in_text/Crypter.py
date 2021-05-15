from . import Functions

functions = Functions()


class Crypter:
    def __init__(self, int_seed=0):
        self.seed = int_seed
        self.crypt_keys = functions.crete_key(int_seed)
        self.range = int_seed % 10 + 1

    def change_seed(self, new_int_seed):
        self.seed = new_int_seed
        self.crypt_keys = functions.crete_key(new_int_seed)
        self.range = new_int_seed % 10 + 1

    def create_message(self, sms='', password='1', secret='нет зашифрованного текста'):
        if not password:
            password = ' '
        crypt_keys = functions.crete_key(password, self.crypt_keys)
        password = functions.password_check(secret, password)
        message = ''
        for i in range(len(secret)):
            message += chr(functions.chr_check(secret[i], password[i]))
        message = functions.crypt_first(message)
        message = functions.crypt_second(message, step=self.range)
        message = functions.coding_invisible(message, crypt_keys)
        if len(sms) >= 2:
            return sms[0:len(sms) // 2] + message + sms[len(sms) // 2::]
        return sms + message
