import numpy as np
import pandas as pd

from typing import Tuple, Dict

import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Set Global configuration

mpl.rcParams['font.family'] = 'Malgun Gothic'
mpl.rcParams['axes.unicode_minus'] = False

plt.style.use("ggplot")
sns.set_palette("Set3")



#############
# Draw plot #
#############

def lineplot(
        df:pd.DataFrame,
        x:str,
        y:str,
        hue:str = None,
        title:str = None,
        xlabel:str = None,
        ylabel:str = None,
        figsize:Tuple[int] = (10, 6),
        tight_layout:bool = False
    ):
    fig, axe, fs = _get_baseplot(figsize=figsize)

    palette = sns.palettes.color_palette()

    sns.lineplot(
        df,
        x=x,
        y=y, 
        hue=hue,
        ax=axe,
        palette=palette,        
    )

    axe = _set_label_layout(axe, fs, title, xlabel, ylabel, tight_layout)

    return fig, axe

def violinplot(
        df:pd.DataFrame,
        x:str,
        y:str,
        hue:str = None,
        title:str = None,
        xlabel:str = None,
        ylabel:str = None,
        figsize:Tuple[int] = (10, 6),
        tight_layout:bool = False
    ):
    fig, axe, fs = _get_baseplot(figsize=figsize)

    palette = sns.palettes.color_palette()

    sns.violinplot(
        df,
        x=x,
        y=y, 
        hue=hue,
        ax=axe,
        palette=palette,
        width=0.5,
        
    )

    axe = _set_label_layout(axe, fs, title, xlabel, ylabel, tight_layout)

    return fig, axe


def boxplot(
        df:pd.DataFrame,
        x:str,
        y:str,
        stripplot:bool = True,
        hue:str = None,
        title:str = None,
        xlabel:str = None,
        ylabel:str = None,
        figsize:Tuple[int] = (10, 6),
        tight_layout:bool = False
    ):
    fig, axe, fs = _get_baseplot(figsize=figsize)
    
    palette = sns.palettes.color_palette()

    box = sns.boxplot(
        df,
        x=x,
        y=y, 
        hue=hue,
        ax=axe,
        palette=palette,
        width=0.5,
        
    )
    if stripplot:
        for patch in box.patches:
            patch.set_alpha(0.6)
        sns.stripplot(df, x=x, y=y, hue=hue, ax=axe, palette=palette)

    axe = _set_label_layout(axe, fs, title, xlabel, ylabel, tight_layout)

    return fig, axe

def histplot(
        df:pd.DataFrame,
        x:str,
        hue:str = None,
        bins:int = 20,
        kde:bool = False,
        title:str = None,
        xlabel:str = None,
        ylabel:str = None,
        figsize:Tuple[int] = (10, 6),
        tight_layout:bool = False
    ):
    fig, axe, fs = _get_baseplot(figsize=figsize)

    sns.histplot(df, x=x, hue=hue, bins=bins, kde=kde)
    
    axe = _set_label_layout(axe, fs, title, xlabel, ylabel, tight_layout)

    return fig, axe


def pieplot(
        df:pd.DataFrame,
        x:str,
        y:str,
        title:str = None,
        center_text:str = None,
        figsize:Tuple[int] = (10, 6),
        tight_layout:bool = False
    ):
    fig, axe, fs = _get_baseplot(figsize=figsize)
    
    linewidth = figsize[0] * figsize[1] // 20

    _, texts, autotexts = axe.pie(
        df[y],
        radius=1,
        labels=df[x],
        labeldistance=1,
        colors=sns.palettes.color_palette(),
        wedgeprops=dict(width=0.45, edgecolor='white', linewidth=linewidth),
        autopct='%1.1f%%'
    )

    for text, autotext in zip(texts, autotexts):
        x, y = text.get_position()
        text.set_text(f"{text.get_text()}: {autotext.get_text()}")
        text.set_fontsize(fs['tick'])
        text.set_position((1.07*x, 1.07*y))
        autotext.set_text(None)
  
    axe.text(0, 0, center_text, ha='center', va='center', fontsize=fs['label'])

    axe = _set_label_layout(axe, fs, title, '', '', tight_layout)
 
    return fig, axe

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
# Utilities #
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