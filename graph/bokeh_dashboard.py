#!/usr/bin/env python3

#%%
import pandas as pd
import numpy as np
from bokeh.palettes import brewer
from bokeh.plotting import figure, output_file, show

x = [2,4,6,8,10]
y = [1,3,5,7,9]

output_file('graph.html')

p = figure(
    title = 'Simple Graph',
    x_axis_label = 'X Axis',
    y_axis_label = 'Y Axis'
)

p.line(x, y, legend_label='line', line_width=2)
show(p)
