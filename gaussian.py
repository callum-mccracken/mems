"""module for fitting / plotting 2D Gaussian"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt

def twoD_Gaussian(points, amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
    x, y = list(zip(*points))
    a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2)
    b = -(np.sin(2*theta))/(4*sigma_x**2) + (np.sin(2*theta))/(4*sigma_y**2)
    c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2)
    g = offset + amplitude*np.exp( - (a*((x-xo)**2) + 2*b*(x-xo)*(y-yo) + c*((y-yo)**2)))
    return g

def plot_gaussian(x, y, data, name):
    # plot twoD_Gaussian data generated above

    x_flat = x.flatten()
    y_flat = y.flatten()
    data_flat = data.flatten()

    xy_points = list(zip(x_flat, y_flat))

    initial_guess = (0.5, np.mean(x),np.mean(y),np.std(x),np.std(y),0,0)

    popt, _ = opt.curve_fit(twoD_Gaussian, xy_points, data_flat, p0=initial_guess)

    amplitude, xo, yo, sigma_x, sigma_y, theta, offset = popt

    data_fitted = twoD_Gaussian(xy_points, amplitude, xo, yo, sigma_x, sigma_y, theta, offset)

    data_fitted = np.array(data_fitted).reshape(x.shape)

    plt.contourf(x, y, data_fitted)

    plt.title(name)
    fname = "gaussian_" + name.lower().replace(" ", "_") + ".png"
    plt.savefig(fname)
    return amplitude, xo, yo, sigma_x, sigma_y, theta, offset