import socket

IP = "127.0.0.1"
PORT = 9011
MAX_OPEN_REQUESTS = 5

def process_client(clientsocket):

    mensaje_solicitud = clientsocket.recv(1024).decode("utf-8")
    
    import json
    import urllib.request

    with urllib.request.urlopen("https://api.fda.gov/drug/label.json?limit=10") as API:
        info = json.loads(API.read().decode())
    
    def dame_nombres(info): #Nos devuelve en pantalla los nombres de cada medicamento y su posición en la lista que es capaz de 
                            #crear, por si es requerido el manejo de estos datos.
                            #Si no tiene nombre genérico, se almacena su identificador.
        nombres=[]
        for i in range(10):
            text = "Nombre genérico:" + info["results"][i]["openfda"].get("generic_name",  [info["results"][i]["id"]])[0]
            nombres.append(text)    
            print("Medicamento:", [i])
            print(text + "\n")
            
        return print("LISTA COMPLETADA")

    def crea_html(info): #Genera el contenido que será devuelto en un html, iterando sobre cada medicamento y agrupándo los nombres
                         #en una tabla
        contenido = """
        <!doctype html>
        <html>
          <head>
            <meta charset="utf-8">
            <title>API</title>
          </head>
           <body style='background: linear-gradient(to right, #D358F7, #FF0040)'>
              <h1>Obtención de datos Openfda:</h2>
              <p>Se expresan a continuación los nombres de diez medicamentos.</p>
              <p>Para más información sobre ellos, <a href="https://api.fda.gov/drug/label.json?limit=10">pulse aquí</a></p>
              <img src="https://2.bp.blogspot.com/-_QDuJunXuyM/WJxbPq_5XsI/AAAAAAAASls/84d8ZrZYoCMyt_jigvCRmqGxJjITZjjcACLcB/s1600/medico.jpg" border="1" width="500" height="500" align="right">
              <table style="width:50%" border="4">
              <tr>
              <th><p style="color:white;"style="font-size:50px;">NOMBRES</p>\n"""


        for i in range(10):
            text = str(info["results"][i]["openfda"].get("generic_name", ["No aparece información al respecto"])[0])
            contenido = str(contenido + "\n" + "<tr>\n   <th><p style='font-size:12px'>" + text + '</p></th>\n  </tr>\n')
            
        return contenido
            
        
    dame_nombres(info) #Llamamos a la función para que, una vez se haya realizado la petición, se imprima la información.

    linea_inicial = "HTTP/1.1 200 OK\n"
    cabecera = "Content-Type: text/html\n"
    cabecera += "Content-Length: {}\n".format(len(str.encode(crea_html(info)))) #El contenido será nuestra función html

    mensaje_respuesta = str.encode( linea_inicial + cabecera + "\n" + crea_html(info))  
    clientsocket.send(mensaje_respuesta)
    


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    serversocket.bind((IP, PORT))
    serversocket.listen(MAX_OPEN_REQUESTS)

    while True:
        print("Esperando clientes en IP: {}, Puerto: {}".format(IP, PORT))
        (clientsocket, address) = serversocket.accept()
        print("  Peticion de cliente recibida. IP: {}".format(address))
        process_client(clientsocket)
        clientsocket.close()

except socket.error:
    print("Problemas usando el puerto {}".format(PORT))
    print("Lanzalo en otro puerto (y verifica la IP)")
