# -*- coding: utf-8 -*-

import os
import csv
import pandas as pd
#根目录下需要包含：1.app.csv文件夹2.node文件夹3.loops/slices文件夹
basedir = '../Result_csv0529/'

#这是保存appcsv的文件夹
choose_appcsvfolder = basedir + 'fi'

#这是最外侧的loops或slices文件夹
#choose_loopfolder = "./loops"
choose_loopfolder = basedir + 'slices'

###这是loops/app/内的loops或slices文件夹
#loop_inner_foldername = 'loops1.0'
loop_inner_foldername = 'slices'

#
CrashMapFileName = "slice_crash.map"
LoopsFileName = "slice.csv"
csvtitle = 'slice_name'
###这是你要运行的应用程序，使用'all'对choose_appcsvfolder中的所有应用程序进行分析
appnamechoose = 'all'


def get_folder_path(prompt):
    while True:
        folder_path = input(prompt)
        if os.path.isdir(folder_path):
            return folder_path
        else:
            print("输入的路径不是一个有效的文件夹，请重新输入。")


def count_ip_in_appdf(appdf,loopdf,file_path):

    #print(loopdf.head(5))
    loopdf['COUNT'] = 0
    loopdf['CRASHC'] = 0
    
    total_count = 0
    total_crash_sum = 0
    #print(loopdf.head(5),appdf.head(5))
    # 遍历 appdf 的 IP 列
    for ip in appdf['IP']:
        # 遍历 loopdf 的第二列
        for index, value in enumerate(loopdf.iloc[:, 1]):
            # 检查 value 是否与 appdf 中的 IP 元素相同
            value = str(value).replace("0x",'')

            if value == ip:
                loop_index = loopdf.index[index]
                loopdf.at[loop_index, 'COUNT'] += 1
                total_count += 1
                # 找到对应行的 Crash 值，并加到总和中
                crash_value = appdf.loc[appdf['IP'] == ip, 'Crash'].values[0]
                loopdf.at[loop_index, 'CRASHC'] += crash_value
                total_crash_sum += crash_value
        #print(total_count)
    
    
    print(total_count,total_crash_sum)
    
    loopdf.to_csv(file_path,index=False,header=False)
    return total_count,total_crash_sum


def count_ip_in_appdf2(appdf,loopdf,file_path):#对单个loop文件操作
    # 初始化指针
    app_index = 0
    loop_index = 0
    loopdf['COUNT'] = 0
    loopdf['CRASHC'] = 0
    total_count = 0
    total_crash_sum = 0
    # 开始双指针循环
    while loop_index < len(loopdf) and app_index < len(appdf):
        #loop_ip = loopdf.at[loop_index, 'IP'].replace('0x','')
        #app_ip = appdf.at[app_index, 'IP'].replace('0x','')
        loop_ip = loopdf.at[loop_index, 'IP']
        app_ip = appdf.at[app_index, 'IP']
        #print(loop_ip,app_ip)
        # 检查两个指针指向的 IP 是否相同    
        if loop_ip == app_ip:
            loopdf.at[loop_index, 'COUNT'] += 1
            total_count += 1
            # 找到对应行的 Crash 值，并加到 loopdf 中
            crash_value = appdf.at[app_index, 'Crash']
            loopdf.at[loop_index, 'CRASHC'] += crash_value
            total_crash_sum += crash_value

            #print(app_index,loop_index,loop_ip,app_ip,loopdf.at[loop_index, 'COUNT'],loopdf.at[loop_index, 'CRASHC'])
            # 指针移动
            app_index += 1
        elif loop_ip < app_ip:
            # 如果 loop_ip 小于 app_ip，向后移动 loop 指针
            loop_index += 1
        else:
            # 如果 loop_ip 大于 app_ip，向后移动 app 指针
            app_index += 1
    #print(total_count,total_crash_sum)
    #if total_count:
    #    print(1.0*total_crash_sum/total_count)
            
    #loopdf.to_csv(file_path,index=False,header=False)
    return total_count,total_crash_sum


def savemap(loopinfolder,loop_name,count,crashc):
    mapname = "slice_crash.map"
    result_file_path = os.path.join(loopinfolder, mapname)
    #将该loop文件的统计结果保存
    """with open(result_file_path, mode='a') as file:

        # 写入统计结果
        if count != 0 or crashc != 0:
            #writer.writerow([loop_name, count, crashc, "{:.2f}%".format(crashc/count*100)])
            file.write(loop_name.replace('.csv','')+' '+"{:.4f}".format(crashc/count)+'\n')
            #print(loop_name.replace('.csv','')+' '+"{:.2f}".format(crashc/count))
        #else:
            #writer.writerow([loop_name.replace('.csv','')+' '+'None'])
    """
    try:
        # 打开文件
        file = open(result_file_path, mode='a')
        
        # 写入统计结果
        if count != 0 or crashc != 0:
            file.write(loop_name.replace('.csv','')+' '+"{:.4f}".format(crashc/count)+'\n')
        
        # 关闭文件
        file.close()
    except IOError:
        print("无法打开文件或写入数据:",result_file_path,"")
        exit

    
