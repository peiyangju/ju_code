# 用代码模拟非对称式加密

# 获取用户输入的五位数字
number = input("请输入一个五位数字：")

# 验证输入是否为五位数字
if len(number) != 5 or not number.isdigit():
    print("请输入有效的五位数字！")
else:
    # 将输入转换为整数
    num = int(number)

    # 乘以2359（公钥）
    step1 = num * 2359
    print(f"乘以2359后的结果：{step1}")

    # 取结果的后五位数
    last_five1 = step1 % 100000
    print(f"后五位数字是：{last_five1:05d}")

    # 乘以12039(私钥)
    step2 = last_five1 * 12039
    print(f"乘以12039后的结果：{step2}")

    # 取结果的后五位数
    last_five2 = step2 % 100000
    print(f"密码是：{last_five2:05d}")

'''综上所述，密码✖2359取后五位，再✖12039取后五位等于原密码
   所以，只要别人不知道私钥为12039，密码就不会被破解'''