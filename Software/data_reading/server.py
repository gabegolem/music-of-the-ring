import socket
import struct
import csv
from collections import deque
import time

NUM_READINGS = 40
PIEZO_THRESHOLD = 1000
CSV = "../modeling/punch_data/cross.csv"


format_string = '<7d'
struct_size = struct.calcsize(format_string)

queue = deque(maxlen=NUM_READINGS)

csv_file = open(CSV,'a',newline='')
csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ("10.0.0.210", 8000)
server_socket.bind(address)
print("Listening...")
server_socket.listen(1)

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")
    try:
        data_bytes = client_socket.recv(56)
        unpacked_data = struct.unpack(format_string, data_bytes)
        queue.append(unpacked_data)
        if (unpacked_data[6] > PIEZO_THRESHOLD):
            for i in range(len(queue)):
                csv_writer.writerow(queue[i])
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
