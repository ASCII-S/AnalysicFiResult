import os
import csv
import pandas as pd
import sys

#本程序对app.csv进行分析，csv中列包含IP	REG	fi	seg	result_class	FUC	INS	INS_FULL	Masked	Crash	Dynamic Execution	Masked%	Crash%
#本程序作用后：  
#功能1：结果列中追加了INS_type，do=1
#功能2：在node文件夹中产生CrashOnSameIp, do=2
do = 1
#功能3：该功能会再生成一个Uknown_文件，用来提取程序ins_type中属于unknown的部分，以供进一步划分指令
filter_ukn_ctrl = 1
#根目录
base_dir = '../Result_csv0529/'
#存放appcsv文件的文件夹
choose_default_path = base_dir + '/fi'
#node文件夹，用来存放opcode
choose_opcode_path = base_dir + '/node'
crashon_sameins_savepath = choose_opcode_path
#这是你在choose_opcode_path中的文件，利用该文件的分类规则对ins进行类型分类
choose_opcode_name = "opcode.csv"
#以下是生成文件的前缀
ins_class_pre = 'InsClass_'
unknown_class_pre = "UknType_"



def readop(app_file):
    # 读取 CSV 文件并使用第一行作为列名
    df = pd.read_csv(app_file, header=0)

    # 对每一列按照字典序排序
    for column in df.columns:
        df[column] = df[column].dropna().str.lower()
        df[column] = df[column].sort_values().tolist()
    return df

def read_and_sort_csv(app_file,colname):
    # 读取 CSV 文件
    df = pd.read_csv(app_file)
    
    # 按照 'INS' 列进行排序
    sorted_df = df.sort_values(by=[colname, 'fi'])
    #sorted_df.reset_index(drop=True, inplace=True)
    return sorted_df

def crashon_sameins(merged_df,file_name):
    df = merged_df.sort_values(by=['IP'])
    columns_to_drop = [col for col in df.columns if col.startswith('CrashOnSameIP')]
    df.drop(columns=columns_to_drop, inplace=True)

    # 按照 IP 列对 DataFrame 进行分组，计算 Crash 列的总和和分组大小
    grouped = df.groupby('IP')['Crash'].agg(['sum', 'count'])
    # 计算新列 CrashOnSameIP
    grouped['CrashOnSameIP'] = 100.0 * grouped['sum'] / grouped['count']

    # 将新列合并到原始 DataFrame 中，并按照 IP 列去重
    dfAddCosi = df.merge(grouped[['count','CrashOnSameIP']], how='left', on='IP').drop_duplicates(subset=['IP'])
    # 保存到指定位置folder_path
    folder_path = os.path.join(crashon_sameins_savepath,'CrashOnSameIp')
    savefile(dfAddCosi[['IP', 'CrashOnSameIP','count']],folder_path,file_name)

    #print(dfAddCosi)

    # 打印结果
    #print(df)
    
    
    return df


def filter_ukn_ins(INS_value):
    global ukndf
    if INS_value in ukndf['INS_value'].values:
        # 更新 inscount 列的值
        ukndf.loc[ukndf['INS_value'] == INS_value, 'inscount'] += 1
    else:
        # 新增一行，并设置 inscount 为 1
        new_row = pd.DataFrame({'INS_value': [INS_value], 'inscount': [1]})
        ukndf = pd.concat([ukndf, new_row], ignore_index=True)


def add_INS_type_column(df_readop, sorted_df,file_name,):
    # 为sorted_df添加INS_type列
    # 初始化一个与 sorted_df['INS'] 列长度相同的列表，所有元素为空字符串
    INS_type_list = [''] * len(sorted_df['INS'])  # 用于存储每个 INS 对应的类别列名
    index = 0
    # 遍历 sorted_df 的 'INS' 列的每一行
    for INS_value in sorted_df['INS']:
        find_type = 0   #表示这个指令是否被归类了
        # 遍历 df_readop 的列，看看INS_value在不在某一列中
        for column in df_readop.columns:
            # 判断 INS_value 是否在 df_readop 的当前列中
            if INS_value in df_readop[column].values:
                INS_type_list[index]=column
                find_type = 1
                break  
        # 如果找不到匹配项，如何操作
        if find_type == 0:
            INS_type_list[index]='UnKnown'
            if filter_ukn_ctrl == 1:
                filter_ukn_ins(INS_value)
                
        index+=1
    #print(len(sorted_df['INS']),len(INS_type_list))
    sorted_df['INS_type'] = INS_type_list
    
    print(file_name , '\t 中添加opcode-type列,deal_app 完成!')
    return sorted_df


def move_column_to_position(df, column_name, target_position):
    # 获取指定列的数据
    column_data = df[column_name]
    
    # 删除指定列
    df.drop(labels=[column_name], axis=1, inplace=True)
    
    # 在目标位置插入指定列
    df.insert(loc=target_position, column=column_name, value=column_data)





