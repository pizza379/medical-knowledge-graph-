# 医疗知识图谱对话系统作业
# 林雨珊 2022310943

## 作业要求
1.	描述本任务“医疗知识图谱对话系统”的整体设计思路-5分
2.	neo4j-安装、启动、增删改查，文字描述+运行成功截图-5分
3.	neo4j-数据导入，文字描述+运行成功截图-5分
4.	基于关键词的文本->cypher语句解析，文字描述+核心代码-5分
5.	对话系统的输入输出、用户交互，运行成功截图-5分
6.	提交csdn/github网页链接或将网页输出成pdf提交-5分

## 一、整体设计思路


## 二、Neo4j-安装、启动、增删改查
### 1. Neo4j启动
- **docker desktop**：点击桌面上的docker desktop成功打开后不登录
- **命令语句**：在powershell中输入命令行
docker run --publish=7475:7474 --publish=7688:7687 --volume=/root/专业综合实践/data:/data --volume=/root/专业综合实践/import:/import docker.1ms.run/library/neo4j

### 2. Neo4j增删改查操作
#### （1）创建节点/关系（增）
```cypher
// 创建疾病节点，症状节点，并建立关系
CREATE (d:Disease {name: "感冒"})
CREATE (s:Symptom {name: "发烧"})
CREATE (d)-[:HAS_SYMPTOM]->(s)
```
[Neo4j增添结果](./screenshots/1增.png)
#### （2）查询数据(查)
```cypher
// 查询所有疾病节点
MATCH (d:Disease) RETURN d.name
// 查询所有症状有发烧的疾病名称
MATCH (d)-[:HAS_SYMPTOM]->(s:Symptom{name:"发烧"}) RETURN d.name
```
[Neo4j查询结果1](./screenshots/2查.png)
[Neo4j查询结果2](./screenshots/3查.png)

#### （3）修改节点属性（改）
```cypher
MATCH (d:Disease {name: "感冒"}) SET d.alias = "普通感冒" RETURN d
```
[Neo4j修改结果](./screenshots/4改.png)
#### （4）删除节点（删）
```cypher
MATCH (d:Disease {name: "感冒"}) DETACH DELETE d
```
左侧提示 “Deleted 3 nodes, deleted 2 relationships, completed after 8 ms.”，结果列显示 “删除成功”，表示节点与关系已删除。

## 三、Neo4j-数据导入
### 1. 数据准备
- 数据源文件：`disease3.csv`（由`disease1.csv`改名而来，为了适配源代码文件）。将其放在create_graph_wmn_2.py同级目录，确保文件编码为UTF-8（用记事本打开→“另存为”→编码选择 “UTF-8”）
- 数据导入脚本：`create_graph_wmn_2.py`（负责读取CSV数据并批量创建Neo4j节点/关系）。

### 2. 数据导入步骤
#### （1）环境依赖安装
打开命令提示符执行：
```bash
pip install pandas py2neo

```
[环境依赖安装截图](./screenshots/环境依赖安装.png)
#### （2）修改脚本配置
确保create_graph_wmn_2.py中的 Neo4j 连接信息与实际一致：
```python
运行
graph = Graph(
    "bolt://localhost:7688",  # Neo4j端口（默认7687，若修改过需对应）
    auth=("neo4j", "你的Neo4j密码")  # 替换为实际账号密码
)
```
[修改的代码部分](./screenshots/修改脚本配置.png)

#### （3）执行导入脚本
```bash
# 进入脚本所在目录
cd Desktop\medical-knowledge-graph-\code
# 运行导入脚本
python create_graph_wmn_2.py
```
[运行成功截图](./screenshots/数据导入运行成功.png)
#### (4)数据导入验证
```cypher
# 查询导入的疾病节点数量
MATCH (d:Disease) RETURN count(d) AS disease_count
# 查询某疾病的关联药物
MATCH (d:Disease {name: "乙肝"})-[:HAS_Drug]->(dr) RETURN dr.name
```
[验证成功截图](./screenshots/数据导入验证成功.png)


## 四、基于关键词的文本→Cypher 语句解析
### 1. 提取实体和关系
```bash
运行
# 提取实体（生成data.csv，包含所有节点类型）
python extract_keywords.py  
```
### 2.测试关键词到 Cypher 的解析逻辑
match_2.py代码如下
```python
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
```
在命令行中执行：
```bash
python match_2.py
```
[运行成功截图](./screenshots/运行成功截图.png)

## 五、对话系统的输入输出、用户交互
### 1.修改脚本配置,确保create_graph_wmn_2.py中的 Neo4j 连接信息与实际一致
### 2.在命令中执行代码user_interaction.py，进入交互页面。
```bash
python user_interaction.py
```
[交互页面用户对话成功截图](./screenshots/交互成功.png)
