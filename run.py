from id_validator import validator
import csv
import sys
import os

def writerFile(writer, name, id, sex, address, birthday, age, others):
    # 使用 Python open 方法打开文件进行写入，
    writer.writerow([name, id, sex, address, birthday, age] + others)

args = sys.argv
current_dir, filename = os.path.split(os.path.abspath(sys.argv[0]))
inputFile = current_dir+os.sep+'input.csv' if len(args) < 2 else args[1]
outFile = current_dir+os.sep+'output.csv' if len(args) < 3 else args[2]
logPath = current_dir+os.sep+'log'
# print(current_dir,filename,os.path.realpath(sys.argv[0]))

with open(inputFile) as csvFile:
    # 创建一个 CSV Reader 对象
    reader = csv.reader(csvFile)
    logOutput = open(logPath,'w')
    # 设置行数所以我们知道哪一行的标题
    with open(outFile, mode='w') as output:
        writer = csv.writer(output, delimiter=',', quotechar='"', quoting = csv.QUOTE_MINIMAL)
        line = 0
        for row in reader:
            others = []
            for index in range(len(row)):
                if index > 1:
                    others.append(row[index])
            if line == 0:
                writerFile(writer,'姓名', '身份证', '性别', '城市', '生日', '年龄', others)
                line += 1
            else:
                line += 1
                name = row[0]
                id = row[1]
                if not validator.is_valid(id):
                    log = '第'+str(line)+'行:"'+id+'"'+'不是正确的身份证号'
                    print(log)
                    logOutput.write(log+'\n')
                    continue
                data = validator.get_info(id)
                sex = '男' if int(data['sex']) == 1 else '女'
                address = data['address']
                birthDay = data['birthday_code']
                age = data['age']
                # 防止Excel打开时精度丢失
                idInput = id+'\t'
                printLine = '第'+str(line)+'行:'
                print(printLine,name, id, sex, address, birthDay, age)
                writerFile(writer, name, idInput, sex, address, birthDay, age, others)
    logOutput.close()
