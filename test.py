import os
import csv
import json

def read_file(path):
    f = open(path,"r")

    title = ""
    artist = ""
    subtitle = ""
    charts = []
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

    text = f.read()
    sections = text.split("#NOTES:")
    number_of_charts = len(sections)
    for i in range(number_of_charts):
        step_data = sections[i].split(":")
        if "dance-single" in step_data[0]:
            breakdown = []
            first_note_stream = False
            stepartist = step_data[1].strip()
            difficulty = step_data[2].strip()
            block = step_data[3].strip()
            # print(stepartist, difficulty, block)

            breakdown_data = []
            measures = step_data[5].strip().split(",")
            for index, m in enumerate(measures):
                # Filter measure to be just a list of 4-strings, removing whitespaces and ;
                measure = [x for x in list(filter(None, m.split('\n'))) if x != ';']
                is_stream = True
                if len(measure) == 16:
                    # Keep track of 'almost' full stream
                    error_counter = 0
                    for e in measure:
                        if e.count('0') == 4:
                            error_counter += 1
                            if error_counter >= 2:
                                is_stream = False
                else:
                    is_stream = False
                if index == 0 and is_stream:
                    first_note_stream = True
                breakdown_data.append(is_stream)

            increment = 1
            for i in range(len(breakdown_data)):
                if breakdown_data[i] == breakdown_data[i-1] and i != 0:
                    increment += 1
                else:
                    breakdown.append(increment)
                    increment = 1
            breakdown = breakdown[1:]
            # If first note is stream, stream is even-index (starting at 0)
            # Otherwise, stream is odd-index (starting at 1)
            stream = breakdown[int(not first_note_stream)::2]
            breaks = breakdown[int(not first_note_stream)+1::2]
            # print(len(breakdown), len(stream), len(breaks))
            # print(breakdown, stream, breaks)

            if len(stream) == 0:
                breakdown_string = 'No stream!'
                short_breakdown_string = 'No stream!'
            else:
                breakdown_string = str(stream[0])
                short_breakdown_string = breakdown_string
                if len(breaks) == len(stream):
                    breaks = breaks[:1]
                for i in range(len(breaks)):
                    breakdown_string += " (" + str(breaks[i]) + ") " + str(stream[i+1])
                    if breaks[i] >= 32:
                        short_breakdown_string += "|" + str(stream[i+1])
                    elif breaks[i] >= 4:
                        short_breakdown_string += "/" + str(stream[i+1])
                    else:
                        short_breakdown_string += "-" + str(stream[i+1])
        charts.append([stepartist, difficulty, block, short_breakdown_string, breakdown_string])

    return [title, subtitle, artist, charts]
# read_file('sm/ITGAlex\'s Stamina Safari/tricky trick/trickytrick.sm')

with open('test.csv', mode='w') as csv_file:
    writer = csv.writer(csv_file)
    # writer.writerow(['Title', 'Artist', 'Difficulty', 'Block', 'Summary', 'Detailed'])
    for root, dirs, files in os.walk("."):
        for f in files:
            if f.endswith('.sm'):
                path = root + "/" + f
                print(path)
                file = read_file(path)
                for i in range(len(file[3])):
                    if file[1]:
                        writer.writerow([file[0] + ' (' + file[1] + ')', file[2], file[3][i][1], file[3][i][2], file[3][i][3], file[3][i][4]])
                    else:
                        writer.writerow([file[0], file[2], file[3][i][1], file[3][i][2], file[3][i][3], file[3][i][4]])
                    
f = open('test.csv', 'r')
reader = csv.DictReader(f, fieldnames=('Title', 'Artist', 'Difficulty', 'Block', 'Summary', 'Detailed'))
out = json.dumps([row for row in reader])
f = open('test.json', 'w')
f.write(out)
        


# for root, dirs, files in os.walk("."):
#     for file in files:
#         if file.endswith('.sm'):
#             path = root + "/" + file
#             # print(path)
#             read_file(path)