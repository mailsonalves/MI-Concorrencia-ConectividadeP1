from cliente import Cliente

HOST = '127.0.0.1'  
PORT = 65432   
client = Cliente(PORT,HOST)
client.start_client()