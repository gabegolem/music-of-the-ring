import csv

READINGS_PER_PUNCH = 40 #40
NUM_PUNCHES = 10        #10 
PIEZO_THRESHOLD = 1000
NUM_VALUES = 7
PUNCH = "right_hook"
DATA_FILE = "./profiles/test_profile/data/" + PUNCH + ".csv"
CENTROID_FILE = "./profiles/test_profile/centroids/" + PUNCH + "_centroid.csv"

csv_file = open(DATA_FILE,'r')
csv_reader = csv.reader(csv_file)
centroids = [[0] * NUM_VALUES for i in range(READINGS_PER_PUNCH)]

row_total = READINGS_PER_PUNCH * NUM_PUNCHES
row_count = 0
for row in csv_reader:
    row_count += 1
    for i in range(NUM_VALUES):
        centroids[row_count % READINGS_PER_PUNCH][i] += ( float(row[i]) / (row_total / READINGS_PER_PUNCH) )

centroids_file = open(CENTROID_FILE, 'w')

for row in centroids:
    current_row = [str(x) for x in row]
    centroids_file.write(", ".join(current_row))
    centroids_file.write("\n")

csv_file.close()
centroids_file.close()
