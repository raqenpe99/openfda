import http.server
import http.client
import socketserver
import json

PORT = 8000
socketserver.TCPServer.allow_reuse_address = True

class TestHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def get_conection(self, limit=10, busqueda="", name=""):

        headers = {'User-Agent': 'http-client'}
        peticion= "/drug/label.json?limit={}".format(limit)

        if busqueda != "":
            peticion += '&search='+busqueda+':'+ name

        print("Recurso solicitado: {}".format(peticion))

        conexion = http.client.HTTPSConnection("api.fda.gov")
        conexion.request("GET", peticion , None, headers)


        JSON = conexion.getresponse()

        if JSON.status == 404:
            print("ERROR. Recurso no encontrado")
            exit(1)

        print(JSON.status, JSON.reason)
        info = json.loads(JSON.read().decode("utf-8"))

        conexion.close()

        return info

    def get_index(self):
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


    def get_listDrugs(self, limit):

        info=self.get_conection(limit)
        drug=info["results"]
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
            id= drug[i]["id"]
            purpose=drug[i].get("purpose", ["No aparece información al respecto"])[0]

            if drug[i]["openfda"]:
                name=drug[i]["openfda"]["generic_name"][0]
                manufacturer= drug[i]["openfda"]["manufacturer_name"][0]

            contenido+= "<tr>\n   <td><p style='font-size:12px'>" + id+ '</p></td>\n'
            contenido+= "<td><p style='font-size:12px'>" +'<li>'+ name+ '</li>'+'</p></td>\n'
            contenido+= "<td><p style='font-size:12px'>" +manufacturer + '</p></td>\n'
            contenido+= "<td><p style='font-size:12px'>"  +purpose+ '</p></td>\n  </tr>\n'


        return contenido

    def get_listCompanies(self, limit):

        info=self.get_conection(limit)
        drug=info["results"]

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

    def get_listWarnings(self, limit):

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
            id= drug[i]["id"]

            if "warnings" in drug[i].keys():
                warning=drug[i]['warnings'][0]
            else:
                warning = "Desconocido"

            contenido+= "<tr>\n   <td><p style='font-size:12px'>" + id+ '</p></td>\n'
            contenido+= "<td><p style='font-size:12px'>" + '<li>' +warning+'</li>'+ '</p></td>\n  </tr>\n'

        return contenido


    def get_searchDrug(self, limit, busqueda, name):

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
            id= drug[i]["id"]

            contenido+= "<tr>\n   <th><p style='font-size:12px'>" + '<li>' +id+'</li>'+ '</p></th>\n  </tr>\n'


        return contenido

    def get_searchCompany(self,limit, busqueda, name):

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
            id= drug[i]["id"]
            manufacturer=drug[i]["openfda"]["manufacturer_name"][0]

            contenido+= "<tr>\n   <td><p style='font-size:12px'>" + id+ '</p></td>\n'
            contenido+= "<td><p style='font-size:12px'>" + '<li>' +manufacturer+'</li>'+ '</p></td>\n  </tr>\n'

        return contenido



    def do_GET(self):

        path=self.path

        if '&' in path:
            path=path.replace('&', '?')

        if '%3C' in path:
            path=path.replace("%3C", "").replace("%3E", "")
            print(self.path)


        if '?' in path:

            parametros=path.split("?")[1:]

            solicitud=path.split("?")[0]
            print("Solicitud:", solicitud)

            for i in range(len(parametros)):
                parameters=parametros[i].split("=")


                if parameters[0]=='limit':
                    limit=parameters[1]
                    print("Límite:", limit)

                else:
                    limit=10

                if parameters[0]=="company":
                    name=parameters[1]
                    busqueda= "manufacturer_name"
                    print("Nombre:", name)
                    print("Búsqueda:", busqueda)


                if parameters[0]=='active_ingredient':
                    name=parameters[1]
                    busqueda=parameters[0]
                    print("Nombre:", name)
                    print("Búsqueda:", busqueda)

        else:
            limit=10
            solicitud=""

        print('Número de recursos solicitados:', limit)


        if self.path=="/" or self.path=="":
            mensaje=self.get_index()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(mensaje, "utf8"))

        elif path== '/listDrugs' or path== '/listDrugs?limit={}'.format(limit):
            mensaje = self.get_listDrugs(limit)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(mensaje, "utf8"))

        elif path=='/listCompanies' or path== '/listCompanies?limit={}'.format(limit):
            mensaje= self.get_listCompanies(limit)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(mensaje, "utf8"))

        elif path=='/listWarnings' or path=='/listWarnings?limit={}'.format(limit):
            mensaje=self.get_listWarnings(limit)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(mensaje, "utf8"))

        elif solicitud=="/searchDrug":
            mensaje=self.get_searchDrug(limit, busqueda, name)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(mensaje, "utf8"))

        elif solicitud=="/searchCompany":
            mensaje=self.get_searchCompany(limit, busqueda, name)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(mensaje, "utf8"))

        elif path=='/secret':
            self.send_error(401)
            self.send_header('WWW-Authenticate', 'Basic realm="Mi servidor"')
            self.end_headers()

        elif  path=='/redirect':
            self.send_response(302)
            self.send_header('Location', 'http://localhost:'+str(PORT))
            self.end_headers()

        else:

            self.send_error(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("I don't know '{}'.".format(path).encode())

        print('Lista enviada')

        return


Handler = TestHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("Sirviendo en el puerto", PORT)

try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("")
    print("Interrumpido por el usuario")

print("")
print("Servidor parado")
