# Ф-ия для записи строк в файл-журнал.
def log_journal(file_log, string):
    with open(file_log, "a") as file:
        file.write(string+"\n\n")

    # file = open('logs_proc.txt', 'a+')
    # file.write(string)
    # file.write("\n")
    # file.close()