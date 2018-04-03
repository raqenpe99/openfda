#Cambiamos la URL para acceder a la información en formato json de hasta 100 (número máximo) medicamentos relacionados con las aspirinas.

import json
import urllib.request
with urllib.request.urlopen("https://api.fda.gov/drug/label.json?limit=100&search=substance_name:ASPIRIN") as API: 
    info = json.loads(API.read().decode())

#Creamos un bucle que itere para cada medicamento, inicializado en 0, hasta llegar al último, donde se rompe; e imprimimos la 
#información en pantalla.
try:
    i=0
    while True:
        print("Medicamento:", info["results"][i]["id"])
        print("Nombre:", info["results"][i]["openfda"]["generic_name"][0])
        print("Fabricante:", info["results"][i]["openfda"]["manufacturer_name"][0])
        print()
        i+=1
        if i==100:
            break

except KeyError:
    print("Lo sentimos, no aparece registrada toda la información correspondiente a este medicamento", "\n")
