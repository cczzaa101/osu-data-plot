import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import polyval
from numpy import ma
from matplotlib import scale as mscale
from matplotlib import transforms as mtransforms
from matplotlib import ticker
from matplotlib.ticker import Formatter, FixedLocator
from matplotlib import rcParams

ppthres = 3748 #lowest pp to be plotted on graph
ppupthres = 0
width = 1024
height = 768
mydpi = 80

plt.figure(figsize=(width/mydpi, height/mydpi),dpi=mydpi)
rcParams['axes.axisbelow'] = False
rcParams['axes.formatter.useoffset']=False
list = None
ax = None
import os
csvList = os.listdir('csv')
folderList = ['acc-pp','pp-pc','pp-rank','rank-pc']
for i in folderList:
    if not os.path.exists(i):
        os.makedirs(i)
    

def render_nodata_message():
    plt.text(0.5, 0.5,'no data',
    horizontalalignment='center',
    verticalalignment='center',
    transform = plt.gca().transAxes,
    color='red', 
    size = 12,
    bbox={'facecolor':'red', 'alpha':0.5, 'pad':10}        
    )
  
def setupcolor(ax):
    ax.patch.set_facecolor('black')
    ax.spines['bottom'].set_color('#ffffff')
    ax.spines['top'].set_color('#ffffff')
    ax.spines['left'].set_color('#ffffff')
    ax.spines['right'].set_color('#ffffff')
    label = plt.ylabel("y-label")
    ax.tick_params(axis='y', which='both', colors='white')
    [i.set_color("white") for i in ax.get_xticklabels()]
    #[i.set_color("white") for i in ax.get_yticklabels()]
    
    
def plot_100_avg_ppvspc(date,cl):
    l = 19000 #lowest pp to be plotted on graph
    u = 0
    plt.clf()
    
    plt.title(date,color='white')
    x = []
    y = []
    tempx=0
    tempy=0
    lim=1 #每lim个取平均值
    num=0
    for i in list:
        temp = i.split(',')
        tempx+=(int(temp[5]))
        tempy+=(int(temp[7]))
        u = max(u,int(temp[7]))
        l = min(l,int(temp[7]))
        num+=1
        if(num==lim):
            x.append(tempx/lim)
            y.append(tempy/lim)
            num=0
            tempx=0
            tempy=0
    
    global ppupthres,ppthres
    ppupthres =u + 1000
    ppthres = l
    plt.scatter(x,y,s=len(x)*[1.5],alpha=0.3,color = cl)
    '''
    z1 = np.polyfit(x,y,1)
    p1=np.poly1d(z1)
    x2 = np.linspace(26000,110000,1000)
    y2 = [ polyval(p,[z1[1],z1[0]]) for p in x2 ]
    #print(y2)
    #plt.plot(x2,y2)
    print(p1)
    '''
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(which='major', color='white', linestyle='-',linewidth=1.5)
    plt.grid(which='minor', color='#eeeeee', linestyle='-')
    ax = plt.gca()

    ax.set_axisbelow(True)
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    ax.yaxis.set_minor_formatter(ticker.FormatStrFormatter('%d'))
    #ax.set_yticks(np.arange(4000,11000,1000))
    #ax.set_xticks(np.append(np.arange(1000,10000,1000) , np.arange(10000,100000,10000)))
    #ax.set_yticklabels([1000*i for i in range(4,10)])
    #ax.set_xticklabels([1000]+3*['']+[5000]+4*['']+[10000]+3*['']+[50000])
    if(cl=='red'):
        render_nodata_message()
    ax.set_ylim([ppthres,ppupthres])
    ax.set_xlim([1000,300000])
    setupcolor(ax)
    plt.savefig('pp-pc/'+date+'.png',facecolor='black')

    
