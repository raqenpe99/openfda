try:
    import json
    import urllib.request 

    with urllib.request.urlopen("https://api.fda.gov/drug/label.json?limit=10") as API: #Modificamos la URL para que aparezcan diez 
        info = json.loads(API.read().decode())                                          #medicamentos

#Iteramos sobre cada uno, utilizando "get" para detectar la información que falte (indicado mediante una lista) y así permitir observar
#el resto de información sin que se interrumpa el programa.

    for i in range(10): 
        print("Medicamento:", i)
        print("Identificador del medicamento:", info["results"][i]["id"])
        print("Fabricante:", info["results"][i]["openfda"].get("manufacturer_name", ["No aparece información al respecto"])[0])
        print("Propósito:", info["results"][i].get("purpose", ["No aparece información al respecto"])[0])
        print("\n")


except KeyError:
    print("Lo sentimos, no aparece registrada toda la información correspondiente a este medicamento")

