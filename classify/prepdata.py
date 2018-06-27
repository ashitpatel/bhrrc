import sys
import os
import csv
import json
from random import shuffle

sys.path.append("../util")
import util

# process non-HR data in csv format and convert it to json format
json_data = []
with open('nonhrdata/articles.csv',encoding = "ISO-8859-1") as csvfile:
    readCSV = csv.reader(csvfile)
    for row in readCSV:
        if row is not None:
            if len(row) == 0:
                continue
            if len(row[0]) == 0:
                continue
            new_data = {}
            new_data['classification'] = ["NON_HR"]
            new_data['body'] = str(row[0])

# util.clense(str(row[0]), to_lower=False,remove_punc=False).strip()
#            new_data['body'] = util.clense(str(row[0]), to_lower=False,remove_punc=False).strip()
            json_data.append(new_data)

print(len(json_data))

# process HR json file data
with open('data/data_with_middle_layer.json') as jsonfile:
     hrdata = json.load(jsonfile)

     for srcElement in hrdata:
         if len(srcElement['body']) < 5: # if body is empty
             continue
         new_data = {}
         new_data['classification'] = ["HR"]
         new_data['body'] = srcElement['body'] 
#         new_data['body'] = util.clense(srcElement['body'], to_lower=False,remove_punc=False).strip()
         json_data.append(new_data)
         
shuffle(json_data)   # mix up HR and non-HR elements
f=open("data/classified_data.json", "w")
json.dump(json_data,f)
f.close()
