import json
import http.client

headers = {'User-Agent': 'http-client'} #Define el cliente que va a a hacer la petición. Éste está integrado en python

#En la primera línea establecemos la conexión y, a continuación, pedimos el recurso específico empleando el método GET.
#Para nuestro caso, serán los medicamentos que tienen como principio activo el ácido acetilsalicílico.
#Establecemos el límite en 100, número máximo.

conexion = http.client.HTTPSConnection("api.fda.gov")
conexion.request("GET", "/drug/label.json", None, headers)


JSON = conexion.getresponse()   #Obtienes el json en bruto.
print(JSON.status, JSON.reason) #Status imprime el valor de 200 y reason, el OK (funciones de http.client).
                                #Nos muestra que la petición es correcta.

#A continuación, se lee y se descodifica el json, para que "loads" pueda convertirlo en una estructura de datos tipo diccionario.
info = json.loads(JSON.read().decode("utf-8"))

#Encontramos los resultados del medicamento por defecto y, en caso de que no exista esa clave, devuelve el valor por defecto "None":
print("*Identificador del medicamento:", info.get("results")[0]["id"])
print("*Propósito:", info.get("results")[0]["purpose"][0])
print("*Fabricante:", info.get("results")[0]["openfda"]["manufacturer_name"][0])
