import mne
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from  utils.signal_processing import bandpass

from mne import io
from mne.datasets import sample
from mne.cov import compute_covariance

data_path = "//home/arno/Workspace/eeg_painvision/Data Brutes - EEG Arno/20210204163706_arn0-c2-2"

raw_edf = io.read_raw_edf(data_path + ".edf")#, stim_channel='C4')
raw_easy = pd.read_csv(data_path + ".easy", sep='\t', names=raw_edf.ch_names)
data = raw_easy.values.T

sfreq = 500

filtered_data = bandpass(data=data, f1=1, f2=40, fs=sfreq, axis=1)


for i, row in enumerate(filtered_data):
    if i == 8:
        plt.plot(row, alpha=0.7, label=i)
        continue
plt.show()

# ch_names = raw_edf.ch_names
# ch_types = ['eeg'] * len(ch_names)
# info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)

# raw_mne = io.RawArray(raw_easy.values.T, info)

# raw_edf.plot(scalings="auto")