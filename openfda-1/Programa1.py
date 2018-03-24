import json, urllib.request
with urllib.request.urlopen("https://api.fda.gov/drug/label.json") as web:
    info = json.loads(web.read().decode())


print("El identificador del medicamento es", info.get("results")[0]["id"])
print("El propósito del medicamente es", str(info.get("results")[0]["purpose"]).strip("[]").strip("'"))
print("El nombre del fabricante es", str(info.get("results")[0]["openfda"]["manufacturer_name"][0]))
