from threading import Thread
import os
import os.path
import subprocess
import sys
from sys import platform
import datetime
import contextlib
import time




priority = ""
param = ""
mode = 0
timer = 5

# // ф-ия для записи строк в файл-журнал.
def log_journal():
    file = open('master_logs.txt', 'a+', encoding='utf-8')
    now = datetime.datetime.now()
    file.write(str(now))
    file.write("\n")
    file.close()


# Вызов 1 программы с параметрами
def slave_1(priority, timer):
    slave_1 = subprocess.Popen(['python.exe', 'program_proc.py', timer, priority])
    print ("SSS")

# Вызов 2 программы с параметрами
def slave_2(param, mode, timer):
    print (param)
    print (mode)
    if mode != 0:
        slave_2 = subprocess.Popen(['python.exe', 'program_env.py', timer, param, mode])
    else:
        slave_2 = subprocess.Popen(['python.exe', 'program_env.py', timer, param])



# Основная ф-ия входа.
def index():
    global priority
    global param
    global mode
    global timer


    # Присваивание значений пременных
    if len(sys.argv) > 3:

        print ("Время сна {}!".format(sys.argv[1]))
        timer = format(sys.argv[1])

        print ("Вы ввели приоритет {}!".format(sys.argv[2]))
        priority = format(sys.argv[2])

        print ("Вы ввели процесс {}!".format(sys.argv[3]))
        param = format(sys.argv[3])
        print (param)

        if len(sys.argv) > 4:
            mode = format(sys.argv[4])

        # Инициализация двух потоков для слейвов
        thread1 = Thread(target=slave_1, args=(priority, timer))
        thread2 = Thread(target=slave_2, args=(param, mode, timer))

        # Здесь я пытаюсь создать еще один поток для таймера проверки файла стоп на раб.столе
        thread_timer = Thread(target=timer_check, args=())

        # Создание двух потоков для слейвов
        thread1.start()
        thread2.start()
        thread_timer.start()

        # Проверка работы слейвов
        if thread1.wait() != 0:
            thread1.start()

        if thread2.wait() != 0:
            thread2.start()

        thread1.join()
        thread2.join()
        thread_timer.join()

        timer_check()

    else:
        print ("Введите параметры для поиска: 1 параметр - время сна; 2 параметр - приоритет; 3, [4] - искомый процесс, [тип поиска]")


# Ф-ия проверки создания файла stop на рабочем столе
def check():


    if os.path.isfile('C:/Users/79016/Desktop/stop.txt'):
        print ("Файл существует")

        # Создание записи в журнале мастера и выход из программы
        log_journal()
        #with contextlib.closing(Closeable()):
        sys.exit()

    else:
        print ("Файл не существует")

def timer_check():
    while True:

        time.sleep(timer) # in seconds
        check()



index()