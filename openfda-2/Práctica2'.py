import json
import http.client

headers = {'User-Agent': 'http-client'} #Define el cliente que va a a hacer la petición. Éste está integrado en python

#En la primera línea establecemos la conexión y, a continuación, pedimos el recurso específico empleando el método GET.
#Para nuestro caso, serán los medicamentos que tienen como principio activo el ácido acetilsalicílico.
#Establecemos el límite en 100, número máximo.

conexion = http.client.HTTPSConnection("api.fda.gov")
conexion.request("GET", "/drug/label.json/?search=active_ingredient:acetylsalicylic&limit=100", None, headers)


JSON = conexion.getresponse()   #Obtienes el json en bruto.
print(JSON.status, JSON.reason) #Status imprime el valor de 200 y reason, el OK (funciones de http.client).Nos muestra que la petición es correcta.

#A continuación, se lee y se descodifica el json, para que "loads" pueda convertirlo en una estructura de datos tipo diccionario.

info = json.loads(JSON.read().decode("utf-8"))

#Iteramos sobre cada medicamento con "for" hasta llegar al último existente, donde finaliza; e imprimimos la información en pantalla.
#Si no aparece ninguna información en openfda, en lugar de ejecutarse el primer if, se ejecuta el else, evitando el KeyError.

for i in range(len(info["results"])):
    print("*Medicamento:", info["results"][i]["id"])

    if info["results"][i]["openfda"]:
        print("*Nombre:", info["results"][i]["openfda"]["generic_name"][0])
        print("*Fabricante:", info["results"][i]["openfda"]["manufacturer_name"][0])
        print()
    else:
        print("Lo sentimos, no aparece información  del fabricante \n")
