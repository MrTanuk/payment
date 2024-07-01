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
            with open(r"./datas_files/data_payment.json", "r") as read_json:
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
        with open(r"./datas_files/data_payment.json", "w") as save_json:
            json.dump(data, save_json, indent=4)
            print(f"\nLista llamada '{self.titulo}' guardado\n")