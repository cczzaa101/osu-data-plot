import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.polynomial import polyval
from numpy import ma
from matplotlib import scale as mscale
from matplotlib import transforms as mtransforms
from matplotlib import ticker
from matplotlib.ticker import Formatter, FixedLocator
from matplotlib import rcParams


ppthres = 4600 #lowest pp to be plotted on graph
rcParams['axes.axisbelow'] = False
rcParams['axes.formatter.useoffset']=False
list = []

import os
csvList = os.listdir('csv')

    
class ACCScale(mscale.ScaleBase):

    # The scale class must have a member ``name`` that defines the
    # string used to select the scale.  For example,
    # ``gca().set_yscale("mercator")`` would be used to select this
    # scale.
    name = 'acc'

    def __init__(self, axis, **kwargs):
        mscale.ScaleBase.__init__(self)

    def get_transform(self):
        return self.accTransform()
    def set_default_locators_and_formatters(self, axis): 
        major = [1, 5, 10, 12, 14, 16, 18, 20, 25, 28, 30] #+ [range(31,60)]
        axis.set_major_locator(ticker.FixedLocator(major))

    class accTransform(mtransforms.Transform):
        # There are two value members that must be defined.
        # ``input_dims`` and ``output_dims`` specify number of input
        # dimensions and output dimensions to the transformation.
        # These are used by the transformation framework to do some
        # error checking and prevent incompatible transformations from
        # being connected together.  When defining transforms for a
        # scale, which are, by definition, separable and have only one
        # dimension, these members should always be set to 1.
        input_dims = 1
        output_dims = 1
        is_separable = True

        def __init__(self):
            mtransforms.Transform.__init__(self)

        def transform_non_affine(self, a):
            """
            This transform takes an Nx1 ``numpy`` array and returns a
            transformed copy.  Since the range of the Mercator scale
            is limited by the user-specified threshold, the input
            array must be masked to contain only valid values.
            ``matplotlib`` will handle masked arrays and remove the
            out-of-range data from the plot.  Importantly, the
            ``transform`` method *must* return an array that is the
            same shape as the input array, since these values need to
            remain synchronized with values in the other dimension.
            """
            return np.power(a,5)

        def inverted(self):
            """
            Override this method so matplotlib knows how to get the
            inverse transform for this transform.
            """
            return ACCScale.InvertedACCTRansform(
                )

    class InvertedACCTRansform(mtransforms.Transform):
        input_dims = 1
        output_dims = 1
        is_separable = True

        def __init__(self):
            mtransforms.Transform.__init__(self)

        def transform_non_affine(self, a):
            return np.power(a,1/5)

        def inverted(self):
            return ACCScale.accTransform()

# Now that the Scale class has been defined, it must be registered so
# that ``matplotlib`` can find it.
mscale.register_scale(ACCScale)


def plot_100_avg_ppvspc(date):
    plt.clf()
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
        num+=1
        if(num==lim):
            x.append(tempx/lim)
            y.append(tempy/lim)
            num=0
            tempx=0
            tempy=0
    
    plt.scatter(x,y,s=len(x)*[1.5],alpha=0.3)
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
    plt.grid(which='major', color='b', linestyle='-',linewidth=1.5)
    plt.grid(which='minor', color='r', linestyle='-')
    ax = plt.gca()

    ax.set_axisbelow(True)
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    ax.yaxis.set_minor_formatter(ticker.FormatStrFormatter('%d'))
    #ax.set_yticks(np.arange(4000,11000,1000))
    #ax.set_xticks(np.append(np.arange(1000,10000,1000) , np.arange(10000,100000,10000)))
    #ax.set_yticklabels([1000*i for i in range(4,10)])
    #ax.set_xticklabels([1000]+3*['']+[5000]+4*['']+[10000]+3*['']+[50000])
    ax.set_ylim([ppthres,14000])
    ax.set_xlim([1000,300000])
    plt.savefig('pp-pc/'+date+'.png')

    
def plot_accpp(date):
    plt.clf()
    x = []
    y = []
    for i in list:
        temp = i.split(',')
        if(float(temp[4].replace('%',''))<90): continue
        x.append(float(temp[4].replace('%','')))
        y.append(int(temp[7]))
    
    plt.scatter(x,y,s=len(x)*[1.5],alpha=0.3)
    ax = plt.gca()
    #ax.set_yticks([0,10,100,1000,10000])
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(which='major', color='b', linestyle='-',linewidth=0.5)
    plt.grid(which='minor', color='r', linestyle='-',linewidth=0.25)
    ax.xaxis.set_minor_formatter(ticker.FormatStrFormatter('%d'))
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    ax.set_xticks(np.arange(91,100))
    ax.set_ylim([ppthres,14000])
    ax.set_xlim([90,100])
    ax.set_axisbelow(True)
    plt.savefig('acc-pp/'+date+'.png')

def plot_pcrank(date):
    plt.clf()
    x = []
    y = []
    for i in list:
        temp = i.split(',')
        x.append(int(temp[5]))
        y.append(int(temp[0]))
    
    plt.scatter(x,y,s=len(x)*[1.5],alpha=0.3)
    ax = plt.gca()
    #ax.set_yticks([0,10,100,1000,10000])
    plt.xscale('log')
    plt.yscale('log')
    plt.grid(which='major', color='b', linestyle='-',linewidth=0.5)
    plt.grid(which='minor', color='r', linestyle='-',linewidth=0.25)
    #ax.xaxis.set_minor_formatter(ticker.FormatStrFormatter('%d'))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    ax.set_ylim([1,10000])
    ax.set_xlim([1000,300000])
    ax.set_axisbelow(True)
    plt.gca().invert_yaxis()
    #plt.show()
    plt.savefig('rank-pc/'+date+'.png')
    
def plot_pprank(date):
    plt.clf()
    x = []
    y = []
    for i in list:
        temp = i.split(',')
        x.append(int(temp[0]))
        y.append(int(temp[7]))
    
    plt.plot(x,y)
    ax = plt.gca()
    #ax.set_yticks([0,10,100,1000,10000])
    plt.xscale('log')
    #plt.yscale('log')
    plt.grid(which='major', color='b', linestyle='-',linewidth=0.5)
    plt.grid(which='minor', color='r', linestyle='-',linewidth=0.25)
    #ax.xaxis.set_minor_formatter(ticker.FormatStrFormatter('%d'))
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    ax.set_ylim([ppthres,14000])
    ax.set_xlim([1,10000])
    ax.set_axisbelow(True)
    #plt.show()
    plt.savefig('pp-rank/'+date+'.png')
    
for i in csvList:
    date = i[:8]
    f = open("csv/"+i,"r")
    rawData = f.read()
    f.close()
    list = rawData.split('\n')
    list = list[1:10001]
    plot_100_avg_ppvspc(date)
    plot_accpp(date)
    plot_pcrank(date)
    plot_pprank(date)

