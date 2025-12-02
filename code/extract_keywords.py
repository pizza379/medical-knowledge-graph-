#!/usr/bin/env python3

# coding: utf-8

import pandas as pd

df_in = pd.read_csv('./disease3.csv', encoding='utf-8')

data_list=[]
node_name_list = ["Alias", "Part", "Age", "Infection", "Insurance","Department","Checklist","Symptom","Complication","Treatment","Drug","Period","Rate","Money"]

for i in range(0,28):
    cell_value = df_in.iloc[i, 0]
    data_list.append([cell_value,"Disease"])

    for k in range(1,14):
        cell_value = str(df_in.iloc[i, k])
        new_value=cell_value.split()
        for j in range(len(new_value)):
            data_list.append([new_value[j],node_name_list[k-1]])


#data = [["Name", "Age", "Country"], ["John", 25, "USA"], ["Jane", 30, "Canada"]]
 
df_out = (pd.DataFrame(data_list)).drop_duplicates()
df_out.to_csv('data.csv', index=False, header=False, encoding='gbk')


"""
for i in range(0,28):
    cell_value = str(df.iloc[i, 2])
    new_value=cell_value.split()
    for j in range(len(new_value)):
        print(df.iloc[i, 0],new_value[j],"is_of_part",file = log)
"""




