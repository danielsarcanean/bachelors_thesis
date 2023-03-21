import scipy.stats as sp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy import stats

### FUNCTION FOR GRAPHICAL IMPLEMENTATION ###

def plot_graph(file, color):
  
  x1 = []
  x2 = []
  x3 = []

  y1 = []
  y2 = []
  y3 = []
  with open('20230307/01.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter = ';')
    
    count = 0
    
    for row in plots:
        if count < 3:
            count += 1
            continue
        x1.append(float(row[0]))
        y1.append(float(row[1]))
with open('20230307/01.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter = ';')
    
    count = 0
    
    for row in plots:
        if count < 3:
            count += 1
            continue
        x1.append(float(row[0]))
        y1.append(float(row[1]))
        
with open('20230307/02.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter = ';')
    
    count = 0
    
    for row in plots:
        if count < 3:
            count += 1
            continue
        x2.append(float(row[0]))
        y2.append(float(row[1]))
        
with open('20230307/03.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter = ';')
    
    count = 0
    
    for row in plots:
        if count < 3:
            count += 1
            continue
        x3.append(float(row[0]))
        y3.append(float(row[1]))

data0 = np.array([y1[60], y2[60], y3[60]])
error0 = data0.std()
data0 = -data0.mean()


        
dataw = np.array([y1[60], y2[60], y3[60]])
errorw = dataw.std()
dataw = -dataw.mean()

### DATA TREATMENT ###

stacked_data = [dataw, data0, data1, data2, data3, data4, data5, data6, data7, data8, data9]
stacked_error = [errorw, error0, error1, error2, error3, error4, error5, error6, error7, error8, error9]
concentrations = [0, 5, 2.5, 1.25, 0.625, 0.3125, 0.15625, 0.07813, 0.03906, 0.01953, 0.0097]


slope, intercept, r, p, std_err = stats.linregress(concentrations, stacked_data)

def myfunc(x):
  return slope * x + intercept

res = list(map(myfunc, concentrations))

### PLOT FORMATTING ###

fig, ax = plt.subplots()

plt.rcParams["figure.figsize"] = (5,5)
plt.rcParams["figure.dpi"] = 300

xvalues = np.linspace(-5,6,50)



txt = f"2023/03/07: Chronoamperometric linear fit of the data sets\nwith a curve of y = {slope:.3f}x + {intercept:.3f} and a R-squared factor\nof {r:.3f}, taking the values at 30 s of duration."
plt.figtext(0, 0.925, txt, wrap=True, horizontalalignment='left', fontsize=11)
plt.text(1.25, stacked_data[0]*3-(stacked_data[0]*3 + 0.5)/2, f"Limit of detection (LOD) at {stacked_data[0]*3:.3f} $\mu$A", fontsize=7, horizontalalignment='center', verticalalignment='center')

plt.errorbar(concentrations, stacked_data, yerr=stacked_error, linestyle='', marker='D', color='red', markersize=3, capsize=1, barsabove=True, ecolor='black')
plt.fill_between(xvalues, -1, stacked_data[0]*3, alpha=0.5, color='orange')
plt.plot(concentrations, res, linestyle=':', color='black')
plt.ylabel('Current ($\mu A$)')
plt.xlim(-0.5,5.5)
plt.ylim(bottom=-0.5)
plt.xlabel("Ferri's concentration (mM)")

plt.savefig('20230307/calibration_curve_chrono.png')
plt.show()
