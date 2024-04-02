from socket import *

serverName = "127.0.0.1" #ip do socket
serverPort = 80 #cria socket TCP, porta 8080

clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

# sentence = "PUT /new.html HTTP/1.1\n\n<html><br><head><br><title>New page</title><br></head><br><body><br><p>New file</p><br></body><br></html>"
sentence = "GET /index.html HTTP/1.1"

#Envia a mensagem:
sen = sentence.encode() #formata a mensagem
clientSocket.send(sen) #envia
modifiedSentence = clientSocket.recv(1024) #recebe a resposta
print("From server:", modifiedSentence.decode())
clientSocket.close() #encerra a conexão