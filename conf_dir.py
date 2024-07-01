import os

def loadDirectories():
    actual_dir = os.getcwd()
    if not os.path.exists(actual_dir + "/datas_files"):
        print("No existe la carpeta datas_files.")
        datas_files_dir = actual_dir + "/datas_files"
        print("Creada.\n")
        os.mkdir(datas_files_dir)