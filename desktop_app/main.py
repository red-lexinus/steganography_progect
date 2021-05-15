import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from steganography_in_text import Crypter, Decrypter
import pyperclip

crypt = Crypter()
decrypt = Decrypter()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('app.ui', self)  # Загружаем дизайн
        self.copy.clicked.connect(self.copy_new_message)
        self.copy_2.clicked.connect(self.copy_secret)
        self.create_sms.clicked.connect(self.crypt_message)
        self.create_sms_2.clicked.connect(self.decrypt_message)

    def crypt_message(self):
        txt_1, txt_2, txt_3 = self.sms.toPlainText(), self.password.toPlainText(), self.secret.toPlainText()
        if not txt_2:
            self.result.setPlainText('вы не ввели пароль')
        elif not txt_3:
            self.result.setPlainText('вы не ввели секретное сообщение')
        else:
            self.result.setPlainText(crypt.create_message(txt_1, txt_2, txt_3))

    def decrypt_message(self):
        txt_1, txt_2 = self.sms_2.toPlainText(), self.password_2.toPlainText()
        if not txt_2:
            self.result_2.setPlainText('вы не ввели пароль')
        elif not txt_1:
            self.result_2.setPlainText('вы не ввели секретное сообщение')
        else:
            try:
                self.result_2.setPlainText(decrypt.create_message(txt_1, txt_2))
            except ValueError:
                self.result_2.setPlainText('не удалось расшифровать сообщение')

    def copy_secret(self):
        pyperclip.copy(self.result_2.toPlainText())
        pyperclip.paste()

    def copy_new_message(self):
        pyperclip.copy(self.result.toPlainText())
        pyperclip.paste()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
