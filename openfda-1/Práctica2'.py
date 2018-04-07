import json
import http.client

headers = {'User-Agent': 'http-client'}

conexion = http.client.HTTPSConnection("api.fda.gov")
conexion.request("GET", "/drug/label.json?limit=10", None, headers)


JSON = conexion.getresponse()
print(JSON.status, JSON.reason)
info = json.loads(JSON.read().decode("utf-8"))


#Iteramos sobre cada uno, utilizando "get" para detectar la información que falte (indicado mediante una lista) y así permitir observar
#el resto de información sin que se interrumpa el programa.
try:
    for i in range(10):
        print("Medicamento:", i)
        print("Identificador del medicamento:", info["results"][i]["id"])
        print("Fabricante:", info["results"][i]["openfda"].get("manufacturer_name", ["No aparece información al respecto"])[0])
        print("Propósito:", info["results"][i].get("purpose", ["No aparece información al respecto"])[0])
        print("\n")

except KeyError:#Por si se nos escapa alguna posibilidad en las claves anteriores del diccionario.
    print("Lo sentimos, no aparece registrada toda la información correspondiente a este medicamento")