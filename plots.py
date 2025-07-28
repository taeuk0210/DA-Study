import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib as mpl
mpl.rcParams['font.family'] = 'Malgun Gothic'
mpl.rcParams['axes.unicode_minus'] = False

from typing import Tuple, Dict

#################
# Global config #
#################

plt.style.use("ggplot")
sns.set_palette("Set3")

#############
# Draw plot #
#############

def barplot(
        df:pd.DataFrame,
        x:str,
        y:str,
        hue:str,
        title:str = None,
        xlabel:str = None,
        ylabel:str = None,
        figsize:Tuple[int] = (10, 6),
        tight_layout:bool = False
    ):
    fig, axe, fs = _get_baseplot(figsize=figsize)

    sns.barplot(data=df, x=x, y=y, hue=hue, ax=axe)

    for i, value in enumerate(df[y]):
        axe.text(i, value + 2, f"{value}", ha="center", va="bottom", fontsize=fs['label'])

    axe = _set_label_layout(axe, fs, title, xlabel, ylabel, tight_layout)

    return fig, axe

#############
# Utiliteis #
#############

def _get_fontsize(figsize, base_area=40):
    w, h = figsize
    area = w * h
    scale = area / base_area

    return {
        "title": round(15 * scale, 1),
        "label": round(11 * scale, 1),
        "tick": round(9 * scale, 1)
    }

def _get_baseplot(
        figsize:Tuple[int] = (10, 6)
    ):
    fig, axe = plt.subplots(figsize=figsize)

    fs = _get_fontsize(figsize)

    axe.set_facecolor("#F0F0F0")

    return fig, axe, fs

def _set_label_layout(
        axe,
        fs:Dict[str, int],
        title:str = None,
        xlabel:str = None,
        ylabel:str = None,
        tight_layout:bool = False
    ):
    axe.set_title(title, fontsize=fs['title'], fontweight="bold")
    axe.set_xlabel(xlabel, fontsize=fs['label'], color='#000000')
    axe.set_ylabel(ylabel, fontsize=fs['label'], color='#000000')

    axe.tick_params(axis='x', labelsize=fs['tick'], color='#000000')
    axe.tick_params(axis='y', labelsize=fs['tick'], color='#000000') 

    axe.set_in_layout(tight_layout)
    return axe