import csv
import os
import math
import statistics
import sys

from pythonosc import dispatcher
from pythonosc import osc_server
from pythonosc import udp_client

disp = dispatcher.Dispatcher()

def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")

disp.set_default_handler(default_handler)

server_ip = "192.168.50.197"
server_port = 8000

server = osc_server.ThreadingOSCUDPServer((server_ip, server_port), disp)
print(f"Serving on {server.server_address}")

client_ip = "127.0.0.1"
client_port = 8001

client = udp_client.SimpleUDPClient(client_ip, client_port)


if (len(sys.argv) != 3):
    print("Usage: python identify.py [profile] [log_file]")
    exit(-1)


READINGS_PER_PUNCH = 20 #40
NUM_VALUES = 7
PROFILE = sys.argv[1]
CENTROIDS_DIR = "./profiles/" + PROFILE + "/centroids/"
PUNCH_FILE = sys.argv[2]

'''
Finds euclidean distance between a punch and
centroid at a point in time.
'''
def euclidean_distance(punch, centroid, dimensions=6):
    summation = 0
    avg_error = [0] * dimensions
    for i in range(dimensions):
        summation += (float(punch[i]) + float(centroid[i])) ** 2
        avg_error[i] += abs(float(centroid[i]) - float(punch[i]))
    for i in range(dimensions):
        avg_error[i] = avg_error[i] / READINGS_PER_PUNCH
    return (math.sqrt(summation), avg_error)

translator = {
CENTROIDS_DIR + "cross_centroid.csv" : 0,
CENTROIDS_DIR + "right_hook_centroid.csv" : 1,
CENTROIDS_DIR + "jab_centroid.csv" : 2,
CENTROIDS_DIR + "left_hook_centroid.csv" : 3,
CENTROIDS_DIR + "uppercut_centroid.csv" : 4
}

def handler(address, *args):

    outmsg = []        

    distances = [0] * READINGS_PER_PUNCH
    deviations = dict()

    for centroid_file in os.listdir(CENTROIDS_DIR):  #Iterates through all centroid csv files
        centroid_file = CENTROIDS_DIR + centroid_file
        
        centroid_csv = open(centroid_file,'r')       #Opens current csv
        centroid_reader = csv.reader(centroid_csv)   #Initializes a reader for current csv
        
        punch_csv = open(PUNCH_FILE, 'r')
        punch_reader = csv.reader(punch_csv)
        
        for i in range(READINGS_PER_PUNCH): #Stores distance of punch to centroid for each point in time
            current_punch = next(punch_reader)
            current_centroid = next(centroid_reader)
            eud = euclidean_distance(current_punch, current_centroid)
            distances[i] = eud[0]

            
        deviations[centroid_file] = (statistics.stdev(distances), eud[1]) #Stores punch compared to stdev of distances
        punch_csv.close()
        centroid_csv.close()

    min_deviation = min(deviations.items(), key=lambda item: item[1])
    print(min_deviation)
    
    outmsg.append(translator[min_deviation[0]])
    for z in range(len(args)):
        outmsg.append(args[z])

    for y in range(len(min_deviation[1][1])):
        outmsg.append(min_deviation[1][1][y])

    print(outmsg)
    client.send_message("/sonification", outmsg) 

    punch_csv.close()

disp.map("/modeling", handler)

server.serve_forever()
