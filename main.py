import mne
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.signal as sg
import os
from utils.signal_processing import bandpass
from utils import event_parser

from mne import io
from mne.datasets import sample
from mne.cov import compute_covariance

plt.close()

# Get data
data_path = "/home/arno/Workspace/eeg_painvision/Data Brutes - EEG Arno/20210204163706_arn0-c2-2"

raw_edf = io.read_raw_edf(data_path + ".edf", preload=True)
# raw_easy = pd.read_csv(data_path + ".easy", sep='\t', names=raw_edf.ch_names)
# data = raw_easy.values.T
unused_channels = ['X', 'Y', 'Z', 'EXT']
raw_edf.drop_channels(unused_channels)
raw_edf.set_montage('standard_1020')

#%% Fetching events
preprocessed_event_channel = event_parser.preprocess_event_channel(raw_edf, trigger_ch="C4", plot=True)
events = event_parser.get_events(preprocessed_event_channel)

#%% Preprocessing

# Filter data
fs = raw_edf.info['sfreq'] # =500
raw_edf.filter(l_freq=1, h_freq=40, n_jobs=1)
# Drop event channel (here it's C4)
raw_edf.drop_channels(('C4'))
#%% ICA
method = 'fastica'

n_components = 18 # if float, select n_components by explained variance of PCA
decim = 3  # we need sufficient statistics, not all time points -> saves time

# we will also set state of the random number generator - ICA is a
# non-deterministic algorithm, but we want to have the same decomposition
# and the same order of components each time this tutorial is run
random_state = 1

ica = mne.preprocessing.ICA(n_components=n_components, method=method, random_state=random_state)
ica.fit(raw_edf)
ica.plot_components(inst=raw_edf)
ica.plot_sources(inst=raw_edf)
ica.apply(raw_edf)

#%%
event_id, tmin, tmax = 1, -0.1, 0.7
epochs = mne.Epochs(raw_edf, events, event_id, tmin, tmax, picks=('eeg'),
                     baseline=None, reject=None, preload=True)
evoked = epochs.average()
evoked.plot(time_unit='s', spatial_colors=True, gfp=True)
# filtered_data = bandpass(data=data, f1=1, f2=40, fs=fs, axis=1)


#%%
for i, ch in enumerate(raw_edf.ch_names):
    if i == 10:
        print(ch)
        plt.plot(raw_edf[ch][0][0])
        continue
plt.show()

# ch_names = raw_edf.ch_names
# ch_types = ['eeg'] * len(ch_names)
# info = mne.create_info(ch_names=ch_names, sfreq=fs, ch_types=ch_types)

#raw_edf.plot(scalings="auto", alpha=0.7)