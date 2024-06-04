import os
import pandas as pd
## 这个文件是用来为csv文件中IP列添加前缀'0x'的，为了不让这一列在excel中显示为科学计数法，避免了数据在保存时发生错误
# 定义一个函数来处理IP列的每一个元素
def add_0x(ip):
    return '0x' + str(ip)

# 指定包含CSV文件的文件夹路径
folder_path = './Result_csv0417'
modified_folder_path = './Result_csv0417_add0x'
if not os.path.exists(modified_folder_path):
        print(f"文件夹 {modified_folder_path} 不存在，将会创建它。")
        os.makedirs(modified_folder_path)

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):  # 确保文件是CSV文件
        file_path = os.path.join(folder_path, filename)
        # 读取CSV文件
        df = pd.read_csv(file_path)
        # 检查是否存在IP列
        if 'IP' in df.columns:
            # 对IP列应用函数
            df['IP'] = df['IP'].apply(add_0x)
            # 保存修改后的CSV文件
            modified_file_path = os.path.join(modified_folder_path, filename)
            df.to_csv(modified_file_path, index=False)
            print(filename,'\t已经存入',modified_file_path)
        else:
            print(f"文件 '{filename}' 中不存在名为 'IP' 的列，跳过处理。")
