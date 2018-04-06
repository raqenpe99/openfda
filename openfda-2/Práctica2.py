#Cambiamos la URL para acceder a la información en formato json de hasta 100 (número máximo) medicamentos relacionados con las aspirinas,
# que tendrán como principio activo el ácido acetilsalicílico.

import json
import urllib.request
with urllib.request.urlopen("https://api.fda.gov/drug/label.json/?search=active_ingredient:acetylsalicylic&limit=100") as API: 
    info = json.loads(API.read().decode())

#Iteramos sobre cada medicamento con "for" hasta llegar al último existente, donde finaliza; e imprimimos la información en pantalla.
#Si no aparece ninguna información en openfda, en lugar de ejecutarse el primer if, se ejecuta el else, evitando el KeyError.

    
for i in range(len(info["results"])):
    print("Medicamento:", info["results"][i]["id"])

    if info["results"][i]["openfda"]:
        print("Nombre:", info["results"][i]["openfda"]["generic_name"][0])
        print("Fabricante:", info["results"][i]["openfda"]["manufacturer_name"][0])
        print()
    else:
        print("Lo sentimos, no aparece información  del fabricante \n")