def savecsv(loopinfolder,loop_name,count,crashc):
    mapname = "slice.csv"
    result_file_path = os.path.join(loopinfolder, mapname)
    #将该loop文件的统计结果保存
    """with open(result_file_path, mode='a',newline='') as file:
        writer = csv.writer(file)

        # 写入统计结果
        if count != 0 :
            writer.writerow([loop_name, count, crashc, "{:.4f}".format(crashc/count)])
            #print(loop_name.replace('.csv','')+' '+"{:.2f}".format(crashc/count))
        #else:
            #writer.writerow([loop_name.replace('.csv','')+' '+'None'])"""
    
    try:
        # 打开文件
        file = open(result_file_path, mode='a', newline='')

        # 创建 CSV writer 对象
        writer = csv.writer(file)

        # 写入统计结果
        if count != 0:
            writer.writerow([loop_name, count, crashc, "{:.4f}".format(crashc/count)])

        # 关闭文件
        file.close()
    except IOError:
        print("无法打开文件或写入数据:",result_file_path,"请关闭正在打开的文件，或暂停同步软件")


def deal_apploops(appcsvfolder,loopfolder,appname): #对单个app操作
    
    #读入app.csv
    appcsv = appname + '.csv'
    appfile = os.path.join(appcsvfolder, appcsv)
    appdf = pd.read_csv(appfile)
    appdf = appdf.sort_values(by='IP',ascending=True)
    appdf = appdf.reset_index(drop=True)
    appname_lower = appname.lower()

    #初始化结果文件LCM_file_path和LSC_file_path
    matched_folder = None
    for folder in os.listdir(loopfolder):
        # 检查loop文件夹名称是否与 appname 匹配（不区分大小写）
        if folder.lower() == appname_lower and os.path.isdir(os.path.join(loopfolder, folder)):
            matched_folder = os.path.join(loopfolder, folder)
            break
    if matched_folder:
        print(f"\n\t\t{appname}\nThe folder '{matched_folder}' contains the app '{appname}'.")
        # 如果需要，你可以在这里继续处理 matched_folder
    else:
        print(f"The app '{appname}' is not found in any folder within '{loopfolder}'.")
        return

    loopinfolder = os.path.join(matched_folder,loop_inner_foldername)
    if not os.path.exists(loopinfolder):
        print("不存在文件夹：\t",loopinfolder)
        return
    LCM_file_path = os.path.join(loopinfolder, CrashMapFileName)
    LSC_file_path = os.path.join(loopinfolder, LoopsFileName)
    
    #每次对所有loop分析前要保证结果文件干净，并且初始化title
    if os.path.exists(LCM_file_path):
        os.remove(LCM_file_path)
    if os.path.exists(LSC_file_path):
        os.remove(LSC_file_path)
    with open(LSC_file_path, mode='a',newline='') as file:
        writer = csv.writer(file)
        writer.writerow([csvtitle, 'COUNT', 'CRASHC', 'Crash%'])

    # 对每个文件的loop*.csv文件夹内进行操作
    print(loopinfolder,'\tis processing...... ') 
    loop_list = os.listdir(loopinfolder)
    for loop_name in loop_list:
        # 检查文件是否为 CSV 文件
        #print(loop_name)
        if loop_name.endswith(".csv") and loop_name !=LoopsFileName:
            # 构建文件的完整路径
            file_path = os.path.join(loopinfolder, loop_name)
            
            # 读取 loop*.csv 文件并转换为 DataFrame
            loopdf = pd.read_csv(file_path,usecols=[0], header=None,names=['IP'])
            #print("before col:\t",loopdf.shape[0])
            #丢弃loops列中的重复元素
            loopdf = loopdf.drop_duplicates(subset=loopdf.columns[0], keep=False)
            #print("after col:\t",loopdf.shape[0])

            loopdf = loopdf.sort_values(by=loopdf.columns[0],ascending=True)
            loopdf = loopdf.reset_index(drop=True)

            

            count, crashc = count_ip_in_appdf2(appdf,loopdf,file_path)
            #print('分析成功:\tslice_name:%s \n\t\tcount:%s \n\t\tcrashc:%s' % (loop_name,count,crashc))
            
            #print ("正在保存文件：\t",file_path)
            savemap(loopinfolder,loop_name,count,crashc)
            savecsv(loopinfolder,loop_name,count,crashc)

    print(loopinfolder,'\thas been done')
            

def main():
    #print("请输入应用程序csv数据所在文件夹路径：")
    appcsvfolder = choose_appcsvfolder
    #appcsvfolder = get_folder_path("应用程序csv数据所在文件夹路径：")


    #print("请输入loop所在文件夹路径：")
    loopfolder = choose_loopfolder
    #loopfolder = get_folder_path("loop所在文件夹文件夹路径：")
    
    
    appname = appnamechoose
    #appname = input("输入你要处理的应用程序:")
    if appname == 'all':
        app_list = os.listdir(appcsvfolder)
        for app_name in app_list:
            #对有统计数据的应用程序进行loop分析
            if os.path.isdir(os.path.join(appcsvfolder,app_name)):
                continue
            appname = app_name.replace('.csv','')
            if "InsClass" not in appname:
                deal_apploops(appcsvfolder,loopfolder,appname)
            #print(loopfolder,os.path.join(loopfolder, appname, "loops", "loops.csv"))
    else:
        deal_apploops(appcsvfolder,loopfolder,appname)

if __name__ == "__main__":
    main()