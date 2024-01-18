import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import sys
import numpy as np
from numpy.core.defchararray import startswith
"""
Args:

    audio_result = FFT result text file
    lenth_s = the freq start scope you want to start from the result txt
            default is 1.
    lenth_e = the freq end scope you want to get from the result txt 
            should be "all" or numbers (1000, 10000, 20000)
"""

fs = []
ch1 = []
ch2 = []
ch3 = []
CH_2 = False

audio_result = sys.argv[1]
lenth_e = sys.argv[2]

print(sys.argv)

if lenth_e != 'all':
    lenth_e = int(lenth_e)
    full = False
else:
    full = True


with open(audio_result,'r')as f:
    text = f.read()

text = text.split('\n')
if full:
    scope = text[1:]
else:
    scope = text[1:lenth_e+2]

for i in scope:
    x = i.split('\t')
    fs.append(float(x[0]))
    ch1.append(float(x[1]))
    if len(x) > 2:
        ch2.append(float(x[2]))
        ch3.append(float(x[3]))
        CH_2 = True

plt.style.use('ggplot')
if CH_2:
    fig, axes = plt.subplots(nrows=1, ncols=3,figsize=(15,6))
    ax1, ax2, ax3 = axes.ravel()

    ax1.plot(ch1, color=u'blue',label='ch1')
    ax2.plot(ch2, color=u'green',label='ch2')
    ax3.plot(ch3, color=u'yellow',label='ch3')

    ax1.xaxis.set_ticks_position('bottom')
    ax1.yaxis.set_ticks_position('left')
    ax2.xaxis.set_ticks_position('bottom')
    ax2.yaxis.set_ticks_position('left')
    ax3.xaxis.set_ticks_position('bottom')
    ax3.yaxis.set_ticks_position('left')

    ax1.set_title('ch1-frequency-fft')
    ax2.set_title('ch2-frequency-fft')
    ax3.set_title('ch3-frequency-fft')

    ax1.set_xlabel('freq')
    ax2.set_xlabel('freq')
    ax3.set_xlabel('freq')


    ax1.set_ylabel('s_dbfs')
    ax2.set_ylabel('s_dbfs')
    ax3.set_ylabel('s_dbfs')

    plt.legend(loc='best')
    plt.savefig('{}_plot.png'.format(audio_result), dpi=600, bbox_inches='tight')
    plt.show()

else:
    #   Only CH1
    fig = plt.figure(figsize=(16,9))
    ax1 = fig.add_subplot(1,1,1) 
    ax1.plot(np.array(ch1), color=u'blue',label='ch1')
    ax1.xaxis.set_ticks_position('bottom')
    ax1.yaxis.set_ticks_position('left')
    ax1.set_title('{}\nch1-frequency-fft'.format(audio_result.replace('.txt','')))
    ax1.set_xlabel('freq')
    x_major_locator=MultipleLocator(1000)
    ax=plt.gca()
    ax.xaxis.set_major_locator(x_major_locator)
    if full:
        plt.xlim(-50,24500)
    else:
        plt.xlim(-1000,lenth_e+1000)
    ax1.set_ylabel('s_dbfs')
    plt.legend(loc='best')
    plt.savefig('{}_plot.png'.format(audio_result.replace('.txt','')), dpi=600, bbox_inches='tight')
    plt.show()