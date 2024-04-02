#implementação de um servidor base para interpratação de métodos HTTP

import socket

def file_is_principal(filename):
    principal = ["index.html", "ipsum.html"]
    if filename in principal:
        return True
    else:
        return False

files = ["index.html", "ipsum.html"]

#definindo o endereço IP do host
SERVER_HOST = ''
#definindo o número da porta em que o servidor irá escutar pelas requisições HTTP
SERVER_PORT = 80

#tipos de extensão a serem passadas pelo servidor na resposta
tipo_binario = ['ico', 'png', 'jpeg']
 
#vamos criar o socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#vamos setar a opção de reutilizar sockets já abertos
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#atrela o socket ao endereço da máquina e ao número de porta definido
server_socket.bind((SERVER_HOST, SERVER_PORT))

#coloca o socket para escutar por conexões
server_socket.listen(1)

#mensagem inicial do servidor
print("Servidor em execução...")
print("Escutando por conexões na porta %s" % SERVER_PORT)



#cria o while que irá receber as conexões
while True:
    #espera por conexões
    #client_connection: o socket que será criado para trocar dados com o cliente de forma dedicada
    #client_address: tupla (IP do cliente, Porta do cliente)
    client_connection, client_address = server_socket.accept()

    print("Conectado")


    #pega a solicitação do cliente

    request = client_connection.recv(1024).decode()

    #while True:
       # data = client_connection.recv(1024)
       # if data == b'\r\n': break
       # print("Received data:", data)
       # request += data.decode()
        
    print(request)
       
    #verifica se a request possui algum conteúdo (pois alguns navegadores ficam periodicamente enviando alguma string vazia)
    if request:
        #imprime a solicitação do cliente
        print(request, "\n")
        
        #analisa a solicitação HTTP
        headers = request.split("\n")
        protocol = headers[0].split()[2]

        if (protocol == "HTTP/1.1"):
            method = headers[0].split()[0]
            filename = headers[0].split()[1][1:]
            extension = filename.split('.')[-1]

            #MÉTODO GET
            if method == "GET":
                #pega o nome do arquivo sendo solicitado
                if filename == '':
                    filename = 'index.html'

                #define se o arquivo sendo solicitado é binário ou não
                arquivo_binario = False
                if extension in tipo_binario:
                    arquivo_binario = True

                #try e except para tratamento de erro quando um arquivo solicitado não existir
                try:
                    #abrir o arquivo e enviar para o cliente
                    if arquivo_binario == True:
                        fin = open(filename, 'rb')
                    else:
                        fin = open(filename, 'r', encoding='utf-8')

                    #leio o conteúdo do arquivo para uma variável
                    content = fin.read()    
                    #fecho o arquivo
                    fin.close()

                    #gera a resposta a ser passada para o navegador
                    if arquivo_binario:
                        response = ("HTTP/1.1 200 OK\n\n").encode() + content
                    else:
                        response = ("HTTP/1.1 200 OK\n\n" + content).encode()
            
                #caso o arquivo solicitado não exista no servidor, gera uma resposta de erro
                except FileNotFoundError:
                    response = ('HTTP/1.1 404 NOT FOUND\n\n<h1>ERROR 404!<br>File Not Found!</h1>').encode()
                
            #MÉTODO PUT
            elif method == "PUT":
                content = headers[2]
                
                if file_is_principal(filename):
                    response = ("HTTP1.1 403 FORBIDDEN\n\n<h1>ERROR 403!<br>Forbidden.</h1>").encode()
                else:
                    if filename in files:
                        with open(filename, "w") as arquivo:
                            arquivo.write(content)
                        response = ("HTTP1.1 200 OK\n\n" + content).encode()
                        arquivo.close()
                    else:
                        filename.touch()
                        with open(filename, "w") as arquivo:
                            arquivo.write(content)
                        response = ("HTTP1.1 201 CREATED\n\n" + content).encode()
                        arquivo.close()
                        files.append("filename")
                        print("files")
            
            else:
                response = ("HTTP1.1 501 NOT IMPLEMENTED\n\n<h1>ERROR 501!<br>Unsupported method</h1>")
        
        elif (protocol != "HTTP/1.1"):
            response = ("HTTP1.1 505 VERSION NOT SUPPORTED\n\n<h1>ERROR 505!<br>The HTTP version used in the request is not supported by the server</br>").encode()
       
        #envia a resposta HTTP
        client_connection.sendall(response)
        client_connection.close()

server_socket.close()
