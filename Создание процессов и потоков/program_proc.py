import subprocess
import sys
import time
from sys import platform
import journal
import re
import os

# Хэш переданных аргументов

# Таймер по которому срабатывает этот слейв
dic_argv = dict.fromkeys(['-t'], 10)

# Приоритет (поиск тех процессов, чей проиритет больше заданного)
dic_argv['-pr'] = 8

# Файл-журнал для логов
file_log = "\logs_process.txt"


pth = os.path.dirname(os.path.realpath(__file__))

# Ф-ия таймера
def timer_func():
    while True:
        time.sleep(int(dic_argv.get('-t')))
        index_env()


# Ф-ия составления строки и вызов ф-ии записи в журнал
def log_process(dic_process, p):

    # Составление строки, которая будет записана в журнал
    line_for_file = "ID: " + str(p) + ", Name: " + str(dic_process[p]['name']) + ", Priority: " + str(
        dic_process[p]['pr']) + ", WorkingSetSize: " + str(dic_process[p]['size'])

    # Вызов ф-ии записи в файл-журнал
    journal.log_journal((str(pth)) + file_log, line_for_file)


# Ф-ия составления хэша для ОС WIN
def get_list_process_win():

    # Хэш процессов
    dic_process = {}

    # Выполнение команды прочтения процессов и перенаправление вывода на канал переменной process
    process = subprocess.Popen('wmic process list brief /FORMAT:CSV',stdout=subprocess.PIPE)

    # Получение перенаправленного вывода из переменной process в output
    output = process.communicate()

    # Вырезание всех пустых строк (знаков переноса строки, перевода каретки)
    array_file = str(output[0]).split('\\r\\r\\n')

    # Строка заголовка параметров процесса (нужна для дальнейшего игнорированию эквивалентной строки
    str_title = str("Node,HandleCount,Name,Priority,ProcessId,ThreadCount,WorkingSetSize")

    # Цикл по каждому элементу массива array_file (элемент = строка процесса)
    for line in array_file:

        # Проверка длины строки и чтобы эта строка не совпадала с загаловком
        if len(line) > 5 and line != str_title:

            # Сплит строки по запятым - получаем массив элементов одного процесса
            array = line.split(',')

            # Составление хэша 2 уровня
            dic_process_param = {'name': array[2], 'pr': array[3], 'size': array[6]}

            # Добавления элемента в хэш процессов
            dic_process[array[4]] = dic_process_param

    return dic_process


# Ф-ия составления хэша для ОС UNIX
def get_list_process_lin():

    # Хэш процессов
    dic_process = {}

    # Выполнение команды прочтения процессов и перенаправление вывода на канал переменной process
    process = subprocess.Popen(['ps', '-la'], stdout=subprocess.PIPE)

    # Получение перенаправленного вывода из переменной process в output
    output = process.communicate()

    # Вырезание всех пустых строк (знаков переноса строки, перевода каретки)
    array_file = str(output[0]).split('\\n')

    # Строка заголовка параметров процесса (нужна для дальнейшего игнорированию эквивалентной строки
    str_title = str("b'F S   UID   PID  PPID  C PRI  NI ADDR SZ WCHAN  TTY          TIME CMD")

    # Цикл по каждому элементу массива array_file (элемент = строка процесса)
    for line in array_file:

        # Проверка длины строки и чтобы эта строка не совпадала с загаловком
        if len(line) > 5 and line != str_title:

            # Приведение строки в вид, где параметры разделены ',' , а не пробелами
            line = re.sub(r' +', ',', str(line))

            # Сплит строки по запятым - получаем массив элементов одного процесса
            array = line.split(',')

            # Составление хэша 2 уровня
            dic_process_param = {'name': array[13], 'pr': array[7], 'size': array[9]}

            # Добавления элемента в хэш процессов
            dic_process[array[3]] = dic_process_param

    return dic_process


# Для проверки строки, поиска соответсвия параметрам
def check_write_process(dic_process):

    # Получение значения ключа -list
    line_list_argv = dic_argv.get('-list')

    array_list_argv = ()

    # Проверка наличия такого ключа
    if line_list_argv is not None:

        try:
            # Сплит строки по запятым - получаем массив элементов запрашиваемых процессов
            array_list_argv = line_list_argv.split(',')
            print(array_list_argv)
        except:
            array_list_argv = line_list_argv
            pass

    # Получение значения ключа -pr
    priority = dic_argv.get('-pr')

    # Цикл по всем ключам хэша процессов
    for p in dic_process.keys():

        # Проверка наличия аргументов названий процессов для поиска (-list)
        if len(array_list_argv) != 0:

            # Цикл проходит по всем заданным названиям процессов (-list)
            for process_argv in array_list_argv:

                # Сравнение имен процессов и заданного приоритета с текущим
                if str(dic_process[p]['name']) == process_argv and int(dic_process[p]['pr']) > int(priority):

                    # Ф-ия составление строки
                    log_process(dic_process, p)

                    # Уничтожение процесса, удовлетворяющего условия
                    #os.kill(int(p), signal.SIGABRT)

                    break

        else:

            # Сравнение заданного приоритета и текущего
            if int(dic_process[p]['pr']) > int(priority):

                # Ф-ия составление строки
                log_process(dic_process, p)


# Основная ф-ия входа (обработка аргументов, вызов рабочей ф-ии).
def index_env():

    global dic_argv

    if len(sys.argv) > 1:

        # Проход по всем переданным аргументам(кроме 0 - это путь до исполняемого файла)
        for i in range(1, len(sys.argv)):

            try:
                # Сплит аргумента
                one_arg = format(sys.argv[i]).split(':')

                if one_arg[0] == "" or one_arg[1] == "":

                    print(format(sys.argv[i]) + " Данный параметр будет проигнорирован.")

                else:

                    # Добавление элемента в хэш агрументов
                    dic_argv[one_arg[0]] = one_arg[1]
            except:
                print(format(sys.argv[i]) + " Данный параметр будет проигнорирован.")


        if platform == "linux" or platform == "linux2":

            # Ф-ия работы с хэшем процессов
            dic_process = get_list_process_lin()

            # Ф-ия работы с хэшем процессов
            check_write_process(dic_process)
        else:

            # Ф-ия получения хэша процессов
            dic_process = get_list_process_win()

            # Ф-ия работы с хэшем процессов
            check_write_process(dic_process)

    # Вызов ф-ии таймера
    timer_func()


index_env()

