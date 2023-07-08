'''
This code is used to get the ubike info. from the following link.
URL: https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json
Government updates this data every minute.
'''
import json
import requests
import csv
import time
import os.path

url = 'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'
data = []  # save the json data 

filename = 'data_test_gui.csv'
num = 0
# If the CSV file does not exist, write the column names first.
if not os.path.isfile(filename):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['infoTime', 'tot', 'sbi', 'infoDate', 'aren', 'act', 'lng', 'srcUpdateTime', 'updateTime', 'sareaen', 'snaen', 'ar', 'bemp', 'mday', 'sarea', 'sna', 'lat', 'sno']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

while True:
    num += 1
    print(f"Have read {num} data.")
    # read new json
    response = requests.get(url)
    data += json.loads(response.text)

    # write the new data into CSV
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['infoTime', 'tot', 'sbi', 'infoDate', 'aren', 'act', 'lng', 'srcUpdateTime', 'updateTime', 'sareaen', 'snaen', 'ar', 'bemp', 'mday', 'sarea', 'sna', 'lat', 'sno']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for d in data:
            writer.writerow(d)

    # clear data to save new data
    data = []

    # wait a min
    time.sleep(60)





import json
import requests
import csv
import time
import os.path

url = 'https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json'
data = []  # save the json data 

filename = 'data_test_gui.csv'
while True:
    data += json.loads(response.text)
    with open(filename, 'a', newline='') as csvfile:
        fieldnames = ['infoTime', 'tot', 'sbi', 'infoDate', 'aren', 'act', 'lng', 'srcUpdateTime', 'updateTime', 'sareaen', 'snaen', 'ar', 'bemp', 'mday', 'sarea', 'sna', 'lat', 'sno']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for d in data:
            writer.writerow(d)
    # clear data to save new data
    data = []

    # wait a min
    time.sleep(60)