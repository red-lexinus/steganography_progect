from .Decrypter import Decrypter
from .Crypter import Crypter
from .functions import Functions

functions = Functions()


def test_0():
    assert functions.chr_check(' ', ' ') == 64


def test_1():
    assert functions.chr_check(' ', 12) == 44


def test_2():
    assert functions.password_check('111', '12') == '121'


def test_3():
    assert functions.crypt_first('1234') == '1324'


def test_4():
    assert functions.decrypt_first(functions.crypt_first('12345')) == '12345'


def test_5():
    crypter = Crypter()
    decrypter = Decrypter()
    assert crypter.crypt_keys == decrypter.crypt_keys


def test_6():
    crypter = Crypter()
    decrypter = Decrypter()
    assert decrypter.create_message(crypter.create_message('привет', 'пароль', 'секрет'), 'пароль') == 'секрет'


for i in range(7):
    eval(f'test_{i}()')
