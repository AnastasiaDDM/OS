import datetime


# Ф-ия для записи строк в файл-журнал.
def log_journal(file_log, string):

    with open(file_log, "a") as file:
        file.write(str(datetime.datetime.now()) + "    " + string+"\n\n")
