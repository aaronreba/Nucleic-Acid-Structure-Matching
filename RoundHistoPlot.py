#!/usr/bin/env python

#$1: list of data files.
#pass like so: "file1.txt,file2.txt,file3.txt"
#$2: save name
#$3: title
#$4: x label
#$5: y label
#$6...: options: log for log scale

import matplotlib.pylab as pl
import matplotlib.pyplot as plt
import numpy
import sys

def main(argv=None):
    colorcycle = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
    color = 0
    plotFiles = argv[1].split(',')
    
    step = False
    ncum = False
    
    if len(argv) > 6:
        for option in argv[6:]:
            if option == 'log':
                plt.yscale('log')
            elif option == 'step':
                step = True
            elif option == 'ncum':
                ncum = True
    
    for eachFile in plotFiles:
        data = numpy.genfromtxt(eachFile, names=('n1'))
        
        xAxisSeries = numpy.arange(0, data['n1'].max() + 2, 1)
        frequency = numpy.histogram(data['n1'], bins=xAxisSeries)
        xAxis = frequency[1][:-1][::2]
        yAxis = frequency[0][::2]
        print xAxis
        print yAxis
        if step:
            xPoints = []
            xPoints.append(xAxis[0])
            for x in xAxis[1:]:
                xPoints.append(x)
                xPoints.append(x)
            print xPoints, len(xPoints)
            yPoints = []
            yPoints.append(yAxis[0])
            for y in frequency[0][1:]:
                yPoints.append(y)
                yPoints.append(y)
            print yPoints
        else:
            xPoints = frequency[1][:-1]
            yPoints = frequency[0]
        
        if ncum:
            newyPoints = []
            for iy, y in enumerate(yAxis):
                newyPoints.append(sum(yAxis[iy:]))
            if step:
                yPoints = []
                yPoints.append(yAxis[0])
                for y in newyPoints[1:]:
                    yPoints.append(y)
                    yPoints.append(y)
                print yPoints, len(yPoints)
            else:
                yPoints = newyPoints
            
        
        plt.title(argv[3])
        plt.xlabel(argv[4])
        plt.ylabel(argv[5])
        
        label = eachFile.split('/')[-1]
        
        plt.plot(xPoints,
                 yPoints,
                 colorcycle[color] + '-',
                 label=label,
                 linewidth=1)
        
        color += 1
        if color == len(colorcycle):
            color = 0
    
    leg = plt.legend(loc=2,
                     fancybox=True)
    leg.get_frame().set_alpha(0.5)
    plt.savefig(argv[2])
    plt.clf()

if __name__ == '__main__':
    main(sys.argv)
