#!/usr/bin/env python

import sys
import numpy
import matplotlib.pyplot as plt
import matplotlib.lines as lines

colors = [('#000000'), ('#FF0000'), ('#00FF00'), ('#0000FF'), ('#FFCC00'), ('#FF00FF'), ('#00FFFF'), ('#0066FF'), ('#007700'), ('#CC9999')]

def main(argv=None):
    plot_file_name = sys.argv[1]
    plot_save_name = sys.argv[2]
    x_axis_size = int(sys.argv[3])
    
    plot_data = numpy.genfromtxt(plot_file_name, names=('time', 'score'), dtype=None)
    
    x_axis = []
    y_axis = []
    
    colorcycle = 0
    
    max_y = 0
    
    for plot_line in plot_data:
        if plot_line['time'] == 0:
            if x_axis:
                x_axis.append(x_axis_size)
                y_axis.append(y_axis[-1])
                
                plt.plot(x_axis, y_axis, colors[colorcycle], linestyle='steps')
                colorcycle += 1
                if colorcycle == len(colors):
                    colorcycle = 0
            x_axis = []
            y_axis = []
        x_axis.append(plot_line['time'])
        y_axis.append(plot_line['score'])
        
        if plot_line['score'] > max_y:
            max_y = plot_line['score']
    
    plt.plot(x_axis, y_axis, colors[colorcycle], linestyle='steps')
    
    plt.plot(0, max_y + 1)
    
    plt.xlabel('Time')
    plt.ylabel('Score')
    
    plt.savefig(plot_save_name)
    plt.clf()

if __name__ == '__main__':
    main(sys.argv)
    