import mne
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as sg
import os
from  utils.signal_processing import bandpass

from mne import io
from mne.datasets import sample
from mne.cov import compute_covariance

# Get data
data_path = "//home/arno/Workspace/eeg_painvision/Data Brutes - EEG Arno/20210204163706_arn0-c2-2"

raw_edf = io.read_raw_edf(data_path + ".edf", preload=True)
raw_easy = pd.read_csv(data_path + ".easy", sep='\t', names=raw_edf.ch_names)
data = raw_easy.values.T

# Filter data
fs = 500
raw_edf.filter(l_freq=1, h_freq=40, n_jobs=1)
events_raw = bandpass(raw_edf["C4"][0][0], f1=20, f2=40, fs=fs)

# Get events
events_peaks = sg.find_peaks(events_raw, height=130000, distance=fs*0.8)
# plt.scatter(events_peaks[0], events_peaks[1]['peak_heights'], color='red')
# plt.plot(events_raw)

# This page provides great info : https://mne.tools/stable/auto_tutorials/intro/plot_20_events_from_raw.html#sphx-glr-auto-tutorials-intro-plot-20-events-from-raw-py
events = np.zeros((events_peaks[0].shape[0], 3), dtype=np.int32())
events[:, 0] = events_peaks[0]
events[:, 2] = 1

event_id, tmin, tmax = 1, -0.1, 0.7
epochs = mne.Epochs(raw_edf, events, event_id, tmin, tmax, picks=('eeg'),
                     baseline=None, reject=None, preload=True)

# filtered_data = bandpass(data=data, f1=1, f2=40, fs=fs, axis=1)


# for i, ch in enumerate(raw_edf.ch_names):
#     if 5 < i < 11:
#         print(ch)
#         plt.plot(raw_edf[ch][0][0])
#         continue
# plt.show()

# ch_names = raw_edf.ch_names
# ch_types = ['eeg'] * len(ch_names)
# info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)

# raw_mne = io.RawArray(raw_easy.values.T, info)

# raw_edf.plot(scalings="auto")