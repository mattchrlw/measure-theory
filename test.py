import os
from tabulate import tabulate

def read_file(path):

    f = open(path,"r")
    title = ""
    artist = ""
    subtitle = ""
    current_line = ""

    # Get title, artist and subtitle
    while "#NOTES" not in current_line:
        current_line = f.readline()
        if "#TITLE:" in current_line:
            title = current_line.split(":")[1].split(";")[0]
        elif "#ARTIST:" in current_line:
            artist = current_line.split(":")[1].split(";")[0]
        elif "SUBTITLE:" in current_line:
            subtitle = current_line.split(":")[1].split(";")[0]

    # Naively determine number of difficulties
    number_of_charts = len(f.read().split("//-"))

    print(title, artist, subtitle, number_of_charts, sep=" | ")


for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith('.sm'):
            path = root + "/" + file
            # print(path)
            read_file(path)