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
