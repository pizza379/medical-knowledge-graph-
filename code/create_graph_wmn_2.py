#!/usr/bin/env python3

# coding: utf-8

import pandas as pd
from py2neo import Graph, Node, Relationship
graph = Graph("bolt://localhost:7688",auth=("neo4j", "process-people-begin-record-chicago-3718")) 

df = pd.read_csv('./disease3.csv', encoding='utf-8')

graph.run('MATCH (n) detach delete n')

node_name_list = ["Alias", "Part", "Age", "Infection", "Insurance","Department","Checklist","Symptom","Complication","Treatment","Drug","Period","Rate","Money"]
edge_name_list = ["HAS_ALIAS", "IS_OF_PART", "IS_OF_AGE", "IS_INFECTIOUS", "In_Insurance","IS_OF_Department","HAS_Checklist","HAS_SYMPTOM","HAS_Complication","HAS_Treatment","HAS_Drug","Cure_Period","Cure_Rate","NEED_Money"]

for i in range(0,28):
    cell_value = df.iloc[i, 0]
    node_1 = Node("Disease", name = cell_value)
    graph.create(node_1)

    for k in range(1,14):
        cell_value = str(df.iloc[i, k])
        new_value=cell_value.split()
        for j in range(len(new_value)):
            node_2 = Node(node_name_list[k-1], name = new_value[j])
            graph.merge(node_2,node_name_list[k-1],'name')

            node_1_call_node_2 = Relationship(node_1,edge_name_list[k-1],node_2)
            graph.merge(node_1_call_node_2)

"""
    cell_value = str(df.iloc[i, 2])
    new_value=cell_value.split()
    for j in range(len(new_value)):
        node_3 = Node("Part", part = new_value[j])
        graph.merge(node_3,'Part','part')

        node_1_call_node_3 = Relationship(node_1,'IS_OF_PART',node_3)
        graph.merge(node_1_call_node_3) 

    cell_value = str(df.iloc[i, 3])
    new_value=cell_value.split()
    for j in range(len(new_value)):
        node_4 = Node("Age", age = new_value[j])
        graph.merge(node_4,'Age','age')

        node_1_call_node_4 = Relationship(node_1,'IS_OF_AGE',node_4)
        graph.merge(node_1_call_node_4) 

    cell_value = str(df.iloc[i, 4])
    new_value=cell_value.split()
    for j in range(len(new_value)):
        node_5 = Node("Infection", infection = new_value[j])
        graph.merge(node_5,'Infection','infection')

        node_1_call_node_5 = Relationship(node_1,'IS_INFECTIOUS',node_5)
        graph.merge(node_1_call_node_5) 

    cell_value = str(df.iloc[i, 8])
    new_value=cell_value.split()
    for j in range(len(new_value)):
        node_9 = Node("Symptom", name = new_value[j])
        graph.merge(node_9,'Symptom','name')

        node_1_call_node_9 = Relationship(node_1,'HAS_SYMPTOM',node_9)
        graph.merge(node_1_call_node_9) 
"""


"""
for i in range(0,28):
    cell_value = str(df.iloc[i, 2])
    new_value=cell_value.split()
    for j in range(len(new_value)):
        print(df.iloc[i, 0],new_value[j],"is_of_part",file = log)
"""




