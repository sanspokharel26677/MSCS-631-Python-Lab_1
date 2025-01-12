from socket import *

# Create a TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Bind the socket to the address and port
serverSocket.bind(('', 6789))  # '' allows connections from any IP
serverSocket.listen(1)  # Listen for 1 connection at a time

while True:
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()  # Wait for a client connection
    try:
        # Receive the HTTP request
        message = connectionSocket.recv(1024).decode()  # Decode bytes to string
        print(f"Request: {message}")

        # Parse the requested filename
        filename = message.split()[1]  # Extract "/HelloWorld.html"
        f = open(filename[1:], 'r')  # Remove the leading '/'

        # Read file content
        outputdata = f.read()

        # Send HTTP header
        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
        connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())

        # Send file content
        for i in outputdata:
            connectionSocket.send(i.encode())
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()
    except IOError:
        # Handle file not found
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
        connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
        connectionSocket.send("<html><body>404 Not Found</body></html>\r\n".encode())
        connectionSocket.close()

