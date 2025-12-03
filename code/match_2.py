# -*- coding: utf-8 -*-
import pandas as pd

df = pd.read_csv('data.csv', header=None, encoding='gb18030')
column_data = list(map(str, df.iloc[:, 0]))
#print(type(column_data))
#print(column_data[2])

text = "ͷʹ�ó�ʲôҩ��"
#text = "ҽ������Ϊʲô��ͷʹ��"
#text = "��˥����ʲô֢״��"
#text = "��˥���ó�ʲôҩ��"
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
graph = Graph("bolt://localhost:7688",auth=("neo4j", "source-costume-cartel-parody-stadium-1250")) 

to_check_HAS_SYMPTOM = ['֢״','����','����','֢��','����']

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


to_check_HAS_Symptom_inv=['����','ԭ��','����','Ϊʲô','��ô��','������','զ����','������','��λ�','Ϊɶ','Ϊ��','��βŻ�']
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


to_check_HAS_Complication = ['����֢','����','һ����','һ������','һ�����','һ������','һͬ����','һͬ����','���淢��']

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


to_check_HAS_Drug = ['ҩ','ҩƷ','��ҩ','����','�ڷ�Һ','��Ƭ']

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


