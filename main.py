import mne
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as sg
import os
import pywt
from utils.signal_processing import bandpass
from utils import event_parser

from mne import io
from mne.datasets import sample
from mne.cov import compute_covariance

plt.close()

# Get data
data_path = "/home/arno/Workspace/eeg_painvision/Data Brutes - EEG Arno/20210204171318_arn0-c6-2"

raw_edf = io.read_raw_edf(data_path + ".edf", preload=True)
removed_channels = ['X', 'Y', 'Z', 'EXT'] #+  ['C4']
raw_edf.set_eeg_reference("average")
raw_edf.drop_channels(removed_channels)
raw_edf.set_montage('standard_1020')
channels = raw_edf.ch_names
raw_edf.plot(scalings="auto")
raw_edf.info['bads'] = ["Pz"]

#%% Fetching events
preprocessed_event_channel = event_parser.preprocess_event_channel(
    raw_edf, trigger_ch="C4", apply_filter=False, plot=True, include_csv=False)
events = event_parser.get_events(preprocessed_event_channel)

#%% Preprocessing
# Drop event channel (here it's C4)
#raw_edf.drop_channels(('C4'))
# Filter data
plt.close("all")
fs = int(raw_edf.info['sfreq']) # =500
nyq = int(fs/2)
data = raw_edf.get_data()[7]
raw_filtered = raw_edf.filter(l_freq=1, h_freq=40, n_jobs=1)

# CWT
# t = np.linspace(0, len(data), 20, endpoint=False)

# widths = np.linspace(1, len(data), 20)
# cwtmatr, freqs = pywt.cwt(raw_edf.get_data()[0], widths, 'mexh')
# plt.imshow(cwtmatr, extent=[0, len(data), 0, freqs.max()], cmap='PRGn', aspect='auto',
#             vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())  # doctest: +SKIP
# plt.show()

# Spectrogram

window = fs
fig, ax = plt.subplots()
Pxx, freqs, bins, im = ax.specgram(data, NFFT=window, Fs=fs, noverlap=window/2, cmap="viridis", vmin=30, vmax=70)
ax.set_title('Spectrogram of O2 channel')
ax.set_ylim((0,45))
ax.set_xlabel('time (h:mm:ss)')
ax.set_ylabel('frequency (Hz)')
fig.colorbar(im).set_label('Amplitude (dB)')

# Reduction de la taille des données : récupérer uniquements les points < 60Hz
# Le tableau est de la taille 251 lignes x n colonnes (varie selon le temps et la taille des fenêtres)
# 250Hz (SamplingRate/2) --> 251 lignes, donc 60Hz --> 60 lignes.
# im = im._A[:-60]
# plt.imshow(im,vmin=0,vmax=300, aspect='auto', interpolation='none', cmap='viridis', extent = (0,85000,0,60))
#%% Getting epochs based on events
event_id, tmin, tmax = 1, -0.1, 0.7
epochs = mne.Epochs(raw_filtered, events, event_id, tmin, tmax, picks=('eeg'),
                     baseline=None, reject=None, preload=True)

evoked = epochs.average()
evoked.plot(time_unit='s', spatial_colors=True, gfp=True)
# filtered_data = bandpass(data=data, f1=1, f2=40, fs=fs, axis=1)


#%% Looking at all epochs on a single channel
""" 
J'ai compté à la main les events correctement détectés par le find_peaks
25% : 41
50% : 46
75% : 39 
"""
for i, ch in enumerate(channels):
    if ch == 'C4':
        continue
    single_channel_epochs = epochs.copy().pick(channels[i])
    single_channel_epochs.get_data()
    # for epoch in single_channel_epochs[41:87]:
    #     plt.plot(epoch.T, alpha=.5)
    channel_mean = np.mean(single_channel_epochs[41:87].get_data(), axis=0)[0]
    channel_std = np.std(single_channel_epochs[41:87].get_data(), axis=0)[0]
    plt.plot(channel_mean, label=ch)
    plt.fill_between(range(channel_std.shape[0]),
                      channel_mean-channel_std,
                      channel_mean+channel_std,
                      alpha=.04)
plt.vlines(50,-1.9e5,3e4,color="black")
plt.legend(loc="upper right")
plt.show()
#%%
# for i, ch in enumerate(raw_edf.ch_names):
#     if i == 10:
#         print(ch)
#         plt.plot(raw_edf[ch][0][0])
#         continue
# plt.show()

# ch_names = raw_edf.ch_names
# ch_types = ['eeg'] * len(ch_names)
# info = mne.create_info(ch_names=ch_names, sfreq=fs, ch_types=ch_types)

#raw_edf.plot(scalings="auto", alpha=0.7)

#%% Using the .easy

raw_easy = pd.read_csv(data_path + ".easy", sep='\t', names=raw_edf.ch_names)
data = raw_easy.values.T

filtered_data = bandpass(data=data, f1=1, f2=40, fs=fs, axis=1)

# for i, row in enumerate(filtered_data):
#     plt.plot(row, alpha=0.7, label=i)
ch_names = raw_edf.ch_names

ch_types = ['eeg'] * len(ch_names)
info = mne.create_info(ch_names=ch_names, sfreq=fs, ch_types=ch_types)

raw_mne = io.RawArray(raw_easy.values.T, info)

raw_edf.plot(scalings="auto") 