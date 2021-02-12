#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 15:13:16 2021

@author: arno
"""

from scipy.signal import butter, filtfilt


def bandpass(data, f1, f2, fs, order=5, axis=-1):
    nyq = 0.5 * fs
    b, a = butter(order, (f1/nyq, f2/nyq), 'bandpass')
    return filtfilt(b, a, data, axis=axis)