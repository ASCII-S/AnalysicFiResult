import pandas as pd 
import os
import sys
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib import rcParams

de_path = './TMP'	#your csv folder 
print("Default Folder:",de_path)
path = input("请输入应用数据所在的文件夹：") or de_path

save_directory = path+'/save2pic/'
if not os.path.exists(save_directory):
	os.makedirs(save_directory)
files = [file for file in os.listdir(path) if file.endswith('.csv')]



font_params = {
    'font.family': 'serif',      # 设置字体族，比如'serif'、'sans-serif'等
    'font.serif': 'Times New Roman',  # 设置字体名称
    'font.size': 16,             # 设置字体大小
    'axes.labelsize': 30,        # 设置坐标轴标签字体大小
    'axes.titlesize': 34,        # 设置坐标轴标题字体大小
    'xtick.labelsize': 26,       # 设置X轴刻度字体大小
    'ytick.labelsize': 26,       # 设置Y轴刻度字体大小
    'legend.fontsize': 36,       # 设置图例字体大小
    'axes.linewidth': 2,         # 设置坐标轴框架粗细
}
rcParams.update(font_params)

matplotlib.rc('figure', figsize = (20, 8))

def percent_formatter(x, pos):
    return f'{int(x)}%'

def draw_png(fname,df,x_axis,y_axis):
	
	plt.gca().xaxis.set_major_formatter(FuncFormatter(percent_formatter))
	
	plt.title(fname.replace('.csv',''))
	plt.xlabel(x_axis.replace("'",""))
	plt.ylabel(y_axis.replace("'",""))

	plt.xlim(0, 100)
	plt.ylim(0, 100)
	
	plt.xticks([0,20, 40, 60, 80, 100])
	plt.yticks([20, 40, 60, 80, 100])

	plt.plot(df[x_axis], df[y_axis], 'k-', alpha=1, linewidth=2, label='acc')
	#plt.show()
	
	

def save_pic(path,files,save_directory):
	for file in files:
		if 'InsClass' in file:
			continue
		csvfile = path+'/'+file
		app_filename = file.replace(".csv",'')
		print (csvfile)
		
		data = pd.read_csv(csvfile)
		df =pd.DataFrame(data)	
		errortype = ['Masked%','Crash%']
		sdcapp = ['hpl'] 
		if app_filename in sdcapp:
			errortype_more = ['Sdc%','Masked%+Sdc%']
			for yy in errortype_more:
				draw_png(str(file),df,'Dynamic Execution',yy)
				save_filename = app_filename+'_'+yy+'.png'
				save_path = os.path.join(save_directory, save_filename)
				print ('\t'+save_filename+'\t \t\thas save in '+ save_directory)
				plt.savefig(save_path, dpi=600)
				plt.close()
		for y in errortype:
			draw_png(str(file),df,'Dynamic Execution',y)
			save_filename = app_filename+'_'+y+'.png'
			save_path = os.path.join(save_directory, save_filename)
			print ('\t'+save_filename+'\t \t\thas save in '+ save_directory)
			plt.savefig(save_path, dpi=600)
			plt.close()
			
		#plt.show()

	#	df.to_excel(writer, sheet_name=file, index=False)
	#	writer.save()
	#	writer.close()

if __name__ == '__main__':

	save_pic(path,files,save_directory)
