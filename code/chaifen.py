# -*- coding: utf-8 -*-

import pandas as pd
 
# 读取CSV文件
df = pd.read_csv('./disease3.csv', encoding='utf-8')

# 假设单元格内容是以空格分隔的
#df['new_column'] = df['B'].str.split()

# 使用正则表达式处理多种分隔符（例如逗号和分号）
#df['new_column'] = df['column_name'].str.split('[,;]',expand=True)

# 使用iloc访问特定单元格，注意行和列的索引都是从0开始的
#cell_value = df.iloc[0, 1]  # 第2行第3列（因为索引是从0开始的）
#print(cell_value)  # 打印单元格的值

log = open("a.txt",mode="a",encoding="utf-8")

for i in range(0,28):
    cell_value = str(df.iloc[i, 2])
    new_value=cell_value.split()
    for j in range(len(new_value)):
        print(df.iloc[i, 0],new_value[j],"is_of_part",file = log)

log.close()


#new_value=cell_value.split(",")
#print(type(new_value))

##print(df.head())  # 显示前几行数据以查看结果
 
#for i in range(len(new_value)):
#    print(new_value[i])

