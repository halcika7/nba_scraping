import csv
import json
import sys

inputFile = sys.argv[1]
outputFile = sys.argv[2]
header = sys.argv[3].split(',')
header = tuple(header)

def start():
    array = []
    csvfile = open(inputFile, 'r')
    jsonfile = open(outputFile, 'w')

    reader = csv.DictReader( csvfile, header)
    for row in reader:
        array.append(row)

    json.dump(array, jsonfile)

if __name__ == "__main__":
    start()
