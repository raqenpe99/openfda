import json, urllib.request
with urllib.request.urlopen("https://api.fda.gov/drug/label.json?limit=10") as web:
    info = json.loads(web.read().decode())

for i in range(10):
    try:
        print("Medicamento:", i)
        print("Identificador del medicamento:", info["results"][i]["id"])
        print("Fabricante:",
              info["results"][i]["openfda"].get("manufacturer_name", ["No aparece información al respecto"])[0])
        print("Propósito:", info["results"][i].get("purpose", ["No aparece información al respecto"])[0])
        print("\n")
        continue

    except KeyError:
        print("Lo sentimos, no aparece registrada toda la información correspondiente a este medicamento", "\n")
