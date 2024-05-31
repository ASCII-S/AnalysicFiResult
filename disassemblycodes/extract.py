import re
import csv
import pandas as pd
import os
import sys

# 直接运行会在当前目录下创建一个ext_asbly文件夹，将对汇编文件的格式化文件存储进去

# below claim new column
INDEX = []
IP =[]
INS_FULL = []
INS = [] 
TO_ADDRESS = []
NOTE= []
FUC = []	#which FUC one IP belongs to

original_stdout = sys.stdout

def find_in_dac(filename, data):
    filepath = filename
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    count = 0 
    fuc = 'unknown'
    for line in lines:
        if '0000000000' in line[0:10]:
            fuc = line[17:-2]
            continue
        ip = line[2:8].replace(' ', '')
        if len(ip) < 6:
            continue
        ip = str(ip)
        tmp = re.search(r'^.{32}(.*?)(?=\#|$)', line)
        if tmp:
            tmp = tmp.group(1).strip()
        else:
            tmp = line[32:62]
        note = re.search(r'(?<=#).*$', line)
        if note:
            note = note.group().strip()
        tmp = ' '.join(tmp.split())
        if len(tmp.replace(' ', '')) == 0:  # 处理特殊情况，例如 0000000000400ae0 <fopen@plt>
            continue
        tmp = tmp.split(' ')
        ins_full = str(tmp).replace('\n', '').replace('\r', '').replace('"', '').replace('[', '').replace(']', '').replace("'", "")
        ins = tmp[0]
        to_address = re.search(r'\b[0-9a-fA-F]{6}\b', ins_full)
        if to_address:
            to_address = to_address.group().strip()

        INDEX.append(count)
        IP.append(ip)
        INS_FULL.append(ins_full)
        INS.append(ins)
        TO_ADDRESS.append(to_address)
        NOTE.append(note)
        FUC.append(fuc)
        
        #print(count,'\t',ip,'\t',ins_full,'\t',ins,'\t',note,'\t',fuc )
        count += 1
    
    data['INDEX'] = INDEX
    data['IP'] = IP
    data['INS_FULL'] = INS_FULL
    data['INS'] = INS
    data['TO_ADDRESS'] = TO_ADDRESS
    data['NOTE'] = NOTE
    data['FUC'] = FUC



def custom_sort(x):
    return (x != '<main>').astype(int)


def write_dataframe_to_csv(filename, data):
    # 提取文件名（不包括扩展名）
    file_name_without_extension = filename.split('.')[0]
    file_name_without_extension = file_name_without_extension + '_asbly'
    # 创建文件夹路径
    folder_path = 'ext_asbly'
    
    # 如果文件夹不存在，则创建文件夹
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # 保存到 CSV 文件中
    file_path = os.path.join(folder_path, file_name_without_extension + '.csv')
    data.to_csv(file_path, index=False)


def write_dataframe_to_txt(filename, data):
    # 提取文件名（不包括扩展名）
    file_name_without_extension = filename.split('.')[0]
    file_name_without_extension = file_name_without_extension + '_node'
    # 创建文件夹路径
    folder_path = 'node_txt'
    
    # 如果文件夹不存在，则创建文件夹
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # 保存到 CSV 文件中
    file_path = os.path.join(folder_path, file_name_without_extension + '.txt')

    #data.to_csv(file_path, index=False)
    with open(file_path, 'w') as f:
        # 重定向标准输出到文件
        sys.stdout = f
        
        # 打印内容到标准输出（实际上是写入到文件中）
        former_func = ''
        for index, row in data.iterrows():
            now_func = row['FUC']
            if former_func != now_func:
                if former_func != '':
                    print(former_func,';\n')
                former_func = now_func
            print("{},{};".format(row['INS_FULL'],row['INDEX']))



        # 恢复原始的标准输出对象
        sys.stdout = original_stdout


def folder_do(folder_path):
    # 获取文件夹中的所有文件
    files = os.listdir(folder_path)
    for file in files:
        if file.endswith('.txt'):  # 仅处理 txt 文件
            data = pd.DataFrame({
            'INDEX': [],
            'IP': [],
            'INS_FULL': [],
            'INS': [],
            'TO_ADDRESS': [],
            'NOTE': [],
            'FUC': []
            })
            filename = os.path.join(folder_path, file).replace('./','')
            find_in_dac(filename, data)
            #data = data.sort_values(by='FUC', key=custom_sort)
            write_dataframe_to_csv(filename, data)
            #write_dataframe_to_txt(filename, data)
            print (file)



if __name__ == '__main__':

    # 定义文件夹路径
    folder_path = './'

    
    folder_do(folder_path)

    print("All Completed!")
    
