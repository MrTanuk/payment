from prettytable import PrettyTable
import json
import datetime as dt

class Lista:
    def __init__(self):
        self.lista = {}

    def loadData(self):
        try:
            with open(r"./datas_files/data_payment.json", "r") as read_data:
                self.lista = json.load(read_data)

        except FileNotFoundError:
            print("No existe la base de datos. Añada datos\n")
            return False

        except json.decoder.JSONDecodeError:
            print("Esta vacío la base de dato. Añada datos")
            return False

        else:
            return True

    def chooseTable(self):
        for data_cobrar in self.lista:
            print("._", data_cobrar)
        lista = input("\nEscoja el nombre de la lista: ")

        while lista not in self.lista.keys():
            print("\nNo se encuentra en la lista. Intente de nuevo")
            lista = input("Escoja la lista: ")
        return lista

    def menu(self, name_action, mainAction):
        print(f"1. - Para {name_action}")
        print("2. - Para verificar cómo va la lista")
        print("3. - Para salir\n\n")
        option = int(input("Seleccione: "))
        match option:
            case 1:
                lista = self.chooseTable()
                mainAction(lista)
                return
            case 2:
                self.checkDataOnTable()
                self.menu(name_action, mainAction)

            case 3:
                return
            case _:
                print("Error. Ingrese de acuerdo al menu\n")

    def checkDataOnTable(self):
        for key, table_data in self.lista.items():
            table = PrettyTable(table_data.keys())
            for i in range(len(table_data["Nombres"])):
                table.add_row([table_data[key][i] for key in table_data])
            print(f"{key:}".center(50))
            print(table,"\n")

    def chargePage(self, price_dolar):
        def selectStudent(lista):
            print("Nombres:")
            for count, name in enumerate(self.lista[lista]["Nombres"]):
                print(f"{count + 1}.- {name}")

            person = input("Seleccione el índice de la persona en la lista: ")
            print("¿Cuánto pagó? Ejemplo: '43 Bs', '2.5 $")
            cobrar = input("Indique monto: ").split()
            value, unidad = float(cobrar[0]), cobrar[1]
            if unidad.lower() == "bs":
                self.lista[lista]["Bs"][int(person) - 1] = float(value)
                self.lista[lista]["$"][int(person) - 1] = round(value/price_dolar, 2)
            elif unidad == "$":
                self.lista[lista]["$"][int(person) - 1] = float(value)
                self.lista[lista]["Bs"][int(person) - 1] = round(price_dolar*value, 2)
            else:
                print("Error. Formato incorrecto: Bolívares o dolares")
            fecha_actual = dt.datetime.now()
            fecha_actual_str = dt.datetime.strftime(fecha_actual, "%d %b %Y %H:%M")
            self.lista[lista]["Tiempo de Pago"][int(person) - 1] = fecha_actual_str

            print("--------------------------")
            print(self.lista[lista]["Nombres"][int(person) - 1], "ha pagado",
            cobrar[0], cobrar[1])
            print("--------------------------\n")
            repeat = input("¿Cobrarás a alguien más? y/n: ")

            if repeat == "y":
                selectStudent(lista)
            else:
                with open(r"./datas_files/data_payment.json", "w") as save_cobrar:
                    json.dump(self.lista, save_cobrar, indent=4)
                    print("Actualizado con éxito\n")

        self.menu("cobrar", selectStudent)

    def addStudent(self, price_dolar):
        def addStudents(lista):
            nombre = input("Escriba el nombre: ")
            self.lista[lista]["Nombres"].append(nombre)
            pagara = input("¿Va a pagar de una vez? y/n: ").lower()
 
            if pagara == "y":
                print("¿Cuánto pagó? Ejemplo: '43 Bs', '2.5 $")
                cobrar = input("Indique monto: ").split()
                value, unidad = float(cobrar[0]), cobrar[1]
                if unidad.lower() == "bs":
                    self.lista[lista]["Bs"].append(float(value))
                    self.lista[lista]["$"].append(round(value/price_dolar, 2))
                elif unidad == "$":
                    self.lista[lista]["$"].append(float(value))
                    self.lista[lista]["Bs"].append(round(price_dolar*value, 2))
                else:
                    print("Error. Formato incorrecto: Bolívares o dolares")
    
            elif pagara == "n":
                print("Perfecto. Continuemos")
                self.lista[lista]["Bs"].append(0)
                self.lista[lista]["$"].append(0)
                self.lista[lista]["Tiempo de Pago"].append("")
            else:
                print("Escribiste mal. Intente de nuevo")
                
            fecha_actual = dt.datetime.now()
            fecha_actual_str = dt.datetime.strftime(fecha_actual, "%d %b %Y %H:%M")
            self.lista[lista]["Tiempo de Pago"].append(fecha_actual_str)
            
            repeat = input("¿Cobrarás a alguien más? y/n: ")

            if repeat == "y":
                addStudents(lista)
            else:
                self.lista.update(self.lista)
                with open(r"./datas_files/data_payment.json", "w") as edit_list:
                    json.dump(self.lista, edit_list, indent=4)
                print("persona añadida\n")

        self.menu("Añadir", addStudents)