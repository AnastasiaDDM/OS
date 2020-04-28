import os
import subprocess
import sys
from sys import platform
from subprocess import call
import time

param = ""
mode = 0
timer = 0


# // ф-ия для записи строк в файл-журнал.
def log_journal(string):
    file = open('logs.txt', 'a+', encoding='utf-8')
    file.write(string)
    file.write("\n")
    file.close()

# Для проверки строки и поиска соответсвия параметру .
def dict_env():
# //Открытие файла, где записались из батника переменные окр.
    with open("env.txt") as file:
        fr = file.read()
        #   print("QQQQQ"+fr)

# Это место я миллиард раз переделывала. Здесь берется одна строка из переменной (которая как файл)
    for line in fr.split('\n'):
        if line != "":
            array = line.split('=')
            #     print (array[0] + array[1] + "mmmmmmmmmmmmmmmmmmmmmmmmm")

            if array[0]!= "" and array[1]!= "":
                if mode != 0:
                    if array[0].upper().find(param.upper())> -1 or array[1].upper().find(param.upper())> -1:
                        print (array[0]+"AAAAAAAAAAAAAAA")
                        #       print (param)
                        # Тут я вызываю ф-ю. записи в журнал.
                        log_journal(line)
                else:
                    if array[0].upper() == param.upper() or array[1].upper() == param.upper():
                        #      print (array[0]+"AAAAAAAAAAAAAAA")
                        #      print (param)
                        # Тут я вызываю ф-ю. записи в журнал.
                        log_journal(line)


# Основная ф-ия входа. 
def log_env():
    global param
    global timer
    #   print (format(sys.argv))
    if len(sys.argv) > 2:
        timer = int(format(sys.argv[1]))
        print ("Вы ввели, {}!".format(sys.argv[2]))
        param = format(sys.argv[2])
        #      print (format(sys.argv[2]))

        if len(sys.argv) > 3:
            global mode
            mode = format(sys.argv[3])

        if platform == "linux" or platform == "linux2":
    # Запускаем батник. он просто записывает переменные окружения в файл.
            bash_func = subprocess.call(['/bin/bash', 'env_bash.bash'])
            # Тут я типа выполняю действия только после того, как батник отработал.
    # if bash_func.wait() == 0:
            dict_env()
        else:
            bat_func = subprocess.Popen('env_bat.bat')

            # Тут я типа выполняю действия только после того, как батник отработал.
            if bat_func.wait()==0:
                dict_env()


    else:
        print ("Введите параметры для поиска")



log_env()

while True:
    time.sleep(timer) # in seconds
    log_env()