def plot_accpp(date,cl):
    plt.clf()
    #plt.figure(figsize=(width/mydpi, height/mydpi),dpi=mydpi)
    plt.title(date,color='white')
    x = []
    y = []
    for i in list:
        temp = i.split(',')
        if(float(temp[4].replace('%',''))<90): continue
        x.append(float(temp[4].replace('%','')))
        y.append(int(temp[7]))
    
    plt.scatter(x,y,s=len(x)*[1.5],alpha=0.3,color=cl)
    ax = plt.gca()
    #ax.set_yticks([0,10,100,1000,10000])
    plt.xscale('linear')
    plt.yscale('log')
    plt.grid(which='major', color='white', linestyle='-',linewidth=0.5)
    plt.grid(which='minor', color='#eeeeee', linestyle='-',linewidth=0.25)
    ax.yaxis.set_minor_formatter(ticker.FormatStrFormatter('%d'))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    ax.xaxis.set_minor_formatter(ticker.FormatStrFormatter('%d'))
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    ax.set_xticks(np.arange(95,100))
    
    #ax.set_yticks([4000,5000,6000,7000,8000,9000,10000])
    #print(ppupthres,ppthres)
    ax.set_ylim([ppthres,ppupthres])
    ax.set_xlim([95,100])
    if(cl=='red'):
        render_nodata_message()
    #ax.text((95+100)/2, (ppthres+14000)/2, 'no data', alpha = 0.5, color = 'red', size = 15, bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
    ax.set_axisbelow(True)
    setupcolor(ax)
    plt.savefig('acc-pp/'+date+'.png',facecolor='black')

def plot_pcrank(date,cl):
    plt.clf()
    #plt.figure(figsize=(width/mydpi, height/mydpi),dpi=mydpi)
    plt.title(date,color='white')
    x = []
    y = []
    for i in list:
        temp = i.split(',')
        x.append(int(temp[5]))
        y.append(int(temp[0]))
    
    plt.scatter(x,y,s=len(x)*[1.5],alpha=0.3,color=cl)
    ax = plt.gca()
    #ax.set_yticks([0,10,100,1000,10000])
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(which='major', color='white', linestyle='-',linewidth=0.5)
    plt.grid(which='minor', color='#eeeeee', linestyle='-',linewidth=0.25)
    #ax.xaxis.set_minor_formatter(ticker.FormatStrFormatter('%d'))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    ax.set_ylim([1,10000])
    ax.set_xlim([1000,300000])
    ax.set_axisbelow(True)
    if(cl=='red'):
        render_nodata_message()
    plt.gca().invert_yaxis()
    #plt.show()
    setupcolor(ax)
    plt.savefig('rank-pc/'+date+'.png',facecolor='black')
    
def plot_pprank(date,cl):
    plt.clf()
    #plt.figure(figsize=(width/mydpi, height/mydpi),dpi=mydpi)
    plt.title(date,color='white')
    x = []
    y = []
    for i in list:
        temp = i.split(',')
        x.append(int(temp[0]))
        y.append(int(temp[7]))
    
    plt.plot(x,y,color = cl)
    ax = plt.gca()
    #ax.set_yticks([0,10,100,1000,10000])
    plt.xscale('log')
    #plt.yscale('log')
    plt.grid(which='major', color='white', linestyle='-',linewidth=0.5)
    plt.grid(which='minor', color='#eeeeee', linestyle='-',linewidth=0.25)
    #ax.xaxis.set_minor_formatter(ticker.FormatStrFormatter('%d'))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    ax.set_ylim([ppthres,ppupthres])
    ax.set_xlim([1,10000])
    ax.set_axisbelow(True)
    if(cl=='red'):
        render_nodata_message()
    #plt.show()
    setupcolor(ax)
    plt.savefig('pp-rank/'+date+'.png',facecolor='black')
    
def plot_main(i):
    if(i==0):
        plot_100_avg_ppvspc(date,c)
    if(i==1):
        plot_accpp(date,c)
    if(i==2):
        plot_pcrank(date,c)
    if(i==3):
        plot_pprank(date,c)
        
for i in csvList:
    global date,c
    date = i[:8]
    f = open("csv/"+i,"r")
    rawData = f.read()
    f.close()
    #list = rawData.split('\n')
    if(len(rawData.split('\n'))<=10001):
        print(date, ' not enough players!')
        c = 'red'
        #continue
    else:
        print(date, ' complete')
        list = rawData.split('\n')
        list = list[1:10001]
        c = 'yellow'
    if(list == None): continue
    for i in range(4):
        plot_main(i)

for i in folderList:
    tp = os.listdir(i)
    tp = sorted(tp)
    count = 0
    for file in tp:
        os.rename(i+'/'+file, i+'/'+('000'+str(count))[ len(str(count)):]+'.png')
        count+=1
