import matplotlib.pyplot as plt
import numpy as np

# Load and plot lp.txt data
graph_lp = np.loadtxt('lp.txt')
plt.figure(1)
plt.plot(graph_lp[:, 0], graph_lp[:, 1], '.')
plt.grid(True)
plt.xlabel('a(2)')
plt.ylabel('a(3)')
plt.title('LP')

# Load and plot lpcc.txt data
graph_lpcc = np.loadtxt('lpcc.txt')
plt.figure(2)
plt.plot(graph_lpcc[:, 0], graph_lpcc[:, 1], '.')
plt.grid(True)
plt.xlabel('a(2)')
plt.ylabel('a(3)')
plt.title('LPCC')

# Load and plot mfcc.txt data
graph_mfcc = np.loadtxt('mfcc.txt')
plt.figure(3)
plt.plot(graph_mfcc[:, 0], graph_mfcc[:, 1], '.')
plt.grid(True)
plt.xlabel('a(2)')
plt.ylabel('a(3)')
plt.title('MFCC')

plt.show()
