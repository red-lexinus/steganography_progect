from . import Functions

functions = Functions()


class Decrypter:
    def __init__(self, int_seed=0):
        self.seed = int_seed
        self.crypt_keys = functions.crete_key(int_seed)
        self.range = int_seed % 10 + 1

    def change_seed(self, new_int_seed):
        self.seed = new_int_seed
        self.crypt_keys = functions.crete_key(new_int_seed)
        self.range = new_int_seed % 10 + 1

    def create_message(self, txt='', password='1'):
        if not password:
            password = ' '
        crypt_keys = functions.crete_key(password, self.crypt_keys)
        elem = crypt_keys[5]
        txt = txt[txt.index(elem) + 1: txt.rindex(elem)]
        txt = functions.decoding_invisible(txt, crypt_keys)
        txt = functions.crypt_second(txt, flag=-1, step=self.range)
        txt = functions.decrypt_first(txt)
        message = ''
        password = functions.password_check(txt, password)
        for i in range(len(txt)):
            message += chr(functions.chr_check(txt[i], password[i], -1))
        return message
