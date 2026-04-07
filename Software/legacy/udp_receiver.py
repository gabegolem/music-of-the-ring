import socket
import struct
import os
from collections import deque
import time

NUM_READINGS = 100              #Readings per punch
NUM_READINGS_AFTER = 5        #Number of readings following impact 
PIEZO_THRESHOLD = 1000         #Threshold to register/record a punch 
pipe_path = "named_pipe.fifo"

format_string = '<7dL'          #Sets byte reading using format specifiers 
struct_size = struct.calcsize(format_string) #Sets size to size of 7 floats and 1 unsigned long (64 bytes) 

queue = deque(maxlen=NUM_READINGS) #Creates queue to store readings

'''Sets up pipe'''
named_pipe = open(pipe_path, "w")

'''Sets up udp socket communication'''
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = ''
port = 8000
address = ('', port)
sock.bind(address)
cooldown = 0
print("Waiting...")

'''Displays received data for debugging'''
def displayData(unpacked_data): 
        acceleration_x = unpacked_data[0]
        acceleration_y = unpacked_data[1]
        acceleration_z = unpacked_data[2]
        gyro_x = unpacked_data[3]
        gyro_y = unpacked_data[4]
        gyro_z = unpacked_data[5]
        piezo = unpacked_data[6]
        timestamp = unpacked_data[7]
        csv_writer.writerow(unpacked_data)
        print(f"""Received from client: 
              \nAcc_x: {acceleration_x}
              \nAcc_y: {acceleration_y}
              \nAcc_z: {acceleration_z}
              \nGyro_x: {gyro_x}
              \nGyro_y: {gyro_y}
              \nGyro_z: {gyro_z}
              \nPiezo: {piezo}
              \nTimestamp: {timestamp}
        """)


while True:
    data_bytes, address = sock.recvfrom(struct_size)                      #Receives struct_size bytes
    unpacked_data = struct.unpack(format_string, data_bytes) #Unpacks into list of floats
    queue.append(unpacked_data) #Adds data to queue, automatically dequeueing extra values
    print(f"Accepted: {str(queue[0])}")
    if (queue[0][6] > PIEZO_THRESHOLD and (cooldown == 0)):#If impact threshold is met   
        cooldown = 100
        for i in range(len(queue)):                          #Writes current queue to csv
            named_pipe.write(str(queue[i]))
        named_pipe.flush()
    else:
        if (cooldown > 0):
            cooldown -= 1
    #displayData(unpacked_data)
named_pipe.close()
sock.close()
