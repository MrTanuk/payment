import os
import sys

def completedPath():
    path = sys.argv[0]
    absolute_path = os.path.abspath(path)
    absolute_path = absolute_path[:-7]
    return absolute_path

def cleanScreen():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")