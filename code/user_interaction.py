# -*- coding: utf-8 -*-
from py2neo import Graph
import pandas as pd

# 1. 初始化Neo4j连接
graph = Graph(
    "bolt://localhost:7687",  # 替换为你的Neo4j端口
    auth=("neo4j", "你的Neo4j密码")
)

# 2. 读取医疗实体数据（与match_2.py一致）
df = pd.read_csv('data.csv', header=None, encoding='gbk')
column_data = list(map(str, df.iloc[:, 0]))  # 实体列表

# 3. 意图关键词与Cypher模板映射
intent_cypher_map = {
    "HAS_SYMPTOM": "MATCH (d:Disease)-[:HAS_SYMPTOM]->(s) WHERE s.name CONTAINS $entity RETURN d.name",
    "HAS_Drug": "MATCH (d:Disease)-[:HAS_Drug]->(dr) WHERE d.name CONTAINS $entity RETURN dr.name",
    "IS_OF_Department": "MATCH (d:Disease)-[:IS_OF_Department]->(de) WHERE d.name CONTAINS $entity RETURN de.name"
}

# 4. 实体提取与意图识别函数
def extract_entity(text):
    for entity in column_data:
        if entity in text:
            return entity
    return text  # 无匹配实体时返回原文本

def identify_intent(text):
    if any(word in text for word in ["药", "吃什么药", "用药"]):
        return "HAS_Drug"
    elif any(word in text for word in ["病", "什么病", "诊断"]):
        return "HAS_SYMPTOM"
    elif any(word in text for word in ["科室", "就诊"]):
        return "IS_OF_Department"
    return None

# 5. Cypher查询与答案生成
def get_answer(text):
    entity = extract_entity(text)
    intent = identify_intent(text)
    if not intent or not entity:
        return "抱歉，我还不理解你的问题~"
    
    cypher = intent_cypher_map.get(intent)
    if not cypher:
        return "暂无相关信息"
    
    # 执行Cypher查询
    result = graph.run(cypher, entity=entity).data()
    if not result:
        return "未查询到相关结果"
    
    # 格式化答案
    values = [item[list(item.keys())[0]] for item in result]
    return f"{entity}相关结果：{', '.join(values[:5])}"  # 限制返回数量

# 6. 交互主循环
print("医疗知识图谱对话系统已启动，输入'再见！'退出~")
while True:
    user_input = input("病人：")
    if user_input == "再见！":
        print("医生：恭喜你，出院！")
        break
    answer = get_answer(user_input)
    print(f"医生：{answer}")