from prettytable import PrettyTable
from tasa_bcv import getPriceDolar
import datetime as dt
import json

class Pago:
    def __init__(self, titulo: str, person: list):
        self.titulo = titulo
        self.dict_nombres = {"Nombres": person}
        # Inicialización eficiente de la lista de pagos con ceros
        self.dict_valores_bs = {"Bs": [0] * len(person)}
        self.dict_valores_dolar = {"$": [0] * len(person)}
        self.tiempo_pago = {"Tiempo de Pago":[str()] * len(person)}
        # Actualización del diccionario de nombres con los valores de pagos y
        # unidad
        self.dict_nombres.update(self.dict_valores_bs)
        self.dict_nombres.update(self.dict_valores_dolar)
        self.dict_nombres.update(self.tiempo_pago)

    def savePage(self):
        save_data = {self.titulo: self.dict_nombres}
        try:
            # Leer los datos existentes primero
            with open(r"./data_payment/data_payment.json", "r") as read_json:
                data = json.load(read_json)
                # Asegúrate de que 'self.titulo' no esté en 'data.keys()'
                while self.titulo in data.keys():
                    print("Vas a sobreescribir una lista ya existente")
                    print("Intente de nuevo\n")
                    print("1. Cambiar de nombre de titulo")
                    print("2. Salir\n")
                    opcion = int(input("Seleccione: "))
                    if opcion == 1:
                        nuevo_titulo = input("Escriba el título: ")
                        self.titulo = nuevo_titulo
                    elif opcion == 2:
                        return
                    else:
                        print("No es válida la selección")

                save_data = {self.titulo: self.dict_nombres}
                # Actualizar los datos con la nueva lista
                data.update(save_data)

        except FileNotFoundError:
            data = save_data

        except json.decoder.JSONDecodeError:
            # Si hay un error de decodificación, asumir que el archivo está vacío o corrupto
            data = save_data
            # Escribir los datos actualizados al archivo, usando el modo 'w' para sobrescribir
        with open(r"./data_payment/data_payment.json", "w") as save_json:
            json.dump(data, save_json, indent=4)
            print(f"\nLista llamada '{self.titulo}' guardado\n")

class Lista:
    def __init__(self):
        self.lista = {}

    def loadData(self):
        try:
            with open(r"./data_payment/data_payment.json", "r") as read_data:
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
            print("- ", data_cobrar)
        lista = input("\nEscoja el nombre de la lista: ")

        while lista not in self.lista.keys():
            print("\nNo se encuentra en la lista. Intente de nuevo")
            lista = input("Escoja la lista: ")
        return lista

    def menu(self, name_action, mainAction):
        print(f"1. - Para {name_action}")
        print("2. - Para verificar cómo va la lista")
        print("3. - Para salir")
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

            person = input("Seleccione la persona: ")
            cobrar = input("¿Cuánto pagó? ").split()
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
                with open(r"./data_payment/data_payment.json", "w") as save_cobrar:
                    json.dump(self.lista, save_cobrar, indent=4)
                    print("Actualizado con éxito\n")

        self.menu("cobrar", selectStudent)

    def addStudent(self):
        def addStudents(lista):
            nombre = input("Escriba el nombre: ")
            self.lista[lista]["Nombres"].append(nombre)
            pagara = input("¿Va a pagar de una vez? y/n: ").lower()
 
            if pagara == "y":
                pago = input("Ahora el pago: ").split()
                self.lista[lista]["Pagos"].append(float(pago[0]))
                self.lista[lista]["Unidades"].append(pago[1])
                fecha_actual = dt.datetime.now()
                fecha_actual_str = dt.datetime.strftime(fecha_actual, "%d %b %Y %H:%M")
                self.lista[lista]["Tiempo de Pago"].append(fecha_actual_str)

            elif pagara == "n":
                print("Perfecto. Continuemos")
                self.lista[lista]["Pagos"].append(0)
                self.lista[lista]["Unidades"].append("")
                self.lista[lista]["Tiempo de Pago"].append("")
            else:
                print("Escribiste mal. Intente de nuevo")

            self.lista.update(self.lista)
            with open(r"./data_payment/data_payment.json", "w") as edit_list:
                json.dump(self.lista, edit_list, indent=4)
                print("person añadidos\n")

        self.menu("Añadir", addStudents)

def main():
    while True:
        print("1. Leer listas")
        print("2. Crear nueva lista")
        print("3. Cobrar")
        print("4. Agregar persona")
        print("5. Salir\n")

        option = int(input("Seleccione la opción: "))
        inven = Lista()
        match option:
            case 1:
                if inven.loadData():
                    inven.checkDataOnTable()

            case 2:
                nombre = input("Nombre para la lista: ")
                estud = input("Escribe los nombres separado por coma: ").split(", ")
                pago = Pago(nombre, estud)
                pago.savePage()

            case 3:
                if inven.loadData():
                    price_dolar = getPriceDolar()
                    if price_dolar == None:
                        pass
                    else:
                        inven.chargePage(price_dolar)

            case 4:
                if inven.loadData():
                    inven.addStudent()

            case 5:
                break

            case _:
                print("Error. Ingrese de acuerdo al menu")

if __name__ == "__main__":
    main()