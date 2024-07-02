from list_payment import Lista
from payment import Pago
from tasa_bcv import importPriceDolar
from conf_files import checkFiles

def main():
    checkFiles()
    while True:
        print("1. Leer listas")
        print("2. Crear nueva lista")
        print("3. Cobrar")
        print("4. Agregar persona")
        print("5. Eliminar personas")
        print("6. Eliminar lista")
        print("7. Salir\n")

        option = int(input("Seleccione la opción: "))
        inven = Lista()
        match option:
            case 1:
                if inven.loadData():
                    inven.checkDataOnTable()

            case 2:
                nombre = input("Nombre para la lista: ")
                print("Escribe los nombres separado por coma junto con su espacio: ")
                estud = input("Nombres: ").split(", ")
                pago = Pago(nombre, estud)
                pago.savePage()

            case 3:
                if inven.loadData():
                    price_dolar = importPriceDolar()
                    inven.chargePage(price_dolar)

            case 4:
                if inven.loadData():
                    price_dolar = importPriceDolar()
                    inven.addStudent(price_dolar)

            case 5:
                if inven.loadData():
                    inven.deletePerson()
            
            case 6:
                if inven.loadData():
                    inven.deleteList()
            case 7:
                break

            case _:
                print("Error. Ingrese de acuerdo al menu")

if __name__ == "__main__":
    main()