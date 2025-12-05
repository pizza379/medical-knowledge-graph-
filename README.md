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
本 “医疗知识图谱对话系统” 旨在通过知识图谱技术实现用户与医疗信息的智能交互，核心目标是让用户通过自然语言提问获取疾病、症状、药物等相关医疗知识。系统整体设计分为五个核心环节：
### 1.知识图谱构建：以 Neo4j 作为图数据库，存储医疗领域实体（如疾病、症状、药物等）及实体间关系（如 “疾病有症状”“疾病对应药物” 等），形成结构化的医疗知识网络。
### 2.数据导入：通过 Python 脚本批量处理 CSV 格式的医疗数据，将实体和关系自动导入 Neo4j，避免手动录入的繁琐。
### 3.自然语言解析：基于关键词匹配技术，从用户输入文本中提取实体（如 “头痛”“感冒”）和意图（如 “查症状”“找药物”），并将其转换为 Neo4j 可执行的 Cypher 查询语句。
### 4.查询与反馈：执行 Cypher 语句查询知识图谱，获取结果后以自然语言形式返回给用户。
### 5.用户交互：通过命令行交互界面，支持用户持续输入问题并获得实时响应，实现多轮对话体验。
系统设计的核心逻辑是将非结构化的用户提问转化为结构化的图谱查询，利用图数据库高效的关联查询能力，快速返回精准的医疗知识，为用户提供便捷的信息检索服务。

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
该模块实现用户自然语言到图谱查询语句的转换，分为三个步骤：
1.实体提取：通过extract_keywords.py从医疗数据中生成实体字典（data.csv），包含实体名称及其类型（如 “头痛” 属于 Symptom，“感冒” 属于 Disease）。
2.意图识别：分析用户文本中的关键词（如 “药” 对应 “查药物”，“症状” 对应 “查症状”），确定用户查询意图。
3.Cypher 生成：根据提取的实体类型和识别的意图，动态生成匹配的 Cypher 语句。例如，用户问 “头痛应该吃什么药？” 时，系统识别实体 “头痛”（Symptom）和意图 “药物”，生成查询语句：
### 1. 提取实体和关系
```bash
运行
# 提取实体（生成data.csv，包含所有节点类型）
python extract_keywords.py  
```
### 2.测试关键词到 Cypher 的解析逻辑
关键代码说明
load_entities()：加载data.csv中的实体信息，构建实体 - 类型映射字典。
extract_entities()：从用户文本中匹配实体字典中的实体，返回识别结果。
identify_intent()：通过关键词匹配判断用户意图（药物、症状、疾病等）。
query_graph()：根据实体类型和意图生成 Cypher 语句，调用 Neo4j 接口执行查询并返回结果。
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
### 2.在命令中执行代码user_interaction.py，进入交互页面，流程如下：
运行脚本：在命令行执行python user_interaction.py启动交互模式。
用户输入：例如 “感冒有什么症状？”“发烧吃什么药？” 等问题。
系统处理：自动提取实体、识别意图、生成 Cypher 查询、返回结果（如 “感冒的症状包括发烧、咳嗽”）。
多轮对话：支持用户连续提问，直至输入退出指令。
### 3.交互特点
响应及时：基于关键词匹配和图数据库查询，快速返回结果。
容错处理：若未识别到实体或无匹配结果，会提示 “未识别到实体” 或 “未查询到相关信息”。
```bash
python user_interaction.py
```
[交互页面用户对话成功截图](./screenshots/交互成功.png)
