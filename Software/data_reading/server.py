import socket
import struct
import csv
from collections import deque
import time

NUM_READINGS = 40              #Readings per punch
NUM_READINGS_AFTER = 10        #Number of readings following impact 
PIEZO_THRESHOLD = 1000         #Threshold to register/record a punch 
CSV = "../modeling/sample.csv" #"../modeling/profiles/test_profile/data/right_hook.csv"


format_string = '<7d'          #Sets byte reading to 7 little-endian floats 
struct_size = struct.calcsize(format_string) #Sets size to size of 7 floats (56 bytes) 

queue = deque(maxlen=NUM_READINGS) #Creates queue to store readings

'''Sets up csv'''
csv_file = open(CSV,'a',newline='')
csv_writer = csv.writer(csv_file, delimiter=',', lineterminator='\n')

'''Sets up tcp socket communication'''
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ("10.0.0.210", 8000)
server_socket.bind(address)
print("Listening...")
server_socket.listen(1)

'''Displays received data for debugging'''
def displayData(unpacked_data): 
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
              \nGyro_z: {gyro_zi}
        """)


while True:
    client_socket, client_address = server_socket.accept()
    #print("Accepted")
    try:
        data_bytes = client_socket.recv(56)                      #Receives struct_size bytes
        unpacked_data = struct.unpack(format_string, data_bytes) #Unpacks into list of floats
        queue.append(unpacked_data) #Adds data to queue, automatically dequeueing extra values
        if (queue[-NUM_READINGS_AFTER][6] > PIEZO_THRESHOLD):    #If impact threshold is met   
            for i in range(len(queue)):                          #Writes current queue to csv
                csv_writer.writerow(queue[i])

        #displayData(unpacked_data)
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()
