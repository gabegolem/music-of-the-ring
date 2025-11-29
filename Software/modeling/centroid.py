import csv

READINGS_PER_PUNCH = 40
NUM_PUNCHES = 4
PIEZO_THRESHOLD = 1000
NUM_VALUES = 7
CSV = "./punch_data/cross.csv"

csv_file = open(CSV,'r')
csv_reader = csv.reader(csv_file)
centroids = [[0] * NUM_VALUES for i in range(READINGS_PER_PUNCH)]

row_total = READINGS_PER_PUNCH * NUM_PUNCHES
row_count = 0
for row in csv_reader:
    row_count += 1
    for i in range(NUM_VALUES):
        centroids[row_count % READINGS_PER_PUNCH][i] += ( float(row[i]) / (row_total / READINGS_PER_PUNCH) )

centroids_file = open('centroid.txt', 'w')

for row in centroids:
    print(row)
    '''for value in row:
        value = str(value)
    centroids_file.write(", ".join(row))
    centroids_file.write("\n")'''

csv_file.close()
centroids_file.close()
