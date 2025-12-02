# coding=gbk

import pandas as pd

df = pd.read_csv('data.csv', encoding='gbk')
column_data = list(map(str, df['c1']))
#print(type(column_data))
#print(column_data[2])

text = "头痛该吃什么药？"
#text = "医生，我为什么会头痛？"
#text = "神经衰弱有什么症状？"
#text = "神经衰弱该吃什么药？"
search_strings = column_data
 
count=-1
name_param=""
for s in search_strings:
    count=count+1
    if s in text:
        print(f"'{s}' found in text")
        print(count,str(df.iloc[count, 1]))
        name_param=s

from py2neo import Graph, Node, Relationship
graph = Graph("bolt://localhost:7688",auth=("neo4j", "delta-gossip-winter-degree-jumbo-7812")) 

to_check_HAS_SYMPTOM = ['症状','表征','现象','症候','表现']

flag=[]
for s in to_check_HAS_SYMPTOM:
    if s in text:
        flag.append(1)

if flag:
    print("HAS_SYMPTOM")

    query = """
    MATCH (d:Disease {name: $name})-[:HAS_SYMPTOM]->(relatedSymptom)
    RETURN relatedSymptom.name
    """
    results = graph.run(query,name=name_param)
    for record in results:
        print(record)


to_check_HAS_Symptom_inv=['导致','原因','成因','为什么','怎么会','怎样才','咋样才','怎样会','如何会','为啥','为何','如何才会']
flag=[]
for s in to_check_HAS_Symptom_inv:
    if s in text:
        flag.append(1)

if flag:
    print("HAS_Symptom_inv")

    query = """
    MATCH (relatedSymptom{name: $name})<-[:HAS_SYMPTOM]-(d:Disease)
    RETURN d.name
    """
    results = graph.run(query,name=name_param)
    for record in results:
        print(record)


to_check_HAS_Complication = ['并发症','并发','一起发生','一并发生','一起出现','一并出现','一同发生','一同出现','伴随发生']

flag=[]
for s in to_check_HAS_Complication:
    if s in text:
        flag.append(1)

if flag:
    print("HAS_Complication")

    query = """
    MATCH (d:Disease {name: $name})-[:HAS_Complication]->(relatedComplication)
    RETURN relatedComplication.name
    """
    results = graph.run(query,name=name_param)
    for record in results:
        print(record)


to_check_HAS_Drug = ['药','药品','用药','胶囊','口服液','炎片']

flag=[]
for s in to_check_HAS_Drug:
    if s in text:
        flag.append(1)

if flag:
    print("HAS_Drug")

    query = """
    MATCH (d:Disease {name: $name})-[:HAS_Drug]->(relatedDrug)
    RETURN relatedDrug.name
    """
    results = graph.run(query,name=name_param)
    for record in results:
        print(record)

    query = """
    MATCH (a:Symptom {name: $name})<-[:HAS_SYMPTOM]-(m), (m)-[:HAS_Drug]->(b)
    RETURN b.name
    """
    results = graph.run(query,name=name_param)
    for record in results:
        print(record)


