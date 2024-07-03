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
            if self.lista == {}:
                print("No database exists. Add data\n")
                return False
    
        except FileNotFoundError:
            print("No database exists. Add data\n")
            return False

        except json.decoder.JSONDecodeError:
            print("The database is empty. Add data\n")
            return False
        
        else:
            return True

    def chooseTable(self):
        for name_in_list in self.lista:
            print(". ", name_in_list)
        lista = input("\Choose the name from the list: ")
        while lista not in self.lista.keys():
            print("\nit is not in the list. Try again")
            lista = input("Choose the list: ")
        return lista

    def chooseName(self, lista):
        print("Names:")
        for index_name, name in enumerate(self.lista[lista]["Name"]):
            print(f"{index_name + 1}.- {name}")

    def chooseRepeat(self, mainAction, lista):
        select_option = input("Will you select anyone else? y/n: ")

        if select_option == "y":
            mainAction(lista)
        else:
            self.lista.update(self.lista)
            with open(r"./datas_files/data_payment.json", "w") as edit_list:
                json.dump(self.lista, edit_list, indent=4)
            print("Completed.\n")

    def menu(self, name_action, mainAction):
        print(f"1. - {name_action}")
        print("2. - Check how the list is going")
        print("3. - Exit\n")

        option = int(input("Choose: "))
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
                print("Error. Enter according to the menu\n")

    def checkDataOnTable(self):
        for title_list, datas_on_table in self.lista.items():
            table = PrettyTable(datas_on_table.keys())
            for i in range(len(datas_on_table["Name"])):
                table.add_row([datas_on_table[title_list][i] for title_list in datas_on_table])
            print(f"{title_list:}".rjust(len(title_list) + 3))
            print(table,"\n")

    def chargePage(self, price_dolar):
        def selectPerson(lista):
            self.chooseName(lista)

            select_person = input("Select the index of the person in the list: ")
            print("How much did the person pay? Example: '43 Bs', '2.5 $'.")
            charge_person = input("Indicate amount: ").split()
            value_money, unity_money = float(charge_person[0]), charge_person[1]
            if unity_money.lower() == "bs":
                self.lista[lista]["Bs"][int(select_person) - 1] = float(value_money)
                self.lista[lista]["$"][int(select_person) - 1] = round(value_money/price_dolar, 2)
            elif unity_money == "$":
                self.lista[lista]["$"][int(select_person) - 1] = float(value_money)
                self.lista[lista]["Bs"][int(select_person) - 1] = round(price_dolar*value_money, 2)
            else:
                print("Error. Incorrect format: Bolivars or dollars.")
            current_date = dt.datetime.now()
            current_date_str = dt.datetime.strftime(current_date, "%d %b %Y %H:%M")
            self.lista[lista]["Payment Time"][int(select_person) - 1] = current_date_str

            print("--------------------------")
            print(self.lista[lista]["Name"][int(select_person) - 1], "has paid",
            charge_person[0], charge_person[1])
            print("--------------------------\n")

            self.chooseRepeat(selectPerson, lista)
        self.menu("Charge", selectPerson)

    def addPerson(self, price_dolar):
        def addPeople(lista):
            add_person = input("Type the name: ")
            self.lista[lista]["Name"].append(add_person)
            option = input("Is the person going to pay at once? y/n: ").lower()
 
            if option == "y":
                print("How much did the person pay? Example: '43 Bs', '2.5 $'.")
                charge_person = input("Indicate amount: ").split()
                value_money, unity_money = float(charge_person[0]), charge_person[1]
                if unity_money.lower() == "bs":
                    self.lista[lista]["Bs"].append(float(value_money))
                    self.lista[lista]["$"].append(round(value_money/price_dolar, 2))
                elif unity_money == "$":
                    self.lista[lista]["$"].append(float(value_money))
                    self.lista[lista]["Bs"].append(round(price_dolar*value_money, 2))
                else:
                    print("Error. Incorrect format: Bolivars or dollars.")
    
            elif option == "n":
                print("Perfect. Let's continue")
                self.lista[lista]["Bs"].append(0)
                self.lista[lista]["$"].append(0)
                self.lista[lista]["Payment Time"].append("")
            else:
                print("You spelled it wrong. Try again")

            current_date = dt.datetime.now()
            current_date_str = dt.datetime.strftime(current_date, "%d %b %Y %H:%M")
            self.lista[lista]["Payment Time"].append(current_date_str)

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
            print("Person deleted correctly\n")

            self.chooseRepeat(selectPerson, lista)
        self.menu("Delete person", selectPerson)

    def deleteList(self):
        delete_list = self.chooseTable()
        del self.lista[delete_list]
        with open(r"./datas_files/data_payment.json", "w") as edit_list:
            json.dump(self.lista, edit_list, indent=4)
        print("Correctly completed list\n")