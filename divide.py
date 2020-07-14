# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 10:22:23 2020

@author: 25223
"""


import tkinter as tk
from tkinter import filedialog
import struct
import numpy as np

root=tk.Tk()
root.withdraw()

Filepath = filedialog.askopenfilename()
# Filepath="D:/dan Java/3ds/Lockin X (V).bin"
print(Filepath)
file=open(Filepath,"rb")

nx=int(struct.unpack(">i",file.read(4))[0])
ny=int(struct.unpack(">i",file.read(4))[0])
nlayers=int(struct.unpack(">i",file.read(4))[0])

print(nlayers)

x=np.zeros(nx,dtype=np.float64)
y=np.zeros(ny,dtype=np.float64)
v=np.zeros(nlayers,dtype=np.float64)



for i in range(nx):
    data=np.float64(struct.unpack(">d",file.read(8))[0])
    x[i]=data
    # print(data)
    
for j in range(ny):
    data=np.float64(struct.unpack(">d",file.read(8))[0])
    # y[j]=data
    
for n in range(nlayers):
    data=np.float64(struct.unpack(">d",file.read(8))[0])
    v[n]=data
    print(data)
    

    
dataset=np.zeros((nlayers,nx,ny),dtype=np.float64)

for n in range (nlayers):
    for i in range(nx):
        for j in range(ny):
            data=np.float64(struct.unpack(">d",file.read(8))[0])
            dataset[n][i][j]=data
            
for n in range(nlayers):
    binfile=open(str(int(v[n]*1000))+"vDIDV.bin","wb")
    data=struct.pack(">i",nx)
    binfile.write(data)
    data=struct.pack(">i",ny)
    binfile.write(data)  
    data=struct.pack(">d",v[n])
    binfile.write(data)
    data=struct.pack(">d",0)
    binfile.write(data)
    
    for i in range(len(x)):
        data=struct.pack(">d",x[i])
        binfile.write(data)
    for i in range(len(y)):
        data=struct.pack(">d",y[i])
        binfile.write(data)
        
    for i in range(nx):
        for j in range(ny):
            data=struct.pack(">d",dataset[n][i][j])
            binfile.write(data)
    binfile.close()
    print(n)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
