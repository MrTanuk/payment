import os

def loadDirectories():
    actual_dir = os.getcwd()

    if not os.path.exists(actual_dir + "/datas_files"):
        print("No existe la carpeta datas_files.")
        datas_files_dir = actual_dir + "/datas_files"
        os.mkdir(datas_files_dir)
        print("Carpeta datas_files creada.\n")

        if not os.path.exists(actual_dir + "conf_date.json"):
            print("No existe el archivo conf_date.json.")
            open(datas_files_dir + "conf_date.json", "x")
            print("archivos conf_date.json creada\n")

        if not os.path.exists(actual_dir + "data_payment.json"):
            print("No existe el archivo data_payment.json.")
            open(datas_files_dir + "data_payment.json", "x")
            print("archivos data_payment.json creada\n")