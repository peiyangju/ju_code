import time    
    
def sum_to_one_million():    
    start_time = time.time()  # 记录开始时间    
    total = 0    
        
    for i in range(1, 1_000_000001):  # 从1加到1,000,000
        total += i    
            
        # 每10万次打印一次进度（避免打印太频繁）    
        if i % 100_000 == 0:    
            print(f"已加到 {i:,}，当前总和：{total:,}")    
        
    end_time = time.time()  # 记录结束时间    
    elapsed_time = end_time - start_time    
        
    print("\n计算完成！")    
    print(f"1加到1,000,000000的总和是：{total:,}")
    print(f"总耗时：{elapsed_time:.2f}秒")    
    
# 调用函数    
sum_to_one_million()  
