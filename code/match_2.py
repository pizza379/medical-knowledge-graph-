# coding=utf-8

import pandas as pd
from py2neo import Graph

# 1. 连接Neo4j（确保配置正确）
graph = Graph("bolt://localhost:7688", auth=("neo4j", "mask-quarter-company-elite-lotus-2723"))

# 2. 读取data.csv，获取所有实体及类型（过滤空值和非字符串）
def load_entities():
    try:
        df = pd.read_csv('data.csv', encoding='gbk')
        entity_dict = {}
        for _, row in df.iterrows():
            # 提取实体名称和类型，强制转为字符串并去空格
            entity_name = str(row.iloc[0]).strip()
            entity_type = str(row.iloc[1]).strip()
            # 跳过空值或"nan"（NaN转换后的字符串）
            if entity_name not in ["", "nan"] and entity_type not in ["", "nan"]:
                entity_dict[entity_name] = entity_type
        return entity_dict
    except Exception as e:
        print(f"读取实体失败: {e}")
        return {}

# 3. 从文本中提取所有匹配的实体
def extract_entities(text, entity_dict):
    matched_entities = []
    for entity_name, entity_type in entity_dict.items():
        # 确保entity_name是字符串且存在于文本中
        if isinstance(entity_name, str) and entity_name in text:
            matched_entities.append({
                "name": entity_name,
                "type": entity_type
            })
    return matched_entities

# 4. 识别用户意图
def identify_intent(text):
    intent_keywords = {
        "药物": ["药", "吃药", "吃什么药", "用药", "药品"],
        "症状": ["症状", "表现", "征兆"],
        "疾病": ["原因", "是什么病", "对应疾病"],
        "并发症": ["并发症", "后遗症"]
    }
    for intent, keywords in intent_keywords.items():
        if any(keyword in text for keyword in keywords):
            return intent
    return "未知"

# 5. 根据实体类型和意图执行查询
def query_graph(entities, intent):
    results = []
    for entity in entities:
        entity_name = entity["name"]
        entity_type = entity["type"]
        
        if intent == "药物":
            # 症状→疾病→药物
            if entity_type == "Symptom":
                query = """
                MATCH (s:Symptom {name: $name})<-[:HAS_SYMPTOM]-(d:Disease)-[:HAS_Drug]->(dr)
                RETURN dr.name AS drug
                """
                res = graph.run(query, name=entity_name).data()
                results.extend([item["drug"] for item in res])
            
            # 疾病→药物
            elif entity_type == "Disease":
                query = """
                MATCH (d:Disease {name: $name})-[:HAS_Drug]->(dr)
                RETURN dr.name AS drug
                """
                res = graph.run(query, name=entity_name).data()
                results.extend([item["drug"] for item in res])
        
        elif intent == "疾病" and entity_type == "Symptom":
            query = """
            MATCH (s:Symptom {name: $name})<-[:HAS_SYMPTOM]-(d:Disease)
            RETURN d.name AS disease
            """
            res = graph.run(query, name=entity_name).data()
            results.extend([item["disease"] for item in res])
    
    return list(set(results))  # 去重

# 6. 主逻辑
if __name__ == "__main__":
    entity_dict = load_entities()
    if not entity_dict:
        print("实体数据加载失败！")
        exit()
    
    text = "头痛应该吃什么药？"
    print(f"用户输入：{text}")
    
    matched_entities = extract_entities(text, entity_dict)
    if not matched_entities:
        print("未识别到任何实体！")
        exit()
    print(f"识别到实体：{matched_entities}")
    
    intent = identify_intent(text)
    print(f"识别到意图：{intent}")
    
    answers = query_graph(matched_entities, intent)
    
    if answers:
        print(f"\n结果：{answers}")
    else:
        print("\n未查询到相关信息！")