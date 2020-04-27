"""A module for analyzing the test run of the mems setup"""

import numpy as np
import matplotlib.pyplot as plt
import os

import gaussian

files = [
    "memsscan20march_bottomleft_7.dat",
    "memsscan20march_bottomright_6.dat",
    "memsscan20march_centre_5.dat",
    "memsscan20march_topleft_3.dat",
    "memsscan20march_topright.dat",
    ]

names = {
    "memsscan20march_bottomleft_7.dat": "Bottom Left",
    "memsscan20march_bottomright_6.dat": "Bottom Right",
    "memsscan20march_centre_5.dat": "Centre",
    "memsscan20march_topleft_3.dat": "Top Left",
    "memsscan20march_topright.dat": "Top Right"
}

centroid_file = "centroid.txt"
gaussian_file = "gaussian.txt"
open(centroid_file, "w").close()  # clear it
open(gaussian_file, "w").close()

for filename in files:
    print(filename)

    # get the lines of the file
    with open(filename, "r") as f:
        lines = f.readlines()

    # cut off the junk at the start
    lines = lines[6:]

    # number of data points in the file
    n_lines = len(lines)

    # get x, y, v data as floats
    xs = np.empty(n_lines)
    ys = np.empty(n_lines)
    vs = np.empty(n_lines)
    for i, line in enumerate(lines):
        x, y, v = map(float, line.split())
        xs[i] = x
        ys[i] = y
        vs[i] = v

    # reshape for plotting
    x_vals = np.unique(xs)
    y_vals = np.unique(ys)
    xg, yg = np.meshgrid(x_vals, y_vals)
    vg = vs.reshape(xg.shape)

    # make contour plot
    plt.cla(); plt.clf()
    plt.xlabel("dx")
    plt.ylabel("dy")
    plt.contourf(xg, yg, vg)
    fname = filename.replace("memsscan", "contour_no_filter")[:-4] + ".png"
    plt.savefig(fname)

    # filter out some noise
    vg[vg < 0.3] = 0

    # find the centroid the simple way
    centroid_x = sum(xs * vs) / sum(vs)
    centroid_y = sum(ys * vs) / sum(vs)

    with open(centroid_file, "a") as cfile:
        cfile.write(f"Centroid for {filename}: {centroid_x}, {centroid_y}\n")

    # fit a Gaussian to get better parameters
    amplitude, xo, yo, sigma_x, sigma_y, theta, offset = gaussian.plot_gaussian(xg, yg, vg, names[filename])

    with open(gaussian_file, "a") as gfile:
        gfile.write(f"Gaussian parameters for {filename}:\n")
        gfile.write(f"\tCentroid: ({xo},{yo})\n")
        gfile.write(f"\tAmplitude: {amplitude}\n")
        gfile.write(f"\tWidths: ({sigma_x},{sigma_y})\n")

    # make contour plot
    plt.cla(); plt.clf()
    fig, ax = plt.subplots()
    plt.xlabel("dx")
    plt.ylabel("dy")
    plt.title("Voltage (filtered) at Scanned Points of "+names[filename]+" Port")
    cs = plt.contourf(xg, yg, vg)
    cbar = fig.colorbar(cs, shrink=0.9)
    cbar.ax.set_ylabel('Voltage')
    plt.plot(centroid_x, centroid_y, marker="+", markersize=40)
    fname = filename.replace("memsscan", "contour_filter")[:-4] + ".png"
    plt.tight_layout()
    plt.savefig(fname)
