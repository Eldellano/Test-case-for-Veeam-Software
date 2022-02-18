import os
import shutil
import time
import sys


def sinch(frm, to, time_last_sinch):
    dir_from = frm
    dir_to = to
    last_sinch_dt = time_last_sinch
    content_dir_from = os.listdir(dir_from)
    content_dir_to = os.listdir(dir_to)
    for i in content_dir_from:
        mod_file_time = os.path.getmtime(fr'{dir_from}\{i}')  # время и дата последнего изменения файла
        if os.path.isfile(fr'{dir_from}\{i}') and mod_file_time > last_sinch_dt:  # проверяем когда модифицировался файл
            shutil.copy(fr'{dir_from}\{i}', dir_to)
            print('Копируем файл')
        if os.path.isdir(fr'{dir_from}\{i}'):
            if not os.path.isdir(fr'{dir_to}\{i}'):  # если нет папки в целевой директории
                print('Создаем папку')
                os.mkdir(fr'{dir_to}\{i}')  # создаем папку
            frm_for_dir = fr'{dir_from}\{i}'
            to_for_dir = fr'{dir_to}\{i}'
            sinch(frm_for_dir, to_for_dir,  last_sinch_dt)
    for i in content_dir_to:  # удаляем ненужные файлы
        if i not in content_dir_from:
            if os.path.isfile(fr'{dir_to}\{i}'):
                print('Удаляем файл')
                os.remove(fr'{dir_to}\{i}')
            else:
                print('Удаляем папку')
                os.rmdir(fr'{dir_to}\{i}')
    write_sinch_date()  # пишем дату последней синхронизации


# пишем дату и время в файл
# TODO: писать файл в директорию источник
def write_sinch_date():
    with open('sinch_date.txt', 'w') as file:
        file.write(str(time.time()))


# читаем из файла время последней синхронизации
def get_sinch_date():
    try:
        with open('sinch_date.txt', 'r') as file:
            return float(file.read())
    except FileNotFoundError:
        with open('sinch_date.txt', 'w') as file:
            file.write('')
        return 0


def start(frm, to, idle_per):
    dir_f = frm
    dir_t = to
    waiting = idle_per
    last_sinch_dt = get_sinch_date()
    while True:
        sinch(dir_f, dir_t, last_sinch_dt)
        time.sleep(int(waiting) * 60)


if __name__ == "__main__":
    if len(sys.argv) == 4:
        dir_from = sys.argv[1]
        dir_to = sys.argv[2]
        sinch_period = sys.argv[3]
        start(dir_from, dir_to, sinch_period)
    else:
        raise AttributeError(f'При запуске программы следует указывать 3 аргумента, вы указали {len(sys.argv) - 1}')
