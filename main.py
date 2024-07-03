from list_payment import Lista
from payment import Charge
from tasa_bcv import importPriceDolar
from conf_files import checkFiles

def main():
    checkFiles()
    while True:
        print("1. Read lists")
        print("2. Create new list")
        print("3. Charge")
        print("4. Add people_to_list")
        print("5. Delete people_to_list")
        print("6. Delete list")
        print("7. Exit\n")

        option = int(input("Select an option: "))
        inven = Lista()
        match option:
            case 1:
                if inven.loadData():
                    inven.checkDataOnTable()

            case 2:
                name_to_list = input("Name for the list: ")
                print("Type the names separated by comma along with their spacing: ")
                people_to_list = input("Names: ").split(", ")
                pago = Charge(name_to_list, people_to_list)
                pago.saveCharge()

            case 3:
                if inven.loadData():
                    price_dolar = importPriceDolar()
                    inven.chargePage(price_dolar)

            case 4:
                if inven.loadData():
                    price_dolar = importPriceDolar()
                    inven.addPerson(price_dolar)

            case 5:
                if inven.loadData():
                    inven.deletePerson()
            
            case 6:
                if inven.loadData():
                    inven.deleteList()
            case 7:
                break

            case _:
                print("Error. Enter according to the menu")

if __name__ == "__main__":
    main()