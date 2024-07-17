from conf_files import cleanScreen, completedPath
from prettytable import PrettyTable
import re
import json
import datetime as dt

class Lista:
    def __init__(self):
        self.lista = {}
        self.path_data_payment = completedPath()
        self.path_data_payment += "/datas_files/data_payment.json"

    def loadData(self):
        cleanScreen()
        try:
            with open(self.path_data_payment, "r") as read_data:
                self.lista = json.load(read_data)
            if self.lista == {}:
                print("No database exists. Add data\n")
                return False

        except FileNotFoundError:
            print("Database not found. Search if the file data_payment.json exist inside the data_file dir\n")
            return False

        except json.decoder.JSONDecodeError:
            print("The database is empty. Add data\n")
            return False

        else:
            return True

    def chooseTable(self):
        cleanScreen()
        for name_in_list in self.lista:
            print(". ", name_in_list)
        lista = input("\nChoose the name from the list: ")
        if lista not in self.lista.keys():
            print("\nit is not in the list. Try again\n")
            return False
        else:
            return lista

    def chooseName(self, lista):
        cleanScreen()
        print("Names:\n")
        for index_name, name in enumerate(self.lista[lista]["Name"]):
            print(f"{index_name + 1}.- {name}")

    def chooseRepeat(self, mainAction, lista):
        select_option = input("\nWill you select anyone else? y/n: ")

        if select_option == "y":
            mainAction(lista)
        else:
            self.lista.update(self.lista)
            with open(self.path_data_payment, "w") as edit_list:
                json.dump(self.lista, edit_list, indent=4)
            cleanScreen()

    def menu(self, name_action, mainAction):
        print(f"1. - {name_action}")
        print("2. - Check how the list is going")
        print("3. - Exit\n")

        option = int(input("Choose: "))
        match option:
            case 1:
                lista = self.chooseTable()
                if lista:
                    mainAction(lista)
                else:
                    return
            case 2:
                self.checkDataOnTable()
                self.menu(name_action, mainAction)
            case 3:
                cleanScreen()
                return
            case _:
                cleanScreen()
                print("Error. Enter according to the menu\n")

    def checkDataOnTable(self):
        cleanScreen()
        for title_list, datas_on_table in self.lista.items():
            table = PrettyTable(datas_on_table.keys())
            for i in range(len(datas_on_table["Name"])):
                table.add_row([datas_on_table[title_list][i] for title_list in datas_on_table])
            print(f"{title_list:}".rjust(len(title_list) + 3))
            print(table,"\n")

    def chargePage(self, price_dolar):
        def selectPerson(lista):
            self.chooseName(lista)

            select_person = int(input("\nSelect the index of the person in the list: "))
            cleanScreen()
            print("How much did the person pay? Example: '43bs', '2.5$'")
            parts_money = input("Indicate amount: ")
            charge_person = re.split(r"(\d+\.\d+|\d+)", parts_money)
            charge_person = [parts.strip() for parts in charge_person if parts]
            print(charge_person)
            value_money, unity_money = float(charge_person[0]), charge_person[1]
            if unity_money.lower() == "bs":
                self.lista[lista]["Bs"][select_person - 1] = float(value_money)
                self.lista[lista]["$"][select_person - 1] = round(value_money/price_dolar, 2)
            elif unity_money == "$":
                self.lista[lista]["$"][select_person - 1] = float(value_money)
                self.lista[lista]["Bs"][select_person - 1] = round(price_dolar*value_money, 2)
            else:
                print("Error. Incorrect format: Bolivars or dollars.")
                return

            current_date = dt.datetime.now()
            current_date_str = dt.datetime.strftime(current_date, "%d %b %Y %H:%M")
            self.lista[lista]["Payment Time"][select_person - 1] = current_date_str

            cleanScreen()
            print("--------------------------")
            print(self.lista[lista]["Name"][select_person - 1], "has paid",
            value_money, unity_money)
            print("--------------------------")

            self.chooseRepeat(selectPerson, lista)
        self.menu("Charge", selectPerson)

    def addPerson(self, price_dolar):
        def addPeople(lista):
            cleanScreen()
            add_person = input("Type the name: ")
            self.lista[lista]["Name"].append(add_person)
            cleanScreen()
            option = input("Is the person going to pay at once? y/n: ").lower()
            cleanScreen()
 
            if option == "y":
                print("How much did the person pay? Example: '43bs', '2.5$")
                parts_money = input("Indicate amount: ")
                charge_person = re.split(r"(\d+)", parts_money)
                charge_person = [parts.strip() for parts in charge_person if parts]
                print(charge_person)
                value_money, unity_money = float(charge_person[0]), charge_person[1]
                if unity_money.lower() == "bs":
                    self.lista[lista]["Bs"].append(float(value_money))
                    self.lista[lista]["$"].append(round(value_money/price_dolar, 2))
                elif unity_money == "$":
                    self.lista[lista]["$"].append(float(value_money))
                    self.lista[lista]["Bs"].append(round(price_dolar*value_money, 2))
                else:
                    print("Error. Incorrect format: Bolivars or dollars.\n")
                    return
    
            elif option == "n":
                print("Perfect. Let's continue")
                self.lista[lista]["Bs"].append(0)
                self.lista[lista]["$"].append(0)
                self.lista[lista]["Payment Time"].append("")
            else:
                print("You spelled it wrong. Try again")
                return

            current_date = dt.datetime.now()
            current_date_str = dt.datetime.strftime(current_date, "%d %b %Y %H:%M")
            self.lista[lista]["Payment Time"].append(current_date_str)

            cleanScreen()
            print("--------------------------")
            print(add_person, "has been added")
            print("--------------------------")

            self.chooseRepeat(addPeople, lista)
        self.menu("Add", addPeople)

    def deletePerson(self):
        def selectPerson(lista):
            self.chooseName(lista)

            index_person = input("Select the index of the person in the list: ")
            del self.lista[lista]["Name"][int(index_person) - 1]
            del self.lista[lista]["Bs"][int(index_person) - 1]
            del self.lista[lista]["$"][int(index_person) - 1]
            del self.lista[lista]["Payment Time"][int(index_person) - 1]
            
            cleanScreen()
            print("Person deleted correctly")
            self.chooseRepeat(selectPerson, lista)
        self.menu("Delete person", selectPerson)

    def deleteList(self):
        def deleteListFinal(delete_list):
            del self.lista[delete_list]
            with open(self.path_data_payment, "w") as edit_list:
                json.dump(self.lista, edit_list, indent=4)

            cleanScreen()
            print("Correctly completed list")
        self.menu("Delete list", deleteListFinal)