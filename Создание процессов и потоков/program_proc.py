import os
import subprocess
import sys
from sys import platform
from subprocess import call
import codecs
import time

priority = ""
timer = 0


# // ф-ия для записи строк в файл-журнал.
def log_journal(string):
    file = open('logs_proc.txt', 'a+')
    file.write(string)
    file.write("\n")
    file.close()


# Для проверки строки и поиска соответсвия параметру .
def dict_env():
# //Открытие файла, где записались из батника переменные окр.
    #with open("proc.txt") as file:
     #   fr = file.read()
       # print("QQQQQ"+fr)


    fr = list()

    with codecs.open('proc.txt', 'r', "utf-16") as f:
     #   fr = f.read().splitlines()
      #  fr.remove(0)
       # fr.remove(1)
        str_title = str("Node,HandleCount,Name,Priority,ProcessId,ThreadCount,WorkingSetSize")
       # str_title = "{}{}".format(str_title, '\n')
        for line in f:
            line = line.strip('\r\n')
            if len(line) > 5 and line != str_title:
                fr.append(line)
              #  print(line)
    #fr.remove(1)
     #   fr.pop(0)

# Здесь берется одна строка из переменной (которая как файл)
    for line in fr:
        #     print(line.replace(" ", ""))
        if len(line) > 2:
            array = line.split(',')
            array = line.split(',')
          #  print (array[0] + array[1] + "mmmmmmmmmmmmmmmmmmmmmmmmm")

            # Проверка того, что поле приоритета число
        # if int(array[3]).isdigit():
            if array[3] != "Priority":
                if int(array[3]):
                    # print (array[3] + "AAAAAAAAAAAAAAA")
                    if int(array[3]) > int(priority):
                        print (array[3]+"AAAAAAAAAAAAAAA")
                        #    print (priority)
                        # Тут я вызываю ф-ю. записи в журнал.
                        log_journal(line)
                       # os.system("taskkill /f " + array[2])



# Основная ф-ия входа. 
def log_env():
    global priority
    global timer
    print (format(sys.argv))
    if len(sys.argv) > 2:
        print ("Вы ввели приоритет {}!".format(sys.argv[2]))
        timer = int(format(sys.argv[1]))
        priority = format(sys.argv[2])
        #  print (format(sys.argv[2]))

        if platform == "linux" or platform == "linux2":
    # Запускаем батник. он просто записывает переменные окружения в файл.
            bash_func = subprocess.call(['/bin/bash', 'env_bash.bash'])
            # Тут я типа выполняю действия только после того, как батник отработал.
    # if bash_func.wait() == 0:
            dict_env()
        else:
            bat_func = subprocess.Popen('proc_bat.bat')

            # Тут я типа выполняю действия только после того, как батник отработал.
            if bat_func.wait()==0:
                dict_env()

    else:
        print ("Введите параметры для поиска")


# Это просто так )
    # for a in os.environ:
        # print('Var: ', a, 'Value: ', os.getenv(a))
    # print("all done" + "\n" + "\n")


log_env()

while True:
    time.sleep(timer) # in seconds
    log_env()