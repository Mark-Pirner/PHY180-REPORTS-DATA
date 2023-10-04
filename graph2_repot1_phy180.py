import scipy.optimize as optimize
import numpy as np
import matplotlib.pyplot as plt
from pylab import loadtxt
import math

def load_data(filename):
    data = loadtxt(filename, usecols=(0, 1, 2, 3), skiprows=1, unpack=True)
    return data

def plot_fit(my_func, xdata, ydata, xerror=None, yerror=None, init_guess=None,
             font_size=14, xlabel="Independent Variable (units)", ylabel="Dependent Variable (units)"):
    plt.rcParams.update({'font.size': font_size})
    plt.rcParams['figure.figsize'] = 10, 9

    popt, pcov = optimize.curve_fit(my_func, xdata, ydata, sigma=yerror, p0=init_guess)
    puncert = np.sqrt(np.diagonal(pcov))

    print("Best fit parameters, with uncertainties:")
    for i in range(len(popt)):
        print(f"Parameter {i + 1}: {popt[i]} +/- {puncert[i]}")

    start = min(xdata)
    stop = max(xdata)
    xs = np.arange(start, stop, (stop - start) / 1000)
    curve = my_func(xs, *popt)

    fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [4, 1]})

    ax1.errorbar(xdata, ydata, yerr=yerror, xerr=xerror, fmt=".", label="data", color="black", lw=1)
    ax1.plot(xs, curve, label="best fit", color="black")
    ax1.legend(loc='upper right')
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)

    residual = ydata - my_func(xdata, *popt)
    ax2.errorbar(xdata, residual, yerr=yerror, xerr=xerror, fmt=".", color="black", lw=1)
    ax2.axhline(y=0, color="black")
    ax2.set_xlabel(xlabel)
    ax2.set_ylabel("Residuals")

    fig.tight_layout()
    plt.show()
    fig.savefig("graph.png")

    return None

def cosine(t, a, b, c):
    return a * np.exp(-t / b) * np.cos(2 * math.pi * t / c)

filename = r"C:\Users\markp\OneDrive\Desktop\phy180\physlab2TvsTHETA.txt"
x, y, xerr, yerr = load_data(filename)


init_guess = (-0.50397, 106.1333, 1.58) #calculated and extrapolated values

font_size = 12
xlabel = "Time [s]"
ylabel = "Theta [rad]"

plot_fit(cosine, x, y, xerr, yerr, init_guess=init_guess, font_size=font_size,
         xlabel=xlabel, ylabel=ylabel)