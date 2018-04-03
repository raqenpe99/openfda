import json
import urllib.request #Request envía cabeceras HTTP a la URL de destino
                      #Open permite que sean leídas posteriormente

with urllib.request.urlopen("https://api.fda.gov/drug/label.json") as API: #Loads permite tomar la cadena de texto en formato JSON 
    info = json.loads(API.read().decode())                                 #y convertirla en una estructura tipo diccionario, al
                                                                           #leer y descondificar la información de la url
        
#Encontramos los resultados del medicamento por defecto y, en caso de que no exista esa llave, devuelve el valor por defecto "None":

print("Identificador del medicamento:", info.get("results")[0]["id"])
print("Propósito:", info.get("results")[0]["purpose"][0])
print("Fabricante:", info.get("results")[0]["openfda"]["manufacturer_name"][0])
