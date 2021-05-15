from keyboa import button_maker, keyboa_maker


def check_type(sms, txt):
    # подфункция для проверки выбора в данных кнпки
    if txt in sms[0: len(txt)]:
        return True
    return False


def return_keyboard(arr_1, flag=""):
    arr_2 = []
    for i in arr_1:
        if type(i[0]) == list:
            arr_2.append(return_keyboard(i, flag))
        else:
            arr_2.append(button_maker(button_data={i[0]: flag + i[1]}))
    return arr_2


def create_keyboard(arr, flag=''):
    # генерация кнопок из списка типа [['txt', 'id']....]
    return keyboa_maker(return_keyboard(arr, flag))


def deploy_arr(arr, row=2, second_arr=[]):
    # пересборка списка элемнтов в предсписок для генерации кнопок
    if not arr:
        arr = ['444']
    new_arr = []
    buffer_arr = []
    n = 0
    for i in arr:
        if i not in second_arr:
            if len(buffer_arr) == row:
                new_arr.append(buffer_arr)
                buffer_arr = []
            buffer_arr.append([str(i), str(n)])
        n += 1
    if buffer_arr:
        new_arr.append(buffer_arr)
    return new_arr
