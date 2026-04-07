import csv
import sys
from collections import deque

if (len(sys.argv) != 1):
    print("Usage: python process_punch.py")
    sys.exit(-1)

input_file = "raw.csv"
output_file = "data.csv"

CONTEXT_LINES = 20
PIEZO_THRESHOLD = 1000
buffer = deque(maxlen=CONTEXT_LINES)  # Holds up to 20 preceding lines (including current)
count = 0
cooldown = 0

with open(input_file, newline="") as infile, open(output_file, "w") as outfile:
    reader = csv.reader(infile)
    for line_num, row in enumerate(reader, start=1):
        cooldown -= 1
        if not row:
            continue

        buffer.append((line_num, row))

        try:
            if len(row) > 6 and float(row[6]) > PIEZO_THRESHOLD and (cooldown < 0):
                cooldown = 20
                for _, buffered_row in buffer:
                    outfile.write(",".join(buffered_row) + "\n")
                count += 1
        except ValueError:
            # Skip header rows or non-numeric first column values
            pass

print(f"Done. {count} trigger(s) found, output written to '{output_file}'.")
