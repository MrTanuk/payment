import os
import time

def cleanScreen():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")