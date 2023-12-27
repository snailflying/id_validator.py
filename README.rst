1.生成可执行文件
pyinstaller -F run.py 

普通使用：
1.按照文件夹内input.csv内的样式，将需要处理的Excel另存为input.csv，并替换掉文件夹内的input.csv.

2.直接双击run，或者打开terminal，cd到run文件所在目录，并运行 ./run(如果被安全机制拦截，请打开系统设置，给run添加权限)

3.用Excel打开output.csv即可，如果有需要，可以另存为Excel格式。


高级用法：
1.指定输入输出文件名称：
./run xxx1.csv  xxx2.csv

xxx1.csv：输入文件
xxx2.csv：输入文件