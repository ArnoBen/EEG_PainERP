# -*- coding: utf-8 -*-
import matplotlib
import datetime


def set_xticks_time(ax):
    def timeTicks(x, pos):
        d = datetime.timedelta(seconds=x)
        return str(d)
    formatter = matplotlib.ticker.FuncFormatter(timeTicks)
    ax.xaxis.set_major_formatter(formatter)