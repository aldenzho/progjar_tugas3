import socket
import json
import base64
import logging
import os

server_address = ('172.18.0.3', 60001)


def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(server_address)
        logging.warning(f"connecting to {server_address}")

        full_command = command_str + "\r\n\r\n"
        logging.warning(f"sending message")
        sock.sendall(full_command.encode())

        data_received = ""
        while True:
            data = sock.recv(16)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break

        data_received = data_received.replace("\r\n\r\n", "")

        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil

    except Exception as e:
        logging.warning(f"error during data receiving: {e}")
        return False

    finally:
        sock.close()

def remote_list():
    command_str=f"LIST"
    hasil = send_command(command_str)
    if (hasil['status']=='OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_upload(filepath=""):
    try:
        with open(filepath, 'rb') as f:
            filedata = f.read()
        filedata_base64 = base64.b64encode(filedata).decode()
        filename = os.path.basename(filepath)

        command_str = f"UPLOAD {filename} {filedata_base64}"

        hasil = send_command(command_str)

        if hasil['status'] == 'OK':
            print(f"Upload berhasil: {hasil['data']}")
        else:
            print(f"Gagal upload: {hasil['data']}")

        return hasil['status'] == 'OK'

    except Exception as e:
        print(f"Error saat upload: {str(e)}")
        return False

def remote_delete(filename=""):
    command_str = f"DELETE {filename}"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        print(f"Hapus berhasil: {hasil['data']}")
    else:
        print(f"Gagal hapus: {hasil['data']}")
    return hasil['status'] == 'OK'

if __name__ =='__main__':
    server_address = ('172.18.0.3', 60001)
    remote_list()
    # remote_get('pokijan.jpg')
    # remote_upload('pokijan.jpg')
    remote_upload('file_baru.txt')
    # remote_delete('file_baru.txt')
    remote_list()