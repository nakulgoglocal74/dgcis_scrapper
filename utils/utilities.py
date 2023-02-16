import os
import csv

def make_dir(path):
    os.makedirs(path, exist_ok = True)
    
def make_csv(path,headers):
    if not os.path.isfile(path):
        with open(path, 'w') as f:
            w = csv.DictWriter(f, headers)
            w.writeheader()
            
def write_csv(path,data_dict):
    with open(path, 'a') as f:  
        w = csv.DictWriter(f, data_dict.keys())
        w.writerow(data_dict)
                          
def csv_to_json(path):
    data = {}
    with open(path, mode ='r') as csvf:
        reader = csv.DictReader(csvf,delimiter=',')
        for idx,rows in enumerate(reader):
            data[idx] = rows
    return data
