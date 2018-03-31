import json
import urllib.request
with urllib.request.urlopen("https://api.fda.gov/drug/label.json?limit=100%27&search=substance_name:%22ASPIRIN%22") as web:
    info = json.loads(web.read().decode())

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
    print("Lo sentimos, no aparece registrada toda la información correspondiente acerca de este medicamento", "\n")
