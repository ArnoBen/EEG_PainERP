# -*- coding: utf-8 -*-
"""
Created on --unknown--
@author: mathieu

Contains the classes:
    --------------

Contains the exceptions:
    --------------

Contains the functions:
    create_mne_info(layout, sfreq=500, aux=True, montage='standard_1020')
    --------------
"""

import mne

def create_mne_info(layout, sfreq=500, aux=True, montage='standard_1020'):
    """
    Create an mne.Info instance:
        - Trigger
        - 64 EEG electrodes
        - (optional) ECG on AUX1
        - (optional) EOG on AUX2
    
    Without adding montage:
        %timeit
        885 µs ± 2.69 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
    With montage:
        %timeit
        4.62 ms ± 11.8 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

    Parameters
    ----------
    layout : list of str
        List of the channels names present in the layout.
    sfreq: int, optional
        System sampling frequency.
        The default is 500.
    aux: boolean, optional
        Set to True to include ECG channel on AUX1 and EOG channel on AUX2.
        The default is True.
    montage: str or None, optional
        MNE montage defining the layout electrode positions.
        If None, the montage is not added to the info.

    Returns
    -------
    info : mne.Info
        https://mne.tools/stable/generated/mne.Info.html?highlight=info#mne.Info
    """
    ch_names = ['TRIGGER'] + layout
    ch_types = ['stim'] + ['eeg'] * len(layout)
    
    if aux:
        ch_names += ['ECG', 'EOG']
        ch_types += ['ecg', 'eog']
    
    info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
    
    if montage is not None:
        info.set_montage(montage)
    
    return info

if __name__ == '__main__':
    layout = ['Fp1', 'Fz', 'F3', 'F7', 'FT9', 'FC5', 'FC1', 'C3', 
              'T7', 'TP9', 'CP5', 'CP1', 'Pz', 'P3', 'P7', 'O1', 
              'Oz', 'O2', 'P4', 'P8', 'TP10', 'CP6', 'CP2', 'Cz', 
              'C4', 'T8', 'FT10', 'FC6', 'FC2', 'F4', 'F8', 'Fp2', 
              'AF7', 'AF3', 'AFz', 'F1', 'F5', 'FT7', 'FC3', 'C1', 
              'C5', 'TP7', 'CP3', 'P1', 'P5', 'PO7', 'PO3', 'POz',
              'PO4', 'PO8', 'P6', 'P2', 'CPz', 'CP4', 'TP8', 'C6', 
              'C2', 'FC4', 'FT8', 'F6', 'AF8', 'AF4', 'F2', 'FCz']
    
    info = create_mne_info(layout=layout)