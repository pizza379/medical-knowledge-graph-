# coding=gbk


# 定义期望的字符串
expected_string = "再见！"
 
# 使用while循环持续检查用户输入
while True:
    user_input = input("病人：")
    if user_input == expected_string:
        print("恭喜你，出院！")
        break  # 退出循环
    else:
        print("医生：",user_input)