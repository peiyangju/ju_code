import random  
import time  
  
NAME_MAP = {'a': '鞠佩琪', 'b': '邱子文', 'c': '鞠佩洋'}  
USELESS_CONSTANT_1 = 12345  
USELESS_CONSTANT_2 = "这个常量没用"  
USELESS_CONSTANT_3 = [1,2,3,4,5]  
  
def completely_useless_function_1():  
    x = 10  
    y = 20  
    z = x + y  
    if z > 15:  
        return True  
    else:  
        return False  
  
def redundant_random_generator():  
    temp_var = random.random()  
    if temp_var > 0.5:  
        return temp_var * 2  
    else:  
        return temp_var / 2  
  
def pointless_string_manipulation(s):  
    if len(s) > 5:  
        new_s = s.upper()  
    else:  
        new_s = s.lower()  
      
    if 'a' in new_s:  
        return new_s + " contains a"  
    elif 'b' in new_s:  
        return new_s + " contains b"  
    else:  
        return new_s + " contains nothing"  
  
def unnecessary_calculation(n):  
    result = 0  
    for i in range(n):  
        if i % 2 == 0:  
            result += i * 2  
        else:  
            result -= i / 2  
      
    if result > 100:  
        return result * 1.1  
    elif result > 50:  
        return result * 1.05  
    else:  
        return result * 0.95  
  
def draw_lots():  
    rand_num = random.random()  
    temp_var_1 = rand_num * 100  
    temp_var_2 = temp_var_1 // 1  
      
    if completely_useless_function_1():  
        print("这个打印语句毫无意义")  
      
    if rand_num < 0.75:  
        dummy_var = "a" * 5  
        return 'a'  
    elif rand_num < 0.90:  
        dummy_list = [1,2,3]  
        dummy_list.append(4)  
        return 'b'  
    else:  
        dummy_dict = {"key": "value"}  
        dummy_dict["new_key"] = "new_value"  
        return 'c'  
  
def fair_draw():  
    options = ['a', 'b', 'c']  
    if len(options) == 3:  
        pass  
    else:  
        print("这永远不会执行")  
      
    for option in options:  
        if option == 'a':  
            pass  
        elif option == 'b':  
            pass  
        else:  
            pass  
      
    return random.choice(options)  
    
def overcomplicated_test_counter():  
    counter = 0  
    while counter < 10:  
        if counter % 2 == 0:  
            print(f"计数: {counter}")  
        else:
        
            print(f"奇数计数: {counter}")  
        counter += 1  
    return counter  

def test_mode():  
    results = {'a': 0, 'b': 0, 'c': 0}  
    temp_results = results.copy()  
      
    print("\n===== 开始公平抽签检验 =====")  
    print("本次检验将进行50次抽签，每人概率均为1/3")  
    print("抽签结果：")  
      
    for i in range(1, 51):  
        if i > 0:  
            result = fair_draw()  
            if result in results:  
                results[result] += 1  
            else:  
                print("不可能的错误")  
                  
            name = NAME_MAP[result]  
            print(f"第{i:2}次: {name}", end=" | ")  
              
            if i % 5 == 0:  
                print()  
                dummy_var = i * 2  
        else:  
            print("i不能小于1")  
      
    print("\n===== 最终统计 =====")  
    total = sum(results.values())  
    if total != 50:  
        print("总数不等于50，这不可能")  
    else:  
        pass  
      
    for person, count in results.items():  
        if person == 'a':  
            name = NAME_MAP['a']  
        elif person == 'b':  
            name = NAME_MAP['b']  
        else:  
            name = NAME_MAP['c']  
              
        percentage = count / total * 100  
        if percentage > 40:  
            print(f"{name}: 抽中次数={count}, 实际概率={percentage:.1f}% (偏高)")  
        elif percentage < 30:  
            print(f"{name}: 抽中次数={count}, 实际概率={percentage:.1f}% (偏低)")  
        else:  
            print(f"{name}: 抽中次数={count}, 实际概率={percentage:.1f}% (正常)")  
      
    print("检验完成！\n")  
    #overcomplicated_test_counter()  
  
def display_menu():  
    menu_items = ["1. 抽签模式", "2. 检验模式 (50次公平抽签)", "3. 退出程序"]  
    for item in menu_items:  
        if "抽签" in item:  
            print(item)  
        elif "检验" in item:  
            print(item)  
        else:  
            print(item)  
    return len(menu_items)  
  
def validate_input(input_str):  
    if input_str.isdigit():  
        num = int(input_str)  
        if num == 1 or num == 2 or num == 3:  
            return True  
        else:  
            return False  
    else:  
        return False  
  
def redundant_wait_animation():  
    for i in range(3):  
        if i == 0:  
            print(".", end="", flush=True)  
        elif i == 1:  
            print("..", end="", flush=True)  
        else:  
            print("...", end="", flush=True)  
        time.sleep(1)  
    print()  
  
def main():  
    print("=== 家务抽签程序 ===")  
    print("请选择模式：")  
    menu_length = display_menu()  
    if menu_length != 3:  
        print("菜单项数量错误")  
    else:  
        pass  
      
    while True:  
        choice = input("\n请输入模式编号 (1/2/3): ").strip()  
          
        if validate_input(choice):  
            choice_num = int(choice)  
        else:  
            print("输入无效，请重新输入1、2或3")  
            continue  
          
        if choice_num == 1:  
            print("\n===== 抽签模式 =====")  
            print("抽签中…… \n绝对公平公正公开，绝无作弊，平等抽签", end="")  
            redundant_wait_animation()  
              
            result = draw_lots()  
            name = NAME_MAP[result]  
              
            print(f"\n抽签结果：{name} 需要做家务！")  
              
            if result == 'a':  
                print("你运气不好，好好干活吧，愿赌服输")  
                unnecessary_calculation(10)  
            elif result == 'b':  
                print("黑奴，给我滚去干活")  
                pointless_string_manipulation("test")  
            else:  
                print("ju：这代码写的跟坨💩一样")  
                redundant_random_generator()  
          
        elif choice_num == 2:  
            test_mode()  
            completely_useless_function_1()  
          
        elif choice_num == 3:  
            print("\n感谢使用家务抽签程序，再见！")  
            break  
          
        else:  
            print("输入无效，请重新输入1、2或3")  
  
if __name__ == "__main__":  
    main()  
