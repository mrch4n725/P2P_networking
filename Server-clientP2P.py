import socket
import threading
import os
import random
import tkinter as tk

SHARED_DIR = "shared_files"
if not os.path.exists(SHARED_DIR):
    os.makedirs(SHARED_DIR)


def handle_client(conn):
    while True:
        filename = conn.recv(1024).decode('utf-8')
        if not filename:
            break
        if os.path.exists(filename):
            conn.send(b"EXISTS "+str(os.path.getsize(filename)).encode('utf-8'))
            with open(filename, 'rb') as f:
                bytes_read = f.read(1024)
                while bytes_read:
                    conn.send(bytes_read)
                    bytes_read = f.read(1024)
                print(f"Sent: {filename}")
        else:
            conn.send(b"ERR")
        
        conn.close()

def start_server(host='0.0.0.0', port=12345):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)
    print(f"Listening on {host}:{port}")
    while True:
        conn, addr = sock.accept()
        print(f"Connected by {addr}")
        threading.Thread(target=handle_client, args=(conn,)).start()

def request_file(host='localhost', port=12345, filename=''):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except ConnectionRefusedError:
        print("Connection refused - Is the server running and reachable?")
        sock.close()
        return
    filepath = os.path.join(SHARED_DIR, filename)
    file_save_as = str(random.random()) + "_"+filename
    sock.sendall(filepath.encode('utf-8'))

    response = sock.recv(1024).decode('utf-8')

    if response.startswith("EXISTS"):
        filesize = int(response.split()[1])
        print(f"File exists, size: {filesize} bytes. Downloading....")
        
        filepath = os.path.join(os.getcwd(), file_save_as)
        with open(filepath,'wb') as f:
            bytes_received = 0
            while bytes_received < filesize:
                bytes_read = sock.recv(1024)
                if not bytes_read:
                    break
                f.write(bytes_read)
                bytes_received += len(bytes_read)
        
        print(f"Downloaded: {file_save_as}")

    else:
        print("File does not exist on the server.")

    sock.close()

if __name__ =="__main__":
    choice = input("Start server (s) or request file (r)? ")

    if choice.lower() == 's':
        start_server()
    elif choice.lower() == 'r':
        filename = input("Enter the filename to request: ")
        request_file(filename=filename)
    
    