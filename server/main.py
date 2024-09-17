from servidor import Servidor
HOST = '127.0.0.1'  
PORT = 65432   
server = Servidor(PORT, HOST)
server.start_server()
    