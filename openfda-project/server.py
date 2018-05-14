import http.server
import http.client
import socketserver
import json

PORT = 8000
socketserver.TCPServer.allow_reuse_address = True

#Escogemos la siguiente clae de la libería htttp.server para poder emplear los métodos que hereda e incorporar nuevos
class TestHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def get_conection(self, limit=10, busqueda="", name=""): #Establece la conexión con OpenFDA

        headers = {'User-Agent': 'http-client'}
        peticion= "/drug/label.json?limit={}".format(limit) #Creamos la petición en función de los parámetros escogidos.

        if busqueda != "": #En el caso de que existan parámetros, los añade a la petición para poder acceder a esos datos en la búsqueda
            peticion += '&search='+busqueda+':'+ name

        print("Recurso solicitado: {}".format(peticion))

        conexion = http.client.HTTPSConnection("api.fda.gov") #Establece la conexión.
        conexion.request("GET", peticion , None, headers)     #Envía el mensaje de solicitud.


        JSON = conexion.getresponse() #Obtiene la respuesta del servidor

        if JSON.status == 404:  #Si no existe la página solicitada de OpenFDA, envía el mensaje indicándolo Y aborta el programa.
            print("ERROR. Recurso no encontrado")
            exit(1)

        print(JSON.status, JSON.reason)
        info = json.loads(JSON.read().decode("utf-8")) 
        #Se lee y se descodifica el json, para que "loads" pueda convertirlo en una estructura de datos tipo diccionario.
        conexion.close()

        return info

    def get_index(self): #Crea el contenido html del formulario
        contenido= '''
            <html>
                <head>
                    <title>API OpenFDA</title>
                </head>
                <body style='background: linear-gradient(to right, #A3E4D7, #196F3D)'>
                    <h1>Introduzca los datos que desee buscar:</h1>
            <p><h3>Listado de medicamentos:</h3></p>
            <p><form action="listDrugs">
                  Limite:<input type="text" name='limit' value="1">
            <p><input type="submit" value="Aceptar"></p>
            </form>

            <p><h3>Listado de empresas:</h3></p>
            <form action = "listCompanies" method="get">
                  Limite: <input type="text" name="limit" value="1">
            <p><input type="submit" value="Aceptar"></p>

            </form>

            <p><h3>Listado de precauciones:</h3></p>
            <form action = "listWarnings" method="get">
                  Limite: <input type="text" name="limit" value="1">

            <p><input type="submit" value="Aceptar"></p>

            </form>

            <p><h3>Busqueda de farmacos:</h3></p>
            <form action = "searchDrug" method="get">
                  Principio activo: <input type="text" name="active_ingredient" value="acetylsalicylic">
                  Limite: <input type="text" name="limit" value="1">

            <p><input type="submit" value="Aceptar"></p>

            </form>

            <p><h3>Busqueda de empresas:</h3></p>
            <form action = "searchCompany" method="get">
                  Empresa: <input type="text" name="company" value="carefusion">
                  Limite: <input type="text" name="limit" value="1">

            <p><input type="submit" value="Aceptar"></p>

            </form>

            '''
        return contenido


    def get_listDrugs(self, limit): #Crea y devuelve el contenido del html con el listado de fármacos
        
        info=self.get_conection(limit) #Establece la conexión con OpenFDA
        drug=info["results"]     
        
        #A continuación, genera el contenido que será devuelto en un html, iterando sobre cada medicamento dentro del diccionario 
        #obtenido de OpenFD y agrupándo los nombres en una tabla.
        contenido = (' <!DOCTYPE html>\n'     
           '<html lang="es">\n'
           '<head>\n'
           '    <meta charset="UTF-8">\n'
           '    <title>API</title>\n'
           '</head>\n'
           '<body style="background: linear-gradient(to right, #D358F7, #FF0040)">\n'
           '<h1>Obtención de datos Openfda:</h2>\n'
           '<img src="https://2.bp.blogspot.com/-_QDuJunXuyM/WJxbPq_5XsI/AAAAAAAASls/84d8ZrZYoCMyt_jigvCRmqGxJjITZjjcACLcB/s1600/medico.jpg" border="1" width="500" height="500" align="right">'
           '<h3>listDRUGS</h3>'
           '\n'
           '<table style="width:50%" border="4">\n'
           '<tr>\n'
             '<th>Identificador</th>\n'
             '<th>Nombre</th>\n'
             '<th>Empresa</th>\n'
             '<th>Propósito</th>\n'
            '</tr>\n')

        for i in range(len(drug)):   
            id= drug[i]["id"]     #Identificador
            purpose=drug[i].get("purpose", ["No aparece información al respecto"])[0]  #Propósito

            if drug[i]["openfda"]:
                name=drug[i]["openfda"]["generic_name"][0]  #Nombre del medicamento
                manufacturer= drug[i]["openfda"]["manufacturer_name"][0] #Empresa

            contenido+= "<tr>\n   <td><p style='font-size:12px'>" + id+ '</p></td>\n'
            contenido+= "<td><p style='font-size:12px'>" +'<li>'+ name+ '</li>'+'</p></td>\n'
            contenido+= "<td><p style='font-size:12px'>" +manufacturer + '</p></td>\n'
            contenido+= "<td><p style='font-size:12px'>"  +purpose+ '</p></td>\n  </tr>\n'


        return contenido

    def get_listCompanies(self, limit): #Crea y devuelve el contenido referente al listado de empresas

        info=self.get_conection(limit) #Establece la conexión con OpenFDA
        drug=info["results"]
        #Busca la información referente a las empresas junto al identificador del medicamento correspondiente y 
        # lo va introduciendo en una tabla
        contenido = (' <!DOCTYPE html>\n'
           '<html lang="es">\n'
           '<head>\n'
           '    <meta charset="UTF-8">\n'
           '    <title>API</title>\n'
           '</head>\n'
           '<body style="background: linear-gradient(to right, #c39bd3, #5b2c6f)">\n'
           '<h1>Obtención de datos Openfda:</h2>\n'
           '<img src="https://2.bp.blogspot.com/-_QDuJunXuyM/WJxbPq_5XsI/AAAAAAAASls/84d8ZrZYoCMyt_jigvCRmqGxJjITZjjcACLcB/s1600/medico.jpg" border="1" width="500" height="500" align="right">'
           '<h3>ListCompanies</h3>'
           '\n'
           '<table style="width:50%" border="4">\n'
           '<tr>\n'
             '<th>Identificador</th>\n'
             '<th>Empresa</th>\n'
            '</tr>\n')

        for i in range(len(drug)):
            id= drug[i]["id"]
            if drug[i]["openfda"]:
                manufacturer=drug[i]["openfda"]["manufacturer_name"][0]
            else:
                manufacturer="Desconocido"

            contenido+= "<tr>\n   <td><p style='font-size:12px'>" + id+ '</p></td>\n'
            contenido+= "<td><p style='font-size:12px'>" + '<li>' +manufacturer+'</li>'+ '</p></td>\n  </tr>\n'


        return contenido

    def get_listWarnings(self, limit): #Crea el html con el identificador del medicamento y sus advertencias

        info=self.get_conection(limit)
        drug=info['results']

        contenido = (' <!DOCTYPE html>\n'
           '<html lang="es">\n'
           '<head>\n'
           '    <meta charset="UTF-8">\n'
           '    <title>API</title>\n'
           '</head>\n'
           '<body style="background: linear-gradient(to right,  #f5cba7 ,  #d35400)">\n'
           '<h1>Obtención de datos Openfda:</h2>\n'
           '<img src="https://2.bp.blogspot.com/-_QDuJunXuyM/WJxbPq_5XsI/AAAAAAAASls/84d8ZrZYoCMyt_jigvCRmqGxJjITZjjcACLcB/s1600/medico.jpg" border="1" width="500" height="500" align="right">'
           '<h3>ListWARNINGS</h3>'
           '\n'
           '<table style="width:50%" border="4">\n'
           '<tr>\n'
             '<th>Identificador</th>\n'
             '<th>Precauciones</th>\n'
            '</tr>\n')

        for i in range(len(drug)):
            id= drug[i]["id"] #Identificador

            if "warnings" in drug[i].keys():
                warning=drug[i]['warnings'][0] #Advertencias
            else:
                warning = "Desconocido"

            contenido+= "<tr>\n   <td><p style='font-size:12px'>" + id+ '</p></td>\n'
            contenido+= "<td><p style='font-size:12px'>" + '<li>' +warning+'</li>'+ '</p></td>\n  </tr>\n'

        return contenido


    def get_searchDrug(self, limit, busqueda, name): #Crea y devuelve el html con el identificador de los fármacos con ese principio activo

        info=self.get_conection(limit, busqueda, name)
        drug=info["results"]

        contenido = (' <!DOCTYPE html>\n'
           '<html lang="es">\n'
           '<head>\n'
           '    <meta charset="UTF-8">\n'
           '    <title>API</title>\n'
           '</head>\n'
           '<body style="background: linear-gradient(to right,  #e6b0aa , #922b21)">\n'
           '<h1>Obtención de datos Openfda:</h2>\n'
           '<img src="https://2.bp.blogspot.com/-_QDuJunXuyM/WJxbPq_5XsI/AAAAAAAASls/84d8ZrZYoCMyt_jigvCRmqGxJjITZjjcACLcB/s1600/medico.jpg" border="1" width="500" height="500" align="right">'
           '<h3>SearchDRUG</h3>'
           '\n'
           '<table style="width:50%" border="4">\n'
           '<tr>\n'
           '<th><p style="color:white;"style="font-size:50px;">IDENTIFICADORES de fármacos con este principio</p>\n')

        for i in range(len(drug)):
            id= drug[i]["id"] #Identificador

            contenido+= "<tr>\n   <th><p style='font-size:12px'>" + '<li>' +id+'</li>'+ '</p></th>\n  </tr>\n'


        return contenido

    def get_searchCompany(self,limit, busqueda, name): #Crea y devuelve el html con los identificadores de los medicamento creados 
                                                       #por la empresa buscada, junto a su nombre, y los introduce en una tabla.
        info=self.get_conection(limit, busqueda, name)
        drug=info["results"]

        contenido = (' <!DOCTYPE html>\n'
           '<html lang="es">\n'
           '<head>\n'
           '    <meta charset="UTF-8">\n'
           '    <title>API</title>\n'
           '</head>\n'
           '<body style="background: linear-gradient(to right,   #a9cce3 ,   #21618c )">\n'
           '<h1>Obtención de datos Openfda:</h2>\n'
           '<img src="https://2.bp.blogspot.com/-_QDuJunXuyM/WJxbPq_5XsI/AAAAAAAASls/84d8ZrZYoCMyt_jigvCRmqGxJjITZjjcACLcB/s1600/medico.jpg" border="1" width="500" height="500" align="right">'
           '<h3>SearchCompanies</h3>'
           '\n'
           '<table style="width:50%" border="4">\n'
           '<tr>\n'
             '<th>Identificador</th>\n'
             '<th>Empresa</th>\n'
            '</tr>\n')


        for i in range(len(drug)):
            id= drug[i]["id"] #Identificador
            manufacturer=drug[i]["openfda"]["manufacturer_name"][0] #Empresa

            contenido+= "<tr>\n   <td><p style='font-size:12px'>" + id+ '</p></td>\n'
            contenido+= "<td><p style='font-size:12px'>" + '<li>' +manufacturer+'</li>'+ '</p></td>\n  </tr>\n'

        return contenido



    def do_GET(self): 
    #Se invoca directamente desde la librería al recibir una petición, la cual quedará almacenada en self.path. Es aquí donde comienza
    #nuestro programa.
    
        path=self.path #Abreviamos el nombre

        if '&' in path:                  #Sustituimos este carácter para procesar de la misma forma los parámetros procedentes 
            path=path.replace('&', '?')  #de los apartados de búsqueda del formulario, para los cuales el parámetro limit, en lugar de
                                         #comenzar en '?', comienza con '&'.

        if '%3C' in path:                                   #Eliminamos los caracteres que aparecen como consecuencia de los signos
            path=path.replace("%3C", "").replace("%3E", "") # '<>', para así poder quedarnos solamente con el nombre que se desee buscar
            print(path)                                     #en los apartados de searchy establecer una conexión adecuada con la API.


        if '?' in path: #Se asegura de que exista al menos un parámetro.

            parametros=path.split("?")[1:] #Se queda únicamente con los parámetros

            solicitud=path.split("?")[0] #Se queda con el recurso solicitado, sin los parámetros
            print("Solicitud:", solicitud)

            for i in range(len(parametros)):
                parameters=parametros[i].split("=") #Divide cada parámetro en el nombre o número correspondiente a la búsqueda
                                                    # y su respectiva variable, y las separa como elementos de una lista sobre la que
                                                    # poder iterar.
                if parameters[0]=='limit':#Si la variable es la palabra "limit", almacena el valor correspondiente al dato que acompaña.
                    limit=parameters[1]
                    print("Límite:", limit)

                else: #Si aparecen parámetros, pero no el referente al límite, le establece un valor por defecto.
                    limit=10 

                if parameters[0]=="company": #Si la variable es company (searchCompany), almacena el valor correspondiente 
                    name=parameters[1]       #al dato que acompaña (name), así como la propia variable (busqueda).
                    busqueda= "manufacturer_name"
                    print("Nombre:", name)
                    print("Búsqueda:", busqueda)


                if parameters[0]=='active_ingredient': #Si la variable es active_ingredient (searchDrug), almacena el valor correspondiente
                    name=parameters[1]                 #al dato que acompaña (name), así como la propia variable (busqueda).
                    busqueda=parameters[0]
                    print("Nombre:", name)
                    print("Búsqueda:", busqueda)

        else: #Si no hay parámetros en la búsqueda, establece un valor por defecto.
            limit=10
            solicitud=""

        print('Número de recursos solicitados:', limit)


        if self.path=="/" or self.path=="": 
            mensaje=self.get_index() #Determina que el mensaje sea el formulario
            self.send_response(200) #Indicamos el estatus 200 OK en la primera línea del mensaje de respuesta.
            self.send_header('Content-type', 'text/html') #Indicamos en la cabecera del mensaje que el contenido será un texto en html.
            self.end_headers()
            self.wfile.write(bytes(mensaje, "utf8")) #Enviamos todo el mensaje

        elif path== '/listDrugs' or path== '/listDrugs?limit={}'.format(limit):
            mensaje = self.get_listDrugs(limit) #Determina que el mensaje sea el listado de fármacos, cuya función será capaz de 
            self.send_response(200)             #conectarse con OpenFDA pasándole los parámetros que se han recibido en esta misma función.
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(mensaje, "utf8"))

        elif path=='/listCompanies' or path== '/listCompanies?limit={}'.format(limit):
            mensaje= self.get_listCompanies(limit) #Listado de empresas
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(mensaje, "utf8"))

        elif path=='/listWarnings' or path=='/listWarnings?limit={}'.format(limit):
            mensaje=self.get_listWarnings(limit) #Listado de advertencias
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(mensaje, "utf8"))

        elif solicitud=="/searchDrug": 
            mensaje=self.get_searchDrug(limit, busqueda, name) #Búsqueda de fármacos
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(mensaje, "utf8"))

        elif solicitud=="/searchCompany":
            mensaje=self.get_searchCompany(limit, busqueda, name) #Búsqueda de empresas.
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(mensaje, "utf8"))

        elif path=='/secret': #Envía el código 401 y una página de advertencia
            self.send_error(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()

        elif  path=='/redirect': #Envía el código 302 y redirige a la página
            self.send_response(302)
            self.send_header('Location', 'http://localhost:'+str(PORT))
            self.end_headers()

        else: #Si no se reconoce la petición, envía el status 404 de error y el mensaje de advertencia, que, en este caso, no será del
              #tipo html
            self.send_error(404) 
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("I don't know '{}'.".format(path).encode())

        print('Lista enviada')

        return
#---------------------------------------------------------------------------------------------------------

Handler = TestHTTPRequestHandler #Establecemos nuestra clase como manejador

httpd = socketserver.TCPServer(("", PORT), Handler) #Creamos el socket para establecer las conexiones con el cliente.
print("Sirviendo en el puerto", PORT)

try:
    httpd.serve_forever() #Permite que el servidor permanezca a la escucha, ejecutando en cada petición que recibe el método do_GET.
except KeyboardInterrupt:
    print("")
    print("Interrumpido por el usuario")

print("")
print("Servidor parado")
