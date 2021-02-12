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

data_path = "//home/arno/Workspace/eeg_painvision/Data Brutes - EEG Arno/20210204163706_arn0-c2-2"

raw_edf = io.read_raw_edf(data_path + ".edf", preload=True)
raw_easy = pd.read_csv(data_path + ".easy", sep='\t', names=raw_edf.ch_names)
data = raw_easy.values.T

fs = 500
raw_edf.filter(l_freq=1, h_freq=40, n_jobs=1, fir_design='firwin')
events_raw = bandpass(raw_edf["C4"][0][0], f1=20, f2=40, fs=fs)
events = sg.find_peaks(events_raw, height=140000, distance=fs*0.8)
plt.scatter(events[0], events[1]['peak_heights'], color='red')
plt.plot(events_raw)

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