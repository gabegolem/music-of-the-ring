import socket
import struct
import csv

format_string = '<7d'
struct_size = struct.calcsize(format_string)


csv_file = open('readings.csv','a',newline='')
csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ("10.98.148.138", 8000)
server_socket.bind(address)
print("Listening...")
server_socket.listen(5)

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")
    try:
        data_bytes = client_socket.recv(56)
        unpacked_data = struct.unpack(format_string, data_bytes)
        if (unpacked_data[6] > 500):
            csv_writer.writerow(unpacked_data)
        '''
        acceleration_x = unpacked_data[0]
        acceleration_y = unpacked_data[1]
        acceleration_z = unpacked_data[2]
        gyro_x = unpacked_data[3]
        gyro_y = unpacked_data[4]
        gyro_z = unpacked_data[5]
        piezo = unpacked_data[6]
        csv_writer.writerow(unpacked_data)
        print(f"""Received from client: 
              \nAcc_x: {acceleration_x}
              \nAcc_y: {acceleration_y}
              \nAcc_z: {acceleration_z}
              \nGyro_x: {gyro_x}
              \nGyro_y: {gyro_y}
              \nGyro_z: {gyro_z}
              \nPiezo: {piezo}\n""")
        '''
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()
