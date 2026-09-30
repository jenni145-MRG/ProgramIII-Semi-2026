from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib import parse 
from urllib.parse import urlparse, parse_qs
import crud_clientes
import crud_tarifas
import crud_balances
import json

port = 3000
crudClientes = crud_clientes.crud_clientes()
crudTarifas = crud_tarifas.crud_tarifas()
crudBalances = crud_balances.crud_balances()

class miServidor(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        longitud = int(self.headers['Content-Length'])
        datos = self.rfile.read(longitud)
        datos = datos.decode("utf-8")
        datos = parse.unquote(datos)
        datos = json.loads(datos)
        
        # Limpiar la ruta quitando espacios o / al final
        ruta = urlparse(self.path).path.rstrip('/')

        print(f"[POST] Ruta recibida: '{self.path}' -> Ruta procesada: '{ruta}'")
        
        if ruta == "/cliente":
            respuesta = {'msg': crudClientes.administrar(datos)}
        elif ruta == "/tarifa":
            respuesta = {'msg': crudTarifas.administrar(datos)}
        elif ruta == "/balance":
            respuesta = {'msg': crudBalances.administrar(datos)}
        else:
            respuesta = {'msg': f'Ruta no encontrada ({self.path})'}

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(respuesta).encode("utf-8"))

    def do_GET(self):
        urlParse = urlparse(self.path)
        qs = parse_qs(urlParse.query)
        ruta = urlParse.path.rstrip('/')
       
        if ruta == "/clientes":
            buscar = qs.get('buscar', [''])[0]
            datos = crudClientes.consultar(buscar)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(datos, default=str).encode("utf-8"))
            
        elif ruta == "/tarifas":
            buscar = qs.get('buscar', [''])[0]
            datos = crudTarifas.consultar(buscar)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(datos, default=str).encode("utf-8"))

        elif ruta == "/balances":
            idCliente = qs.get('idCliente', [''])[0]
            datos = crudBalances.consultar(idCliente)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(datos, default=str).encode("utf-8"))
        
        elif self.path == "/":
            self.path = "/index.html"
            return SimpleHTTPRequestHandler.do_GET(self)

print(f"Servidor corriendo en el puerto {port}")
server = HTTPServer(("localhost", port), miServidor)
server.serve_forever()