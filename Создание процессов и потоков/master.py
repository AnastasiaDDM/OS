from threading import Thread
import os
import os.path
import subprocess
import sys
import time
import journal
import re
import winreg

# Адрес текущей директории
pth = os.path.dirname(os.path.realpath(__file__))

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
file_log = "\logs_journal.txt"


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
    journal.log_journal((str(pth)) + file_log, line_for_file)


# Ф-ия добавления файла master в реестр автозагрузки
def add_master_reg(key, name_reg, address):

    try:

        # Получения значения в реестре элемента с именем name_reg
        software = winreg.QueryValueEx(key, name_reg)
    except:

        # Установить программу "master" в автозагрузку
        winreg.SetValueEx(key, name_reg, 0, winreg.REG_SZ, address)


# Ф-ия удаления файла master из реестра автозагрузки
def del_master_reg(key, name_reg):

    try:

        # Получения значения в реестре элемента с именем name_reg
        software = winreg.QueryValueEx(key, name_reg)

        # Удалить программу "master" из автозагрузки
        winreg.DeleteValue(key, name_reg)
    except:
        pass


# Ф-ия отктытия ключа реестра
def open_key_reg(autoload):

    # Имя файла master, который нужно удалить из автозагрузки реестра
    s_name = "\master.py"

    # Имя в реестре прогаммы автозапуска - master
    name_reg = "master"

    # Соединяет адрес Python.exe и исполняемого текущего файла
    address = '"' + sys.executable + '" ' + '"' + (str(pth)) + s_name + '"'

    # Путь в реестре, открытие ключа
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0,
                         winreg.KEY_ALL_ACCESS)

    if autoload == '1':

        # Добавление мастера в автозагрузку
        add_master_reg(key, name_reg, address)

    elif autoload == '0':

        # Удаление мастера из автозагрузки
        del_master_reg(key, name_reg)

    # Закрыть реестр
    winreg.CloseKey(key)


# Вызов 1 программы с параметрами
def slave_proc():

    slave_proc = subprocess.Popen(['python.exe', (str(pth)) + '\program_proc.py', '-t:' + str(dic_argv['-t']), '-pr:' + str(dic_argv['-pr'])])


# Вызов 2 программы с параметрами
def slave_env():

    slave_env = subprocess.Popen(['python.exe', (str(pth)) + '\program_env.py', '-t:' + str(dic_argv['-t']), '-par:' + str(dic_argv['-par']), '-mode:' + str(dic_argv['-mode'])])


# Основная ф-ия входа.
def index():

    global dic_argv

    if len(sys.argv) > 0:

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
        if re.match(r'\d+', str(dic_argv['-t'])) is None:

            dic_argv['-t'] = 10
            print("Значение для таймера(-t) должно быть числом, данный параметр будет проигнорирован. Установлен -t:" + str(dic_argv['-t']))

        # Проверка валидности значения приоритета
        if re.match(r'\d+', str(dic_argv['-pr'])) is None:

            dic_argv['-pr'] = 8
            print("Значение для приоритета(-pr) должно быть числом, данный параметр будет проигнорирован. Установлен -pr:" + str(dic_argv['-pr']))

        # Проверка валидности значения списка процессов (скорее всего не имеет смысла)
        # if dic_argv['-list']:
        #
        #     if re.match(r'[\S^,]+([\S^,]+(,))*', dic_argv['-list']) is None:
        #         print("Значение для списка процессов(-list) должно выглядет так: -list:pr1.exe,pr2.exe , данный параметр будет проигнорирован.")

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

        # Проверка наличия ключа -a
        autoload = dic_argv.get('-a')

        # Проверка наличия такого ключа
        if autoload is not None:

            # Ф-ия открытия ключа реестра
            open_key_reg(autoload)

        # Ф-ия запуска таймера для мастера
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