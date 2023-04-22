import csv
import sys
from collections import defaultdict
import webbrowser as wb
import random
import os

# checking for correct arguments
if (len(sys.argv) != 2):
        print("wrong usage")
        sys.exit()

# checking if output exists, if not create it
if os.path.exists("X:\coding\python\'first test'\output.csv"):
    output = open("output.csv", "r", encoding="utf8", newline='')
else:
    output = open("output.csv", "w", encoding="utf8", newline='')
    writer = csv.DictWriter(output, fieldnames=["Artist", "Track"])
    writer.writeheader()

nreader = csv.reader(output)

artists = defaultdict(list)



def main():

    try:
        inp = open("playlist.csv", "r", encoding="utf8")
    except:
        print("file doesn't exist")
        sys.exit()
    

    reader = csv.DictReader(inp)

    for row in reader:
        lis = []
        lis += row.keys()
        name = row[lis[1]]
        song = row[lis[0]]
        artists[name].append(song)

    for item in artists.items():
        print(item)

    #for item in artists.items():
        #write_row(item)

    ran = random.choice(list(artists))

    webURL = 'https://www.youtube.com/results?search_query=' + str(artists[ran][random.randint(0, len(artists[ran])-1)])
    wb.open(webURL)


def write_row(item):
    for key, val in item:
        writer.writerow({"Artist" : key, "Track" : val})
    

main()

