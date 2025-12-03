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


