from socket import *

serverPort = 12000 #define em qual porta o socket irá executar
serverSocket = socket(AF_INET,SOCK_STREAM) #cria um socket TCP
serverSocket.bind(('',serverPort)) #atrela ao socket o localhost e a porta de escuta
serverSocket.listen(1) #começa a escutar

print('The server is ready to receive')

while 1:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024)
    capitalizedSentence = bytes("Apagardeblio", 'utf-8')
    connectionSocket.send(capitalizedSentence)
    connectionSocket.close()