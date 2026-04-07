import csv
import sys

if (len(sys.argv) != 3):
    print("Usage: python centroid.py [profile] [punch]")
    sys.exit(-1)


PROFILE = sys.argv[1]
PUNCH = sys.argv[2]    #Punch the centroid is being created for
DATA_FILE = "./profiles/" + PROFILE + "/data/" + PUNCH + ".csv" #file reading raw data from   
CENTROID_FILE = "./profiles/" + PROFILE + "/centroids/" + PUNCH + "_centroid.csv"  #file writing centroid to

with open(DATA_FILE, 'r') as f:
    line_count = sum(1 for line in f)

READINGS_PER_PUNCH = 20 #40
NUM_PUNCHES = (line_count / READINGS_PER_PUNCH)        #Ideally is automatically read 
NUM_VALUES = 7 #Number of data values (accel, gryo, piezo)


'''Opens raw data for reading'''
csv_file = open(DATA_FILE,'r') 
csv_reader = csv.reader(csv_file)

centroids = [[0] * NUM_VALUES for i in range(READINGS_PER_PUNCH)]

row_total = READINGS_PER_PUNCH * NUM_PUNCHES
row_count = 0
for row in csv_reader:
    for i in range(NUM_VALUES):
        centroids[row_count % READINGS_PER_PUNCH][i] += ( float(row[i]) / (row_total / READINGS_PER_PUNCH) )
    row_count += 1
centroids_file = open(CENTROID_FILE, 'w')

for row in centroids:
    current_row = [str(x) for x in row]
    centroids_file.write(", ".join(current_row))
    centroids_file.write("\n")

csv_file.close()
centroids_file.close()
