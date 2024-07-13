import list_payment
import payment
import dolar_rate
import conf_files

def main():
    conf_files.cleanScreen()
    while True:
        print("1. Read lists")
        print("2. Create new list")
        print("3. Charge")
        print("4. Add Person in list")
        print("5. Delete Person in list")
        print("6. Delete list")
        print("7. Exit\n")

        option = int(input("Select an option: "))
        inven = list_payment.Lista()
        match option:
            case 1:
                if inven.loadData():
                    inven.checkDataOnTable()

            case 2:
                conf_files.cleanScreen()
                name_list = input("Name for the list: ")
                conf_files.cleanScreen()
                print("Type the names separated by comma\n")
                names_people = input("Names: ")
                names_people_to_list = [name.strip() for name in names_people.split(",")]
                pago = payment.Charge(name_list, names_people_to_list)
                pago.saveCharge()

            case 3:
                if inven.loadData():
                    conf_files.cleanScreen()
                    price_dolar = dolar_rate.importPriceDolar()
                    if price_dolar:
                        inven.chargePage(price_dolar)

            case 4:
                if inven.loadData():
                    price_dolar = dolar_rate.importPriceDolar()
                    if price_dolar:
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