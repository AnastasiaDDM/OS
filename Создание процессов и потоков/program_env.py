import subprocess
import sys
from sys import platform
import time
import journal
import os

# Хэш переданных аргументов

# Таймер по которому срабатывает этот слейв
dic_argv = dict.fromkeys(['-t'], 10)

# Режим поиска (0-точное вхождение)
dic_argv['-mode'] = 0

# Параметр для поиска (по умолчанию - user)
dic_argv['-par'] = 'path'

# Файл-журнал для логов
file_log = "/logs_environ.txt"

pth = os.path.dirname(os.path.realpath(__file__))


# Ф-ия таймера
def timer_func():
    while True:
        time.sleep(int(dic_argv.get('-t')))
        index_env()


# Ф-ия составления строки и вызов ф-ии записи в журнал
def log_env(dic_env, name):

    # Составление строки, которая будет записана в журнал
    line_for_file = "Name: " + str(name) + ", Value: " + str(dic_env[name])

    # Вызов ф-ии записи в файл-журнал
    journal.log_journal((str(pth)) + file_log, line_for_file)


# Ф-ия составления хэша переменных
def get_list_env(fr):

    # Хэш переменных окружения
    dic_env = {}

    # Вырезание всех пустых строк (знаков переноса строки, перевода каретки)
    array_file = fr.split('\n')

    # Цикл по каждому элементу массива array_file (элемент = строка переменной)
    for line in array_file:

        # Проверка длины строки
        if len(line) > 5:

            # Сплит строки по '=' по первому вхождению - получаем массив элементов одной переменной
            array = line.split('=', 1)

            if array[0] != "" and array[1] != "":

                # Добавления элемента в хэш переменных
                dic_env[array[0]] = array[1]

    return dic_env


# Для проверки строки и поиска соответсвия параметру .
def check_write_env(dic_env):

    # Получение значения ключа -pr
    param = dic_argv.get('-par')

    # Получение значения ключа -mode
    mode = dic_argv.get('-mode')

    # Цикл по всем ключам хэша переменных
    for name in dic_env.keys():

        # Режим не 0 - т.е. проверка любых вхождений
        if mode != 0:

            if str(name).upper().find(str(param).upper()) > -1 or dic_env.get(name).upper().find(str(param).upper()) > -1:

                # Ф-ия составление строки
                log_env(dic_env, name)
        else:
            if str(name).upper() == str(param).upper() or dic_env.get(name).upper() == str(param).upper():

                # Ф-ия составление строки
                log_env(dic_env, name)


# Основная ф-ия входа (обработка аргументов, вызов рабочей ф-ии).
def index_env():

    global dic_argv

    if len(sys.argv) > 0:

        # Проход по всем переданным аргументам(кроме 0 - это путь до исполняемого файла)
        for i in range(1, len(sys.argv)):

            # Сплит аргумента
            one_arg = format(sys.argv[i]).split(':')

            # Добавление элемента в хэш агрументов
            dic_argv[one_arg[0]] = one_arg[1]

        if platform == "linux" or platform == "linux2":

            str_file_env = (str(pth)) + '/env.txt'

            # Запускаем батник. он просто записывает переменные окружения в файл.
            bash_func = subprocess.call(['/bin/bash', (str(pth)) + '/env_bash.bash', str_file_env])

            # Открытие файла, где записались из батника переменные окр.
            with open(str_file_env) as file:
                fr = file.read()

            # Вызов ф-ии преобразования данных в хэш
            dic_env = get_list_env(fr)

            # Ф-ия работы с хэшем переменных
            check_write_env(dic_env)

        else:
            bat_func = subprocess.Popen([(str(pth)) + '\env_bat.bat ', str(pth)])

            # Проверка завершения работы батника
            if bat_func.wait() == 0:

                # Открытие файла, где записались из батника переменные окр.
                with open(str(pth)+"\env.txt") as file:
                    fr = file.read()

                # Вызов ф-ии преобразования данных в хэш
                dic_env = get_list_env(fr)

                # Ф-ия работы с хэшем переменных
                check_write_env(dic_env)
        # Вызов ф-ии таймера
        timer_func()


index_env()