def GenerateIns_class_file(ins_class_file,app_file,file_name,merged_df):
    data = merged_df

    # 创建 DataFrame
    df = pd.DataFrame(data)

    # 按照 INS_type 排序并获取唯一值
    ins_types = sorted(df['INS_type'].unique())

    # 打印所有 INS_type 类型
    #print(file_name+','+','       +','.join(ins_types) + '\n')

    # 打印每种 INS_type 对应的数量
    counts = [df[df['INS_type'] == ins_type].shape[0] for ins_type in ins_types]
    #print(file_name+','+'Count,'   +','.join(map(str, counts)) + '\n')

    # 使用 groupby 对 INS_type 进行分组，然后对 crash 列求和
    crash_sum_by_ins_type = df.groupby('INS_type')['Crash'].sum()

    # 打印每种 INS_type 对应的 Crash% 的平均值
    Crash_rate = merged_df.groupby('INS_type')['Crash'].mean()*100
    #print(file_name+','+'Crash%,'  +','.join(map(lambda x: '{:.2f}'.format(x), Crash_rate)) + '\n\n')

    # 保存到 CSV 文件
    ins_class_file = ins_class_file 
    with open(ins_class_file, 'a') as f:
        f.write(file_name+','+'Ins_Type,'       +','.join(ins_types) + '\n')
        f.write(file_name+','+'Count,'          +','.join(map(str, counts)) + '\n')
        f.write(file_name+','+'CrashCount,'     +','.join(map(str, crash_sum_by_ins_type)) + '\n')
        f.write(file_name+','+'Crash%,'         +','.join(map(lambda x: '{:.2f}'.format(x), Crash_rate)) + '\n\n')

   



def savefile(merged_df,folder_path,file_name):
    # 确保文件夹存在，如果不存在则创建它
    if not os.path.exists(folder_path):
        print(folder_path,'文件夹不存在,正在创建')
        #return
        #sys.exit()
        os.makedirs(folder_path)

    # 去掉文件名的后缀
    file_name_without_extension = os.path.splitext(file_name)[0]
    # 生成完整的文件路径
    app_file = os.path.join(folder_path, file_name_without_extension + ".csv")

    #保证生成文件干净不重叠
    if os.path.exists(app_file):
        #if input(f"确定重建 '{app_file}' ?(输入1确认删除)\n") == 1:
        os.remove(app_file)
        print(f"'{app_file}'\t\t已成功重建。")
    else:
        print(f"'{app_file}'\t\t不存在。即将创建。")
        with open(app_file, mode='w', newline='', encoding='utf-8') as file:
            # 不写入任何内容
            pass

    # 将 DataFrame 保存为 .csv 文件
    merged_df.to_csv(app_file, index=False)
    print(app_file,'\t\t已经写入完毕!')
    




def deal_app(folder_path,file_name,opcode_type_file,ins_class_file):   ##对应用程序csv文件的操作都放在这里
    app_file = os.path.join(folder_path, file_name+'.csv')
    if app_file == ins_class_file:
        print ("\nPASS InsType_ ~\n")
        return
    global ukndf,ukn_class_name
    ukn_class_file = os.path.join(folder_path,ukn_class_name)
    if app_file == ukn_class_file:
        print (f"\nPASS {ukn_class_file} ~\n")
        return
    df_readop = readop(opcode_type_file)
    sorted_df = read_and_sort_csv(app_file,'INS')

    #调用函数为 sorted_df 添加新列 INS_type
    
    merged_df = add_INS_type_column(df_readop, sorted_df,file_name)#原地添加列，因此函数中不需要知filename
    
    #将修改后的dataframe保存到原来的位置，以fi为序
    merged_df = merged_df.sort_values(by='fi')
    merged_df.reset_index(drop=True, inplace=True)
    
    if do == 2:
        #统计相同指令的crash率
        merged_df2 = crashon_sameins(merged_df,file_name)
    if do ==1:
        savefile(merged_df,folder_path,file_name)
        #额外生成文件
        GenerateIns_class_file(ins_class_file,app_file,file_name,merged_df)

    print('\n')





if __name__ == "__main__":
    default_path = choose_default_path
    print('默认文件夹为:',default_path)
    #folder_path = input("请输入csv所在文件夹路径: ").strip() or default_path
    folder_path = default_path
    print('文件夹已重定向为:',folder_path)

    opcode_path = choose_opcode_path
    opcode_name = choose_opcode_name
    opcode_type_file = os.path.join(opcode_path, opcode_name)
    print('opcode来源:',opcode_type_file)

    
    ins_class_name = ins_class_pre+str(folder_path).split('/')[-1]+'.csv'
    ins_class_file = os.path.join(folder_path, ins_class_name)

    ukn_class_name = unknown_class_pre+str(folder_path).split('/')[-1]+'.csv'
    ukndf = pd.DataFrame(columns=['INS_value', 'inscount'])

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv')and ins_class_pre not in file_name:  # 确保只处理 CSV 文件
            file_name = os.path.splitext(file_name)[0]
            # 在这里执行你的操作，比如读取 CSV 文件并进行处理
            deal_app(folder_path,file_name,opcode_type_file,ins_class_file)
    if filter_ukn_ctrl == 1:
        savefile(ukndf,folder_path,ukn_class_name)