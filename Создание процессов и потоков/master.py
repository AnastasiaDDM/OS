from threading import Thread
import os
import os.path
import subprocess
import sys
import time
import journal
import re

# Хэш аргументов по умолчанию (когда пользователь ничего не ввел)

# Таймер по которому срабатывает этот слейв
dic_argv = dict.fromkeys(['-t'], 10)

# Приоритет (поиск тех процессов, чей проиритет больше заданного)
dic_argv['-pr'] = 8

# Режим поиска (0-точное вхождение)
dic_argv['-mode'] = 0

# Параметр для поиска (по умолчанию - user)
dic_argv['-par'] = 'path'

# Файл-журнал для логов
file_log = "logs_journal.txt"


# Ф-ия таймера
def timer_func():

    while True:
        time.sleep(int(dic_argv['-t']))
        check()


# Ф-ия составления строки и вызов ф-ии записи в журнал
def log_master():

    # Составление строки, которая будет записана в журнал
    line_for_file = "Файл stop.txt появился на рабочем столе!"

    # Вызов ф-ии записи в файл-журнал
    journal.log_journal(file_log, line_for_file)


# Вызов 1 программы с параметрами
def slave_proc():

    slave_proc = subprocess.Popen(['python.exe', 'program_proc.py', '-t:' + str(dic_argv['-t']), '-pr:' + str(dic_argv['-pr'])])


# Вызов 2 программы с параметрами
def slave_env():

    slave_env = subprocess.Popen(['python.exe', 'program_env.py', '-t:' + str(dic_argv['-t']), '-par:' + str(dic_argv['-par']), '-mode:' + str(dic_argv['-mode'])])


# Основная ф-ия входа.
def index():

    global dic_argv

    if len(sys.argv) > 1:

        # Проход по всем переданным аргументам(кроме 0 - это путь до исполняемого файла)
        for i in range(1, len(sys.argv)):

            try:
                # Сплит аргумента
                one_arg = format(sys.argv[i]).split(':')
                # Добавление элемента в хэш агрументов
                dic_argv[one_arg[0]] = one_arg[1]

            # Обрабатывает исключение, при котором в аргументе нет ':'
            except:
                print("Аргумент " + format(sys.argv[i]) + " введен некорректно, данный параметр будет проигнорирован")

        # Проверка валидности значения таймера
        if re.match(r'\d+', dic_argv['-t']) is None:

            dic_argv['-t'] = 10
            print("Значение для таймера(-t) должно быть числом, данный параметр будет проигнорирован. Установлен -t:" + str(dic_argv['-t']))

        # Проверка валидности значения приоритета
        if re.match(r'\d+', dic_argv['-pr']) is None:

            dic_argv['-pr'] = 8
            print("Значение для приоритета(-pr) должно быть числом, данный параметр будет проигнорирован. Установлен -pr:" + str(dic_argv['-pr']))

        # Проверка валидности значения списка процессов (скорее всего не имеет смысла)
        if dic_argv['-list']:

            if re.match(r'[\S^,]+([\S^,]+(,))*', dic_argv['-list']) is None:
                print("Значение для списка процессов(-list) должно выглядет так: -list:pr1.exe,pr2.exe , данный параметр будет проигнорирован.")

        # Инициализация двух потоков для слейвов
        thread_proc = Thread(target=slave_proc)
        thread_env = Thread(target=slave_env)

        # Создание двух потоков для слейвов
        thread_proc.start()
        thread_env.start()

        # Проверка работы слейвов
        # if thread1.wait() != 0:
        #     thread1.start()

        # if thread2.wait() != 0:
        #     thread2.start()

        thread_proc.join()
        thread_env.join()

        timer_func()


# Ф-ия проверки создания файла stop на рабочем столе
def check():

    if os.path.isfile('C:/Users/79016/Desktop/stop.txt'):
        print("Файл существует")

        # Создание записи в журнале мастера и выход из программы
        log_master()
        sys.exit()

    else:
        print("Файл не существует")


index()