#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 15:13:16 2021

@author: arno
"""
import mne
from scipy.signal import butter, filtfilt


def bandpass(data, f1, f2, fs, order=5, axis=-1):
    nyq = 0.5 * fs
    b, a = butter(order, (f1/nyq, f2/nyq), 'bandpass')
    return filtfilt(b, a, data, axis=axis)

def perform_ica(raw):
    method = 'fastica'

    n_components = 18 # if float, select n_components by explained variance of PCA
    
    # we will also set state of the random number generator - ICA is a
    # non-deterministic algorithm, but we want to have the same decomposition
    # and the same order of components each time this tutorial is run
    random_state = 1
    
    ica = mne.preprocessing.ICA(n_components=n_components, method=method, random_state=random_state)
    ica.fit(raw)
    ica.plot_components(inst=raw)
    ica.plot_sources(inst=raw)
    # eog_component = iex.getBadICAs(patient_number)
    # ica.exclude = eog_component
    # epochs_corrected = epochs.copy()
    # ica.apply(epochs_corrected)