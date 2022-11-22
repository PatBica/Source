from logging import error
from math import ceil
from operator import contains
import openpyxl
import csv
from posixpath import split
import wx
from numpy import *
app = wx.App()
filename = wx.FileSelector("Choose an CSV file")
app.MainLoop()

with open(filename) as file:
    csvreader = csv.reader(file)
    total = []
    sorted = []
    for row in csvreader:
        total.append(row)
    for element in total:
        try:
            all = []
            all.append(element[33])
            all.append(element[10])
            all.append(element[11])
            sorted.append(all)
        except:
            None
    y = []
    for x in sorted:
        if not x[0] in y:
            y.append(x[0])
        else:
            None
    n = len(y)
    m = [[] for _ in range(n)]
    p = array(m).tolist()
    i=0
    while i < n:
        x = y[i]
        m[i].append(x)
        i +=1
    for x in sorted:
        nazis = [x[0]]
        index = m.index(nazis)
        p[index].append(x[1])
        p[index].append(x[2])
    Bubebkis = 0
    for kid in p:
        ble = 0
        x1 = []
        x2 = []
        for toletespapirs in range(len(kid)):
            if toletespapirs % 2 == 1:
                ble += float(kid[(toletespapirs)])
            else:
                RABARBERS = kid[toletespapirs].split("\ ")
                RAUSIS = [int(RABARBERS) for RABARBERS in RABARBERS]
                x1.append(RAUSIS[0])
                x2.append(RAUSIS[1])
                actual = sum(x1)
                total = sum(x2)
        blee = round(ble,2)
        print(y[Bubebkis],blee,"kg","\t",actual,total)
        Bubebkis +=1
    print(m)
    print(n)

