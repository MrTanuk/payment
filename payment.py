import json
import conf_files
import conf_files

class Charge:
    def __init__(self, title_list: str, people: list):
        self.title_list = title_list
        self.dict_names = {"Name": people}
        # Inicialización eficiente de la lista de pagos con ceros
        self.dict_price_bs = {"Bs": [0] * len(people)}
        self.dict_price_dollar = {"$": [0] * len(people)}
        self.payment_time = {"Payment Time":[str()] * len(people)}
        # Actualización del diccionario de nombres con los valores de pagos y
        # unidad
        self.dict_names.update(self.dict_price_bs)
        self.dict_names.update(self.dict_price_dollar)
        self.dict_names.update(self.payment_time)

    def saveCharge(self):
        save_data = {self.title_list: self.dict_names}
        try:
            # Read first the existing data
            with open(r"./datas_files/data_payment.json", "r") as read_json:
                data = json.load(read_json)
                # Asegúrate de que 'self.title_list' no esté en 'data.keys()'
                while self.title_list in data.keys():
                    conf_files.cleanScreen()
                    print("You are going to overwrite an existing list\n")
                    print("1. Rename the list")
                    print("2. Exit\n")
                    opcion = int(input("Select the index: "))
                    if opcion == 1:
                        conf_files.cleanScreen()
                        nuevo_title_list = input("Type the title: ")
                        self.title_list = nuevo_title_list
                    elif opcion == 2:
                        conf_files.cleanScreen()
                        return
                    else:
                        print("The selection is not valid")

                save_data = {self.title_list: self.dict_names}
                # Update the data with the new list
                data.update(save_data)

        except FileNotFoundError:
            print("Database not found.")
            return

        except json.decoder.JSONDecodeError:
            # If there is a decoding error, assume that the file is empty or corrupt.
            data = save_data
            # Write the updated data to the file, to overwrite
        with open(r"./datas_files/data_payment.json", "w") as save_json:
            json.dump(data, save_json, indent=4)

        conf_files.cleanScreen()
        print(f"List named '{self.title_list}' has beed saved\n")