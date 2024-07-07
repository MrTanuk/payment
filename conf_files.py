import os
import time

def cleanScreen():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

def checkFiles():
    actual_dir = os.getcwd()

    if not os.path.exists(actual_dir + "/datas_files"):
        print("The datas_files folder does not exist.")
        time.sleep(2)
        datas_files_dir = actual_dir + "/datas_files/"
        os.mkdir(datas_files_dir)
        print("datas_files folder has been created.\n")

        if not os.path.exists(actual_dir + "conf_date.json"):
            print("No conf_date.json file exist.")
            time.sleep(2)
            open(datas_files_dir + "conf_date.json", "x")
            print("conf_date.json file has been created\n")

        if not os.path.exists(actual_dir + "data_payment.json"):
            print("The data_payment.json file does not exist")
            time.sleep(2)
            open(datas_files_dir + "data_payment.json", "x")
            print("data_payment.json file has been created\n")
    
    cleanScreen()