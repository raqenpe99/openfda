import http.server
import http.client
import socketserver
import json

PORT = 8000
socketserver.TCPServer.allow_reuse_address = True

class TestHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def get_conection(self, limit=1, busqueda="", name=""):

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
            <p><h2>Listado de medicamentos:</h2></p>
            <p><form action="listDrugs">
                  Limite:<input type="text" name='limit' value="1">
            <p><input type="submit" value="Aceptar"></p>
            </form>

            <p><h2>Listado de empresas:</h2></p>
            <form action = "listCompanies" method="get">
                  Limite: <input type="text" name="limit" value="1">
            <input type="submit" value="Aceptar">

            </form>

            <p><h2>Busqueda de farmacos:</h2></p>
            <form action = "searchDrug" method="get">
                  Principio activo: <input type="text" name="active_ingredient" value="acetylsalicylic">
                  Limite: <input type="text" name="limit" value="1">

            <input type="submit" value="Aceptar">

            </form>

            <p><h2>Busqueda de empresas:</h2></p>
            <form action = "searchCompany" method="get">
                  Empresa: <input type="text" name="company" value="carefusion">
                  Limite: <input type="text" name="limit" value="1">

            <input type="submit" value="Aceptar">

            </form>

            <p><h2>Busqueda de precauciones:</h2></p>
            <form action = "listWarnings" method="get">
                  Limite: <input type="text" name="limit" value="1">

            <input type="submit" value="Aceptar">

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
           '</head>\n'
           '<body>\n'
           '<p>Nombre.  Fabricante. ID. Propósito</p>'
           '\n')

        for i in range(len(drug)):
            id= drug[i]["id"]
            purpose=drug[i].get("purpose", ["No aparece información al respecto"])[0]

            if drug[i]["openfda"]:
                name=drug[i]["openfda"]["generic_name"][0]
                manufacturer= drug[i]["openfda"]["manufacturer_name"][0]

            contenido+= '<li>' + name+manufacturer+id+purpose+'</li>'

        return contenido

    def get_listCompanies(self, limit):

        info=self.get_conection(limit)
        drug=info["results"]

        contenido = (' <!DOCTYPE html>\n'
               '<html lang="es">\n'
               '<head>\n'
               '    <meta charset="UTF-8">\n'
               '</head>\n'
               '<body>\n'
               '<p>Fabricantes</p>'
               '\n')

        for i in range(len(drug)):
            if drug[i]["openfda"]:
                manufacturer=drug[i]["openfda"]["manufacturer_name"][0]
            else:
                manufacturer="Desconocido"

            contenido+= '<li>'+manufacturer+'</li>'

        return contenido

    def get_listWarnings(self, limit):

        info=self.get_conection(limit)
        drug=info['results']

        contenido = (' <!DOCTYPE html>\n'
               '<html lang="es">\n'
               '<head>\n'
               '    <meta charset="UTF-8">\n'
               '</head>\n'
               '<body>\n'
               '<p>Precauciones</p>'
               '\n')

        for i in range(len(drug)):

            if "warnings" in drug[i].keys():
                warning=drug[i]['warnings'][0]
            else:
                warning = "Desconocido"

            contenido+= '<li>' + warning+'</li>'

        return contenido


    def get_searchDrug(self, limit, busqueda, name):

        info=self.get_conection(limit, busqueda, name)
        drug=info["results"]

        contenido = (' <!DOCTYPE html>\n'
               '<html lang="es">\n'
               '<head>\n'
               '    <meta charset="UTF-8">\n'
               '</head>\n'
               '<body>\n'
               '<p>Identifiadores de los farmacos con ese principio activo</p>'
               '\n')

        for i in range(len(drug)):
            id= drug[i]["id"]

            contenido+= '<li>'+id+'</li>'

        return contenido

    def get_searchCompany(self,limit, busqueda, name):

        info=self.get_conection(limit, busqueda, name)
        drug=info["results"]

        contenido = (' <!DOCTYPE html>\n'
       '<html lang="es">\n'
       '<head>\n'
       '    <meta charset="UTF-8">\n'
       '</head>\n'
       '<body>\n'
       '<p>Empresas</p>'
       '\n')

        for i in range(len(drug)):
            id= drug[i]["id"]
            manufacturer=drug[i]["openfda"]["manufacturer_name"][0]

            contenido+= '<li>'+id+manufacturer+'</li>'

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
                    limit=1

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
            limit=1
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
