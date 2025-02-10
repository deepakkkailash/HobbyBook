from Models import Hobby
import pandas as pd
import kagglehub
import csv

# Download latest version
path = kagglehub.dataset_download("mrhell/list-of-hobbies")

path_to_dataset = f'{path}/hobbylist.csv'

df = pd.read_csv(path_to_dataset)

df.drop_duplicates(inplace=True)

df.to_csv(path_to_dataset)



with open(path_to_dataset,mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        Hobby.addhobby(row[0],row[1])

