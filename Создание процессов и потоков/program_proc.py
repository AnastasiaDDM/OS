import os
import subprocess
import sys
from sys import platform
from subprocess import call
import time
from sys import platform
import datetime
import journal

# timer = 0

# Хэш переданных аргументов
dic_argv = dict.fromkeys(['-t'],60)
dic_argv['-pr'] = 10

# Файл-журнал для логов
file_log = "logs_process.txt"


# Ф-ия таймера
def timer_func():
    while True:
        time.sleep(int(dic_argv.get('-t')))
        index_env()


# Для проверки строки, поиска соответсвия параметрам и запись в журнал.
def check_write_process():

    global file_log

    # Массив строк процессов
    fr = list()

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

            # Заполнение массива fr
            fr.append(line)

    # Получение значения ключа -list
    line_list_argv = dic_argv.get('-list')

    # Проверка наличия такого ключа
    if line_list_argv != None:

        # Сплит строки по запятым - получаем массив элементов запрашиваемых процессов
        array_list_argv = line_list_argv.split(',')

    # Получение значения ключа -pr
    priority = dic_argv.get('-pr')

    # Здесь берется один элемент из массива fr
    for line in fr:

        # Дополнительная проверка длины строки
        if len(line) > 2:

            # Сплит строки по запятым - получаем массив элементов одного процесса
            array = line.split(',')

            if int(array[3]):

                # Проверка наличия аргументов названий процессов для поиска (-list)
                if line_list_argv != None:

                    # Цикл проходит по всем заданным названиям процессов (-list)
                    for process_argv in array_list_argv:

                        # Сравнение имен процессов и заданного приоритета с текущим
                        if str(array[2]) == process_argv and int(array[3]) > int(priority):

                            # Составление строки, которая будет записана в журнал
                            line_for_file = str(datetime.datetime.now())+ "    ID: "+array[4]+", Name: "+array[2]+", Priority: "+array[3]+", WorkingSetSize: "+array[6]

                            # Вызов ф-ии записи в файл-журнал
                            journal.log_journal(file_log, line_for_file)
                           # os.system("taskkill /f " + array[2])
                            break

                else:

                    # Сравнение заданного приоритета и текущего
                    if int(array[3]) > int(priority):

                        # Составление строки, которая будет записана в журнал
                        line_for_file = str(datetime.datetime.now()) + "    ID: " + array[4] + ", Name: " + array[
                            2] + ", Priority: " + array[3] + ", WorkingSetSize: " + array[6]

                        # Вызов ф-ии записи в файл-журнал
                        journal.log_journal(file_log, line_for_file)
                        # os.system("taskkill /f " + array[2])



# Основная ф-ия входа (обработка аргументов, вызов рабочей ф-ии).
def index_env():

    global dic_argv

    if len(sys.argv) > -2:

        # Проход по всем переданным аргументам(кроме 0 - это путь до исполняемого файла)
        for i in range(1, len(sys.argv)):

            # Сплит аргумента
            one_arg = format(sys.argv[i]).split(':')

            # Добавление элемента в хэш агрументов
            dic_argv[one_arg[0]] = one_arg[1]


        # print ("Вы ввели приоритет {}!".format(sys.argv[2]))
        # timer = int(format(sys.argv[1]))
        # priority = format(sys.argv[2])
        #  print (format(sys.argv[2]))

        if platform == "linux" or platform == "linux2":
    # Запускаем батник. он просто записывает переменные окружения в файл.
    #         bash_func = subprocess.call(['/bin/bash', 'env_bash.bash'])
            # Тут я типа выполняю действия только после того, как батник отработал.
    # if bash_func.wait() == 0:
            check_write_process()
        else:
            # bat_func = subprocess.Popen('proc_bat.bat')

            # Тут я типа выполняю действия только после того, как батник отработал.
            # if bat_func.wait()==0:

            check_write_process()

    else:
        print ("Введите параметры для поиска")

    # Вызов ф-ии таймера
    timer_func()

index_env()

