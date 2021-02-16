# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils.signal_processing import bandpass
from scipy import signal as sg

def get_events(events_peaks):
    # This page provides great info : https://mne.tools/stable/auto_tutorials/intro/plot_20_events_from_raw.html#sphx-glr-auto-tutorials-intro-plot-20-events-from-raw-py
    events = np.zeros((events_peaks[0].shape[0], 3), dtype=np.int32())
    events[:, 0] = events_peaks[0]
    events[:, 2] = 1
    return events
    
def preprocess_event_channel(raw, trigger_ch, plot=False, apply_filter=False):
    fs = raw.info['sfreq']
    events_channel = raw[trigger_ch][0][0]
    if apply_filter:
        events_channel = bandpass(events_channel, f1=1, f2=40, fs=fs)
    height = np.std(events_channel) * 4
    events_peaks = sg.find_peaks(events_channel, height=height, distance=fs*0.8)
    if plot:
        plt.scatter(events_peaks[0], events_peaks[1]['peak_heights'], color='red')
        plt.plot(events_channel)
        csv_triggers = get_false_triggers_from_csv("DonneesImpulsionsAleatoires.csv")
        plt.vlines(csv_triggers["ImpulsionTime"] * 500 + 342, 0, 2000000, color="gray")
        plt.show()
        
    return events_peaks

def get_false_triggers_from_csv(file):
    random_impulses_info = pd.read_csv(file, sep=";", index_col=False)
    impulsions_times = np.zeros(random_impulses_info.shape[0])
    impulsions_times[1:] = np.cumsum([random_impulses_info["ImpulsionInterval"]])[:-1]
    random_impulses_info["ImpulsionTime"] = impulsions_times
    return random_impulses_info[["ImpulsionTime", "PainInflicted"]]
    