import csv
import os
import math
import statistics

READINGS_PER_PUNCH = 25 #40
NUM_VALUES = 7
PROFILE = "test_profile"
CENTROIDS_DIR = "./profiles/" + PROFILE + "/centroids/"
PUNCH_FILE = "./sample.csv"

'''
Finds euclidean distance between a punch and
centroid at a point in time.
'''
def euclidean_distance(punch, centroid, dimensions=6):
    summation = 0
    for i in range(dimensions):
        summation += (float(punch[i]) + float(centroid[i])) ** 2
    return math.sqrt(summation)

'''
Returns string of punch name from id
'''
def punch_from_id(pid):
    
    if (pid == 0):
        return "cross"
    else:
        return "right_hook"


distances = [0] * READINGS_PER_PUNCH
deviations = []

for centroid_file in os.listdir(CENTROIDS_DIR):  #Iterates through all centroid csv files
    centroid_file = CENTROIDS_DIR + centroid_file
    
    centroid_csv = open(centroid_file,'r')       #Opens current csv
    centroid_reader = csv.reader(centroid_csv)   #Initializes a reader for current csv
    
    punch_csv = open(PUNCH_FILE, 'r')
    punch_reader = csv.reader(punch_csv)
    
    for i in range(READINGS_PER_PUNCH): #Stores distance of punch to centroid for each point in time
        distances[i] = euclidean_distance(next(punch_reader), next(centroid_reader))
    
    deviations.append(statistics.stdev(distances)) #Appends stdev to deviations
    punch_csv.close()
    centroid_csv.close()
print(distances)
print(deviations)

min_deviation = min(deviations)
punch_index = deviations.index(min_deviation)

print(punch_from_id(punch_index))

punch_csv.close()
