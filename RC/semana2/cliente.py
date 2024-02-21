from socket import *

serverName = "127.0.0.1" #ip do socket
serverPort = 12000 #cria socket TCP, porta 12000

clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

sentence = input("Faça uma pergunta: ")
#ex: SOMA 5 5
#operações: SOMA - SUB - MULT - DIV

#Envia a mensagem:
sen = sentence.encode() #formata a mensagem
clientSocket.send(sen) #envia
modifiedSentence = clientSocket.recv(1024) #recebe a resposta
print("From server: ", modifiedSentence.decode())
clientSocket.close() #encerra a conexão