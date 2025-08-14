import turtle    
import time    
import random    
import sys    
    
# 全局变量    
screen = turtle.Screen()    
screen.setup(800, 600)    
screen.title("玩家手速与反应力测试")    
screen.bgcolor("#37E547")    
  
# 玩家区域变量    
p1_area = None      
p2_area = None      
    
# 玩家信息    
player1_name = ""    
player2_name = ""    
player1_click_times = []    
player2_click_times = []    
reaction_start_time = 0    
player1_reaction_time = 0    
player2_reaction_time = 0    
reaction_triggered = False    
current_page = "home"    
active_buttons = []    
reaction_timer = None    
game_start_time = 0    
game_duration = 10  # 手速测试时长（秒）    
    
# 清除屏幕    
def clear_screen():    
    global active_buttons    
    # 清除所有海龟对象    
    for turtle_obj in screen.turtles():    
        turtle_obj.clear()    
        turtle_obj.hideturtle()    
        
    # 清除活动按钮    
    active_buttons = []    
        
    # 取消任何待处理的计时器    
    if reaction_timer:    
        screen.ontimer(None)  # 取消所有定时器    
    
# 绘制按钮    
def draw_button(x, y, width, height, text, color, text_color, action=None):    
    button = turtle.Turtle()    
    button.penup()    
    button.hideturtle()    
    button.speed(0)    
        
    # 绘制按钮背景    
    button.goto(x, y)    
    button.fillcolor(color)    
    button.begin_fill()    
    for _ in range(2):    
        button.forward(width)    
        button.right(90)    
        button.forward(height)    
        button.right(90)    
    button.end_fill()    
        
    # 绘制按钮文字    
    button.goto(x + width/2, y - height/2 - 10)    
    button.color(text_color)    
    button.write(text, align="center", font=("Arial", 16, "bold"))    
        
    # 添加按钮信息    
    if action:    
        button_info = {    
            "turtle": button,    
            "coords": (x, x+width, y-height, y),    
            "action": action    
        }    
        active_buttons.append(button_info)    
        
    return button    
    
# 记录点击时间（手速测试）  
def record_click(player):  
    """记录玩家在手速测试中的点击时间"""  
    current_time = time.time() - game_start_time  
    if player == 1:  
        player1_click_times.append(current_time)  
    else:  
        player2_click_times.append(current_time)  

# 全局点击处理    
def handle_click(x, y):    
    global reaction_triggered, player1_reaction_time, player2_reaction_time
    
    # 检查是否点击了按钮      
    for button in active_buttons:      
        x1, x2, y1, y2 = button["coords"]      
        if x1 <= x <= x2 and y1 <= y <= y2:      
            button["action"]()  # 直接调用按钮动作      
            return      
          
    # 处理游戏特定点击    
    if current_page == "click_speed":    
        # 在手速测试页面，点击玩家按钮    
        if -200 <= x <= -50 and -100 <= y <= 0:  # 玩家1按钮区域    
            record_click(1)    
        elif 50 <= x <= 200 and -100 <= y <= 0:  # 玩家2按钮区域    
            record_click(2)    
        
    elif current_page == "reaction_speed" and reaction_triggered:      
        current_time = (time.time() - reaction_start_time) * 1000  # 转换为毫秒      
        # 在反应速度测试页面，记录玩家反应时间      
        if -400 <= x <= -50 and -150 <= y <= -50:  # 玩家1区域      
            if player1_reaction_time == 0:  # 只记录第一次点击      
                player1_reaction_time = current_time      
                if p1_area: p1_area.fillcolor("#90EE90")  # 点击后变色反馈      
        elif 50 <= x <= 400 and -150 <= y <= -50:  # 玩家2区域      
            if player2_reaction_time == 0:  # 只记录第一次点击      
                player2_reaction_time = current_time      
                if p2_area: p2_area.fillcolor("#90EE90")  # 点击后变色反馈      
          
        # 如果两位玩家都已完成反应测试，则显示结果      
        if player1_reaction_time > 0 and player2_reaction_time > 0:      
            reaction_triggered = False      
            time.sleep(0.5)  # 短暂延迟后显示结果      
            show_results()  

