import os
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

GROWTH_FILE = "growth.npy"

def calculate_growth_from_surface_area(file):
    surface_area_arr = []
    with open(file, 'r') as f:
        for line in sorted(f.readlines()):
            surface_area = int(line.split(' ')[1])
            if surface_area:
                surface_area_arr.append(surface_area)
    # plot_surface_area(surface_area_arr)
    Y = np.array(surface_area_arr)
    plot_surface_area(Y)
    X = np.arange(len(surface_area_arr)).reshape(-1, 1)
    model = LinearRegression().fit(X, Y)
    params = model.coef_
    np.save(GROWTH_FILE, params)

def plot_surface_area(arr):
    plt.plot(arr)
    plt.ylabel('Surface area')
    plt.yticks([])
    plt.xlabel('Time')
    plt.savefig("growth_curve.png")
    plt.clf()

if __name__ == "__main__":
    calculate_growth_from_surface_area("surface_area_results.txt")