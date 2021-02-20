# -*- coding: utf-8 -*-

import pywt
import numpy as np
import matplotlib.pyplot as plt


def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


fs = 1024
window = 4*fs
dt = 1/fs
(f0, f1, f2) = fs/16, fs/64, fs/4
x = np.arange(window)
y0 = np.sin(2*np.pi*x/f0) * gaussian(x, 800, 80)
y1 = np.sin(2*np.pi*x/f1) * gaussian(x, 200, 30)
y2 = np.sin(2*np.pi*x/f2)
y = y0 + y1 + y2

scales = np.arange(1,65)
frequencies = pywt.scale2frequency('mexh', scales)/dt

coef, freqs=pywt.cwt(y,np.arange(1,fs/8),'mexh')

plt.close('all')
fig, axs = plt.subplots(5, gridspec_kw={'height_ratios': [1,1,1,1,3]})
axs[0].plot(y0)
axs[1].plot(y1)
axs[2].plot(y2)
axs[3].plot(y)
axs[4].matshow(np.flipud(coef), extent=[0, fs, 1, 64], cmap='PRGn', aspect='auto',
            vmax=abs(coef).max(), vmin=-abs(coef).max(), )
plt.yticks(np.arange(len(frequencies))[::4], np.around(frequencies[::4], 1))
plt.ylabel("f (Hz)")
axs[4].xaxis.tick_bottom()
#fig.tight_layout()
#%%
import scaleogram as scg
fs = 1024
window = 2*fs
(f0, f1, f2) = fs/16, fs/64, fs/4
p1, p2 = 1/f1, 1/f2
x = np.arange(window)
y0 = np.sin(2*np.pi*x/f0) * gaussian(x, 800, 80)
y1 = np.sin(2*np.pi*x/f1) * gaussian(x, 200, 30)
y2 = np.sin(2*np.pi*x/f2)
y = y0 + y1 + y2
x = np.arange(window)
wavelet='cmor0.5-1'

plt.close('all')
fig, axs = plt.subplots(2, gridspec_kw={'height_ratios': [1,3]})
axs[0].plot(y)
scg.cws(x, y, scales=np.arange(1,150), wavelet=wavelet, ax=axs[1])
fig.tight_layout()
txt = ax2.annotate("p1=%ds" % p1, xy=(n/2,p1), xytext=(n/2-10, p1), bbox=dict(boxstyle="round4", fc="w"))
txt = ax2.annotate("p2=%ds" % p2, xy=(n/2,p2), xytext=(n/2-10, p2), bbox=dict(boxstyle="round4", fc="w"))
#%%
from scipy import signal
plt.close('all')

fs = 1024
f0 = fs/16
f1 = fs/64
signal_len = 2 * fs # Let's imagine a 2s signal

widths = np.arange(1, 64)
x = np.arange(signal_len)
y0 = np.sin(2*np.pi*x/f0)
y1 = np.sin(2*np.pi*x/f1) 
y = y0 * gaussian(x, 800, 80) + y1 * gaussian(x, 200, 30)
cwtmatr = signal.cwt(y, signal.ricker, widths)

fis, axs = plt.subplots(2)

axs[0].plot(y)
axs[1].imshow(cwtmatr, extent=[0, signal_len, 1, widths.max()], cmap='PRGn', aspect='auto',
            vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())