# 开始手速测试  
def start_click_speed():  
    """初始化并开始手速测试游戏"""  
    global current_page, game_start_time  
    clear_screen()  
    current_page = "click_speed"  
      
    # 重置玩家数据  
    global player1_click_times, player2_click_times  
    player1_click_times = []  
    player2_click_times = []  
      
    # 绘制游戏界面  
    title = turtle.Turtle()  
    title.penup()  
    title.hideturtle()  
    title.goto(0, 200)  
    title.write("手速测试", align="center", font=("Arial", 32, "bold"))  
      
    instructions = turtle.Turtle()  
    instructions.penup()  
    instructions.hideturtle()  
    instructions.goto(0, 150)  
    instructions.write(f"{game_duration}秒内尽可能快地点击你的按钮",   
                      align="center", font=("Arial", 18, "normal"))  
      
    # 绘制玩家按钮（使用lambda表达式处理点击事件）  
    draw_button(-200, 0, 150, 100, player1_name, "#FF6B6B", "white", lambda: record_click(1))  
    draw_button(50, 0, 150, 100, player2_name, "#4D96FF", "white", lambda: record_click(2))  
      
    # 初始化倒计时显示  
    countdown = turtle.Turtle()  
    countdown.penup()  
    countdown.hideturtle()  
    countdown.goto(0, 50)  
      
    # 开始游戏计时  
    game_start_time = time.time()  
    update_countdown(countdown)  

# 更新倒计时显示  
def update_countdown(countdown_turtle):  
    """实时更新游戏倒计时"""  
    elapsed = time.time() - game_start_time  
    remaining = max(0, game_duration - elapsed)  
      
    # 更新倒计时文本  
    countdown_turtle.clear()  
    countdown_turtle.write(f"剩余时间: {remaining:.1f}秒",   
                         align="center", font=("Arial", 24, "bold"))  
      
    if remaining > 0:  
        # 继续更新倒计时  
        screen.ontimer(lambda c=countdown_turtle: update_countdown(c), 100)  
    else:  
        # 游戏结束，显示结果  
        time.sleep(0.5)  
        show_results()  

# 开始反应速度测试  
def start_reaction_speed():    
    """初始化并开始反应速度测试游戏"""  
    global current_page, reaction_triggered, reaction_start_time, p1_area, p2_area    
    clear_screen()    
    current_page = "reaction_speed"    
      
    # 重置玩家反应时间数据  
    global player1_reaction_time, player2_reaction_time    
    player1_reaction_time = 0    
    player2_reaction_time = 0    
    reaction_triggered = False
      
    # 绘制游戏界面  
    title = turtle.Turtle()    
    title.penup()    
    title.hideturtle()    
    title.goto(0, 200)    
    title.write("反应速度测试", align="center", font=("Arial", 32, "bold"))    
      
    instructions = turtle.Turtle()    
    instructions.penup()    
    instructions.hideturtle()    
    instructions.goto(0, 150)    
    instructions.write("看到你的区域出现后，立即点击！",   
                     align="center", font=("Arial", 18, "normal"))    
      
    # 绘制玩家反应区域  
    p1_area = turtle.Turtle()    
    p1_area.penup()    
    p1_area.hideturtle()    
    p1_area.speed(0)  
    p1_area.goto(-400, -50)    
    p1_area.fillcolor("#FFD6D6")    
    p1_area.begin_fill()    
    for _ in range(2):    
        p1_area.forward(350)    
        p1_area.right(90)    
        p1_area.forward(100)    
        p1_area.right(90)    
    p1_area.end_fill()    
    p1_area.goto(-225, -100)  # 玩家1名称位置修正  
    p1_area.color("black")
    p1_area.write(player1_name, align="center", font=("Arial", 16, "bold"))    
      
    p2_area = turtle.Turtle()    
    p2_area.penup()    
    p2_area.hideturtle()    
    p2_area.speed(0)  
    p2_area.goto(50, -50)  # 修正玩家2区域的起点  
    p2_area.fillcolor("#D6E5FF")    
    p2_area.begin_fill()    
    for _ in range(2):    
        p2_area.forward(350)    
        p2_area.right(90)    
        p2_area.forward(100)    
        p2_area.right(90)    
    p2_area.end_fill()    
    p2_area.goto(225, -100)  # 玩家2名称位置修正  
    p2_area.color("black")
    p2_area.write(player2_name, align="center", font=("Arial", 16, "bold"))    
      
    # 随机延迟后开始测试
    screen.ontimer(start_reaction_test, random.randint(1000, 3000))

def start_reaction_test():
    """正式开始反应测试"""
    global reaction_triggered, reaction_start_time
    reaction_triggered = True
    reaction_start_time = time.time()
    
    # 改变区域颜色提示可以点击了
    if p1_area:
        p1_area.fillcolor("#FF6B6B")
    if p2_area:
        p2_area.fillcolor("#4D96FF")

