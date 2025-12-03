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
# 生成疾病与部位的关系（输出到a.txt）
python chaifen.py  
```
### 2. 导入知识图谱到 Neo4j
```bash
# 执行 build_graph.py 构建节点和关系：
python build_graph.py  
```
运行过程中会打印进度（如节点创建数量、关系创建数量）。根据数据量等待执行完成约20分钟。
[构建图谱运行成功截图](./screenshots/图谱构建运行成功.png)
### 3. 验证知识图谱
在 Neo4j Browser 中执行以下 Cypher 语句验证数据是否导入成功：
#### (1)查看所有节点类型
```cypher
MATCH (n) RETURN distinct labels(n)
```
#### (2)查看具体疾病的属性
```cypher
MATCH (d:Disease {name: "感冒"}) 
RETURN d.name, d.age, d.treatment, d.rate
```
[验证知识图谱截图](./screenshots/验证知识图谱截图.png)

## 五、实现 “文本→Cypher” 解析与问答
1. 核心逻辑说明
实体提取：entity_extractor.py 通过 AC 自动机匹配关键词，识别用户问题中的实体（如 “感冒” 是疾病，“发烧” 是症状）。
意图识别：结合关键词匹配（如 “吃什么药” 对应 “查询药品” 意图）和机器学习模型，确定用户需求。
Cypher 生成：search_answer.py 根据实体和意图生成对应的 Cypher 语句（如查询疾病症状的 Cypher 模板）。
### 2. 交互测试
在 bash 中运行问答测试脚本：
```bash
python kbqa_test.py  
```
输入示例问题，系统会自动解析为 Cypher 并返回结果：
plaintext
用户：感冒有什么症状？
小豪：疾病 感冒 的症状有：发烧,咳嗽,头痛
**************************************************
用户：发烧需要吃什么药？
小豪：疾病 感冒 的治疗方法有：多喝水；可用药品包括：感冒药,退烧药
**************************************************