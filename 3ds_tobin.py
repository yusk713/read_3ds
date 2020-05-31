# -*- coding: utf-8 -*-
"""
Created on Sun May 31 20:47:09 2020

@author: 25223
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 28 08:41:38 2020

@author: 25223
"""


import tkinter as tk
from tkinter import filedialog
import struct
import numpy as np
# root=tk.Tk()
# root.withdraw()


    
def main():
    Filepath ="D:/dan Java/3ds/Grid Spectroscopy002.3ds"
    # Filepath = filedialog.askopenfilename() 
    file=open(Filepath,"rb")
    

    
    headlist=[]#记录数据的测量信息
    
    head=""
    
    
    
    
    while head.find("HEADER_END")==-1:
            head=str(file.readline())
            head=head[2:-5]
            # print(head)
            headlist.append(head)
    headlist=headlist[0:-2]    
    print(headlist)
        

    
    dim=headlist[0][headlist[0].index("=")+2:-1]
    
    dim=dim.split("x")
    nx=int(dim[0]) 
    ny=int(dim[1])#记录数据尺寸
    print(nx,ny)

    
    channel=headlist[9][headlist[9].index("=")+2:-1]
    channel=channel.split(";")#用list记录测量模式
    nchannels=len(channel)#记录测量模式的个数

    
    signal=headlist[3][headlist[3].index("=")+2:-1]#记录signal
    signal_type=0
    if signal.find("Z (m)")==1:
    	signal_type = 1;

    grid=headlist[1][headlist[1].index("=")+1:]
    grid=grid.split(";")
    cx=float(grid[0])
    cy=float(grid[1])
    lx=float(grid[2])
    ly=float(grid[3])
    angle=float(grid[4])
    
    x=np.linspace(cx-lx/2, cx+lx/2, nx)
    y=np.linspace(cy-ly/2, cy+ly/2, ny)
    

    
    nlayers=headlist[8][headlist[8].index("=")+1:]
    nlayers=int(nlayers)
    layername=[None]*nlayers            
    for j in range(nlayers):
        if j<10:
            layername[j]="00000"+str(j)
        elif j in range(10,100):
            layername[j]="0000"+str(j)            
        elif j in range(100,1000):
            layername[j]="000"+str(j)            
        elif j in range(1000,10000):
            layername[j]="00"+str(j)
        else:
            layername[j]=""+str(j) 
    print(layername)

    
    vstart=0;vstop=0;vexist=False
    if signal_type == 0:
        for i in range(0,len(headlist)):
            if headlist[i].find("Bias Spectroscopy>Sweep Start (V)")==1:
                vstart = float(headlist[i][headlist[i].index("=")+1:])
            if headlist[i].find("Bias Spectroscopy>Sweep End (V)")==1:
                vstop = float(headlist[i][headlist[i].index("=")+1:])
        if vstart!=0 or vstop!=0:
            v=np.linspace(vstart,vstop,nlayers)
            vexsit=True
            
    if signal_type == 1:
        for i in range(0,len(headlist)):
            if headlist[i].find("Z Spectroscopy>Initial Z-offset (m)")==1:
                vstart = float(headlist[i][headlist[i].index("=")+1:])
            if headlist[i].find("Z Spectroscopy>Sweep distance (m)")==1:
                vstop = float(headlist[i][headlist[i].index("=")+1:])
        if vstart!=0 or vstop!=0:
            v=np.linspace(vstart,vstop,nlayers)
            vexsit=True
    				
    nPtParam=headlist[6][headlist[6].index("=")+1:]
    nPtParam=int(nPtParam)#记录Parameters
    print(nchannels)
    print(nlayers)
    print(nPtParam)
    
    
    #获取voltage array（在无法根据signal_type获取的条件下）
    if not vexist:

       
        data=file.read(4)
        print(data)
        print(type(data))
        vstart=np.float64((struct.unpack(">f",data )[0]))
        data=file.read(4)
        vstop=np.float64((struct.unpack(">f", data)[0]))
        v=np.linspace(vstart,vstop,nlayers)
        if vstart>vstop:
            v=v[::-1]
        print(vstart,vstop)
    else:
        file.read(4)
        file.read(4)
    
    dataset=np.zeros((nchannels,nlayers,nx,ny),dtype=np.float64)
    topo=np.zeros((nx,ny),dtype=np.float64)
    print(topo.shape)
    count=0
    # filenotFull=False#判断数据是否填满
    flt=np.zeros(nPtParam-2,dtype=np.float64)
    for i in range(0,nx):
        for j in range(0,ny):
            if count!=0:
                one=np.float64(struct.unpack(">f",file.read(4)))
                two=np.float64(struct.unpack(">f",file.read(4)))
                # print(one,two)
                
            for k in range(nPtParam-2):
                flt[k]=np.float64(struct.unpack(">f",file.read(4)))
                
            topo[i][j]=flt[2]
            
            for m in range(0,nchannels):
                for n in range(0,nlayers):
                    dataset[m][n][i][j]=np.float64(struct.unpack(">f",file.read(4)))
            count+=1
            
    for m in range(0,nchannels):
        for n in range(0,nlayers):
            if angle!=180:
                dataset=dataset[:,::-1]

            if angle==90 or nx==ny:
                datacopy=dataset
                for i in range (nchannels):
                    for j in range(nlayers):
                        for m in range(nx):
                            for n in range (ny):
                                datacopy[m][n]=data[ny-n-1][m]
                                data[m][n]=datacopy[n][m]
                
    print(topo.shape)

    topocopy=topo            
    if angle==90 or nx==ny:
        for m in range(nx):
            for n in range (ny):
                topocopy[m][n]=topo[ny-n-1][m]
                topo[m][n]=topocopy[n][m]
        
        
    if angle!=180:
        topo=topo[:,::-1]
        y=y[::-1]
        
    for i in range(5):
        for j in range(5):
            for k in range(5):
                print(dataset[1][i][j][k])
        
    
    
    file.close()
    
    topobinfile=open("3ds.bin","wb")
    data=struct.pack(">i",nx)
    topobinfile.write(data)
    data=struct.pack(">i",ny)
    topobinfile.write(data)  
    print(len(x))
    print(len(y))
    print(len(v))
    print(topo.shape)
    for i in range(len(x)):
        data=struct.pack(">d",x[i])
        topobinfile.write(data)
    for i in range(len(y)):
        data=struct.pack(">d",y[i])
        topobinfile.write(data)
    data=struct.pack(">d",1.0)
    topobinfile.write(data)
    data=struct.pack(">d",0)
    topobinfile.write(data)
    
    for i in range(nx):
        for j in range(ny):
            data=struct.pack(">d",topo[i][j])
            topobinfile.write(data)
    topobinfile.close()
    
    for i in range(nchannels):
        if channel[i].find("\\")==1:
            channel[i]=channel[i].split("\\")[0]+channel[i].split("\\")[1]
        if channel[i].find("/")==1:
            channel[i]=channel[i].split("/")[0]+channel[i].split("/")[1]
        binfile=open(channel[i]+".bin","wb")
        data=struct.pack(">i",nx)
        binfile.write(data)
        data=struct.pack(">i",ny)
        binfile.write(data)  
        data=struct.pack(">i",nlayers)
        binfile.write(data)
        for m in range(len(x)):
            data=struct.pack(">d",x[i])
            binfile.write(data)
        for n in range(len(y)):
            data=struct.pack(">d",y[i])
            binfile.write(data)  
        for j in range(len(v)):
            data=struct.pack(">d",v[i])
            binfile.write(data) 
        for j in range(nlayers):
            print(" "+str(j))
            for m in range(nx):
                for n in range(ny):
                    data=struct.pack(">d",dataset[i][j][m][n])
                    binfile.write(data)
                    
        for j in range(nlayers):
            data=struct.pack(">d",len(layername[j]))
            binfile.write(data)
            data=bytes(layername[j],"utf-8")
            binfile.write(data)
            
        binfile.close()

main()
# print('Filepath:',Filepath)