import csv
import os
import math
import statistics
import sys

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
    for i in range(dimensions):
        summation += (float(punch[i]) + float(centroid[i])) ** 2
    return math.sqrt(summation)

distances = [0] * READINGS_PER_PUNCH
deviations = dict()

for centroid_file in os.listdir(CENTROIDS_DIR):  #Iterates through all centroid csv files
    centroid_file = CENTROIDS_DIR + centroid_file
    
    centroid_csv = open(centroid_file,'r')       #Opens current csv
    centroid_reader = csv.reader(centroid_csv)   #Initializes a reader for current csv
    
    punch_csv = open(PUNCH_FILE, 'r')
    punch_reader = csv.reader(punch_csv)
    
    for i in range(READINGS_PER_PUNCH): #Stores distance of punch to centroid for each point in time
        distances[i] = euclidean_distance(next(punch_reader), next(centroid_reader))
    
    deviations[centroid_file] = statistics.stdev(distances) #Stores punch compared to stdev of distances
    punch_csv.close()
    centroid_csv.close()

min_deviation = min(deviations.items(), key=lambda item: item[1])
print("Punch: ",end ="")
print(min_deviation)
print(deviations)

punch_csv.close()
