import numpy as np
import math
from scipy.stats import poisson

# 定义参数
MTBF = 60 * 60 * 6        
MTBFault = MTBF         # 把所有的application都看做50%的crash概率 12h一次

fault_rate = 1 / MTBF    # 平均故障发生率（每个时间片的故障概率） 6h transient faults comes


fault_rate = [fault_rate, fault_rate/2, fault_rate/4]

computation_all_time = 365 * 24 * 60 * 60 * 5
years_5 = 365 * 24 * 60 * 60 
# 模拟检查点过程

f = open('sim_result_5years.txt','w')

def ckpt_simulation(app, crash_probability, phase, checkpoint_interval_raw, checkpoint_cost,our):
    # 模拟故障发生
    print("start stimulation...")
    time = 0
    checkpoint_point_time = 0
    checkpoint_interval = checkpoint_interval_raw   # 没有调整间隔的固定检查点长度
    fault_time_dur_ckpt = 0
    all_ckpts = 0
    no_need_ckpts = 0
    total_fault = 0
    computation_time = 0   # 程序运行时间
    checkpoints = []

    while computation_time < computation_all_time:
        time += 1
        computation_time += 1
        crash_rate = fault_rate  # 未考虑弹性时的crash概率

        # 判断是否需要做检查点了，以及做检查点的开销
        if time - (checkpoint_point_time + checkpoint_cost) >= checkpoint_interval:
            # print('last ckpt:\t',checkpoint_point_time)
            checkpoint_point_time = time
            checkpoints.append(checkpoint_point_time)
            time += checkpoint_cost 
            # print('now time:\t',time)
            # print('creat ckpt:\t',checkpoint_point_time)
            #  print('ckpt intevral:\t',checkpoint_interval)
            if fault_time_dur_ckpt != 0:
                # print('crashs during ckpts:\t',fault_time_dur_ckpt)
                pass
            all_ckpts += 1
            if fault_time_dur_ckpt == 0 :
                no_need_ckpts += 1
            fault_time_dur_ckpt = 0
            continue

        for index, _ in enumerate(phase):
            #各个阶段的crashrate和checkpoint_interval各不相同，按阶段初始化他们
            if computation_time/ computation_all_time > phase[index]:
                continue
            if computation_time/ computation_all_time <= phase[index]:
                crash_rate = fault_rate * crash_probability[index]
                if our is True:
                    checkpoint_interval =  int(math.sqrt(2 * MTBF / crash_probability[index] *checkpoint_cost))


        faults_this_time = np.random.poisson(crash_rate)
        if faults_this_time > 0:
            # print(f"{faults_this_time} fault(s) occurred at time {time}")
            total_fault += 1
            # 故障发生，查看上一次做检查点的时间是什么时候
            # computation_all_time += (time - checkpoint_point_time)
            computation_time = computation_time - (time - checkpoint_point_time) + checkpoint_cost # 有部分浪费掉的需要重新计算，减去不算作为有效时间
            time += checkpoint_cost   # 加载检查点的开销
            # print('last ckpt:{}\tnow time:{}\twasted time:{}'.format(checkpoint_point_time,time,time - checkpoint_point_time))
            checkpoint_point_time = time   # 类似于重新开始周期性的检查点
            fault_time_dur_ckpt += 1

    # 输出检查点信息
    if our:
        print(f"CKPT:{app}")
        f.write(f"CKPT:{app}\n")
    else:
        print(f"WITHOUT:{app}")
        f.write(f"WITHOUT:{app}\n")
    f.write(f'checkpoint cost: {checkpoint_cost}\n')
    f.write(f"Checkpoints: {checkpoints[:10]}\n")
    f.write('total ckpts:{}\nno need ckpts:{}\t\n'.format(all_ckpts, no_need_ckpts))
    f.write(f'total fault:{total_fault}\n')
    f.write(f'efficiency:{computation_time/time}\n')
    f.write('\n')
    print(f'{app}: efficiency:{computation_time/time}')
    print(f'checkpoint cost: {checkpoint_cost}\n')

    

def data_prepare_and_simu():
    hpl_crash = [0.099,0.2334,0.0875]
    hpl_phase = [0.4,0.58,1]

    miniFE_phase = [0.07, 0.41, 0.48, 1]
    miniFE_crash = [0.26, 0.176, 0.23, 0.26]

    apps = ['hpl','miniFE']

    crash_probability = [hpl_crash,miniFE_crash]
    phase= [hpl_phase,miniFE_phase]

    checkpoint_cost = [15,150,1500]   # 检查点的开销 15s 150s 1500s
    checkpoint_interval_raw = [int(math.sqrt(2*MTBFault*cost)) for cost in checkpoint_cost]  # 检查点间隔（单位：时间片） 

    is_our = [True, False]
    for index, app in enumerate(apps):
        for c_index, cost in enumerate(checkpoint_cost):
            for our in is_our:
                ckpt_simulation(app,crash_probability[index],phase[index], 
                                checkpoint_interval_raw[c_index],cost, our)


data_prepare_and_simu()