# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 02:11:30 2016

@author: 宇
"""

number=[0]
a=0
'''
while a!=0:
    a=0
    a=input("input the number:")
    number.append(a)
'''
number=[0,14,75,24,55,51,30,62,36,18,54,28,37,23,41,65,25,50,26,60,1,22,46,10,35,52]

table = [[1 for i in range(5)] for j in range(5)]

for i in range(5):
    for j in range(5):
        print('the',i+1,'line',j+1,'list:')
        table[i][j]= int(input())

print (table[0])
print(table[1])
print(table[2])
print(table[3])
print(table[4])
        
i=0
if table[0][0] in number and table[0][4] in number and table[4][0] in number and table[4][4] in number:
    print("match with four point")

for i in range(5):
    check=0
    for j in range(5):
        #print(j)
        if table[i][j] in number:
            check+=1
        if check == 5:
            print ("line",i+1,'match!')
        
for j in range(5):
    check = 0
    for i in range(5):
        #print(i)
        if table[i][j] in number:
            check+=1
    if check == 5:
        print ("list",j+1,'match!')
    
if table[4][0] in number and table[3][1] in number and table[2][2] in number and table[1][3] in number and table[0][4] in number:
    print("Left diagonal match!")
if table[0][0] in number and table[1][1] in number and table[2][2] in number and table[3][3] in number and table[4][4] in number:
    print("right diagonal match!")
