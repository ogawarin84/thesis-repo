# -*- coding: utf-8 -*-
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
PATH = r"C:\Users\Home\Desktop\理论生成汇总\0802理论生成汇总\量子平面概率动力学模型_完整版_ver5.md"
lines = open(PATH, encoding='utf-8').read().split('\n')
line = lines[1195]
old = '依赖交互对象的实时输入——文件本身是"静态地图"'
print("old repr:", repr(old))
print("in line:", old in line)
print("dash in old:", [hex(ord(c)) for c in '——'])
print("dash in line:", [hex(ord(c)) for c in '——'])
