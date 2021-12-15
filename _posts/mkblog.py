#!/usr/bin/python
import time  # 引入time模块
import sys


 
ticks = time.time()
filename =  time.strftime("%Y-%m-%d", time.localtime()) + "-"+sys.argv[1]+".md"

print(filename)
with open('./'+filename, 'w') as f:
    f.write("---\n")
    f.write("layout: post\n")
    f.write("title: ")
    f.write(sys.argv[1]+"\n")
    f.write("categories: \n")
    f.write("description: \n")
    f.write("keywords: \n")
    f.write("---\n")
    f.write("\n")
    f.write("简介\n")
    f.write("\n")
    f.write("\n")
    f.write("内容\n")
    f.write("\n")