# 显示测试结果  
def show_results():  
    """展示手速和反应速度测试的最终结果"""  
    global current_page  
    clear_screen()  
    current_page = "results"  
      
    # 绘制结果标题  
    title = turtle.Turtle()  
    title.penup()  
    title.hideturtle()  
    title.goto(0, 250)  
    title.write("测试结果", align="center", font=("Arial", 32, "bold"))  
      
    # 计算测试数据  
    p1_clicks = len(player1_click_times)  
    p2_clicks = len(player2_click_times)  
    p1_reaction = player1_reaction_time  
    p2_reaction = player2_reaction_time  
      
    # 初始化结果表格绘制器  
    results = turtle.Turtle()  
    results.penup()  
    results.hideturtle()  
      
    # 绘制表格标题行  
    results.goto(-300, 180)  
    results.write("玩家", align="center", font=("Arial", 20, "bold"))  
    results.goto(-100, 180)  
    results.write("点击次数", align="center", font=("Arial", 20, "bold"))  
    results.goto(100, 180)  
    results.write("平均点击/秒", align="center", font=("Arial", 20, "bold"))  
    results.goto(300, 180)  
    results.write("反应时间(ms)", align="center", font=("Arial", 20, "bold"))  
      
    # 绘制玩家1结果行  
    results.goto(-300, 120)  
    results.color("#FF6B6B")  
    results.write(player1_name, align="center", font=("Arial", 18, "bold"))  
    results.goto(-100, 120)  
    results.write(str(p1_clicks), align="center", font=("Arial", 18))  
    results.goto(100, 120)  
    results.write(f"{p1_clicks/game_duration:.1f}", align="center", font=("Arial", 18))  
    results.goto(300, 120)  
    results.write(f"{p1_reaction:.0f}" if p1_reaction > 0 else "N/A",   
                align="center", font=("Arial", 18))  
      
    # 绘制玩家2结果行  
    results.goto(-300, 60)  
    results.color("#4D96FF")  
    results.write(player2_name, align="center", font=("Arial", 18, "bold"))  
    results.goto(-100, 60)  
    results.write(str(p2_clicks), align="center", font=("Arial", 18))  
    results.goto(100, 60)  
    results.write(f"{p2_clicks/game_duration:.1f}", align="center", font=("Arial", 18))  
    results.goto(300, 60)  
    results.write(f"{p2_reaction:.0f}" if p2_reaction > 0 else "N/A",   
                align="center", font=("Arial", 18))  
      
    # 添加返回首页按钮  
    draw_button(-100, -150, 200, 60, "返回首页", "#6ECB63", "white", home_page)  

# 获取玩家名称  
def get_player_names():  
    """通过对话框获取两位玩家的名称"""  
    global player1_name, player2_name  
      
    # 使用Turtle的文本输入框获取玩家名称  
    player1_name = screen.textinput("玩家1名称", "请输入玩家1名称:")  
    player2_name = screen.textinput("玩家2名称", "请输入玩家2名称:")  
      
    # 设置默认名称  
    player1_name = player1_name if player1_name else "玩家1"  
    player2_name = player2_name if player2_name else "玩家2"  
      
    # 显示主页面  
    home_page()  

# 安全退出游戏  
def close_game():  
    """安全关闭游戏窗口并退出程序"""  
    turtle.bye()  # 关闭Turtle图形窗口  
    sys.exit(0)   # 正确调用sys.exit()函数

# 显示主页面  
def home_page():  
    """显示游戏主菜单界面"""  
    global current_page  
    clear_screen()  
    current_page = "home"  
      
    # 绘制主标题  
    title = turtle.Turtle()  
    title.penup()  
    title.hideturtle()  
    title.goto(0, 200)  
    title.write("玩家手速与反应力测试", align="center", font=("Arial", 32, "bold"))  
      
    # 显示对战玩家信息  
    players = turtle.Turtle()  
    players.penup()  
    players.hideturtle()  
    players.goto(0, 120)  
    players.write(f"{player1_name}  VS  {player2_name}",   
                align="center", font=("Arial", 24, "normal"))  
      
    # 绘制功能按钮  
    draw_button(-350, 50, 300, 80, "手速测试", "#FF6B6B", "white", start_click_speed)  
    draw_button(50, 50, 300, 80, "反应速度测试", "#4D96FF", "white", start_reaction_speed)  
    draw_button(-150, -100, 300, 80, "重新输入玩家名称", "#6A67CE", "white", get_player_names)  
    draw_button(-150, -200, 300, 80, "退出游戏", "#555555", "white", close_game)  

# 游戏主程序  
def main():  
    """游戏主入口函数"""  
    # 设置点击事件监听  
    screen.onclick(handle_click)  
      
    # 获取玩家名称并显示主页面  
    get_player_names()  
      
    # 启动游戏主循环  
    turtle.mainloop()  

# 程序入口  
if __name__ == "__main__":  
    main()