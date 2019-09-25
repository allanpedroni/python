import os
import shutil
from os import path
import datetime
from datetime import date, time, timedelta
import time

def read_file_by_line(file):
    f = open(file, "r")
    fred = f.readlines()

    for line in fred:
        print(line)

    f.close()


def read_file(file):
    f = open(file, "r")
    if f.mode == 'r':
        contents = f.read()
        print(contents)
    f.close()


def write_file(file):
    f = open(file, "w+")

    for i in range(10):
        f.write(f"this is line {i + 1:d}\r\n")

    f.close()


def append_file(file):
    f = open(file, 'a+')

    for i in range(2):
        f.write(f"Appended line {i + 1:d}\r\n")


def main():
    file = 'new_file.txt'
    if path.exists(file):
        src = path.realpath(file)

    head, tail = path.split(src)
    print('head:', head)
    print('tail:', tail)
    print('last modified date:', time.ctime(path.getctime('new_file.txt.bak')))

    dst = src + '.bak'

    shutil.copy(src, dst)
    # write_file(file)
    # append_file(file)
    # read_file(file)
    # read_file_by_line(file)


main()
