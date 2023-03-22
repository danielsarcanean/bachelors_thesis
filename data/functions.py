import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt
import os
import re
from scipy import stats
import textwrap

def read_data(file_name):
    x = []
    y = []
    with open(file_name, 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=';')
        count = 0
        for row in plots:
            if count < 3:
                count += 1
                continue
            x.append(float(row[0]))
            y.append(float(row[1]))
    return x, y

def process_files(folder, size):
    # Creates the containers for each data set
    # Don't forget to change the concentrations array for the one you will be analyzing!
    data = []
    errors = []
    concentrations = np.array([5, 2.5, 1.25, 0.625, 0.3125, 0.15625, 0.07813, 0.03906, 0.01953, 0.0097, 0])

    for i in range(size+1):
        # Get a list of all files in the directory that start with {i} and are followed by a non-digit character
        files = [f for f in os.listdir(folder) if re.match(f'^{i}\\D', f)]

        # Generate x and y values for each file
        y_values = []
        for file in files:
            x, y = read_data(os.path.join(folder, file))
            y_values.append(y[60])

        # Calculate the mean and standard deviation of the data
        data_i = np.array(y_values)
        error_i = data_i.std()
        data_i = -data_i.mean()
        data.append(data_i)
        errors.append(error_i)
        print(data_i)
    
    slope, intercept, r, p, std_err = stats.linregress(concentrations, data)

    def myfunc(x):
        return slope * x + intercept

    res = list(map(myfunc, concentrations))
    
    # Plot the data

    plt.rcParams["figure.figsize"] = (6,5)
    plt.rcParams["figure.dpi"] = 300
    
    txt = input("Insert the text you want for the figure: ")
    txt += f" The given linear fit has the form of y = {slope:.3f}x + {intercept:.3f} with a R-squared factor of {r:.3f}. Limit of detection (LOD) at {data[size]+3*errors[size]:.3f} $\mu$A."
    fig, ax = plt.subplots(figsize=(6,5))
    
    xval = np.linspace(concentrations[-1]-0.1, concentrations[0]+0.1, 5)
    plt.ylim(data[-1]-20*data[-1], data[0]+0.2)
    plt.xlim(concentrations[-1]-0.1, concentrations[0]+0.1)
    
    # Plot the LOD as a shade that forbids certain data values
    plt.fill_between(xval, data[-1]-20*data[-1], data[size]+3*errors[size], alpha=0.5, color='orange')

    plt.errorbar(concentrations, data, yerr=errors, fmt='D', capsize=5, color='black', markersize=4)
    plt.plot(concentrations, res, linestyle=':', color='red')
    plt.ylabel('Current ($\mu$A)')
    plt.xlabel("Ferrihexacyanate concentration (mM)")
    
    wrapped_txt = textwrap.wrap(txt, width=65)  # Wrap text to 50 characters
    x_pos = -0.1  # Adjust x position of text
    y_pos = 1.20  # Adjust y position of text
    for line in wrapped_txt:
        ax.text(x_pos, y_pos, line, ha='left', va='center', transform=ax.transAxes, fontsize=11)
        y_pos -= 0.05  # Decrease y position for each line

    # Show plot
    plt.show()

filename = input("Insert the location of your files: ")
size_of_files = input("Insert the size of the samples: ")

process_files(filename, size_of_files)

