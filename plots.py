import numpy as np
import pandas as pd

from typing import Tuple, Dict, List

import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

# Set global configuration

mpl.rcParams['font.family'] = 'Malgun Gothic'
mpl.rcParams['axes.unicode_minus'] = False

plt.style.use("ggplot")

# Set global constants

_PALETTES = [
    ["#A6E3E9", "#71C9CE", "#E3FDFD", "#CBF1F5"],
    ["#3F72AF", "#112D4E", "#F9F7F7", "#DBE2EF"],
    ["#FFD1D1", "#FF9494", "#FFF5E4", "#FFE3E1"],
    ["#B83B5E", "#6A2C70", "#F9ED69", "#F08A5D"],
    ["#F5F5F5", "#FC5185", "#364F6B", "#3FC1C9"],
    ["#609966", "#40513B", "#EDF1D6", "#9DC08B"],
]

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

    sns.lineplot(
        df,
        x=x,
        y=y, 
        hue=hue,
        ax=axe,
        palette=_get_palette(),        
    )

    axe = _set_label_layout(axe, fs, title, xlabel, ylabel, tight_layout)

    return fig, axe

def stripplot(
        df:pd.DataFrame,
        x:str,
        y:str,
        hue:str = None,
        palette: List[str] = None,
        fig = None,
        axe = None, 
        fs = None,
        title:str = None,
        xlabel:str = None,
        ylabel:str = None,
        figsize:Tuple[int] = (10, 6),
        tight_layout:bool = False
    ):
    if axe is None:
        fig, axe, fs = _get_baseplot(figsize=figsize)  
    
    if palette is None:
        palette = _get_palette()

    sns.stripplot(
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
        addstrip:bool = True,
        title:str = None,
        xlabel:str = None,
        ylabel:str = None,
        figsize:Tuple[int] = (10, 6),
        tight_layout:bool = False
    ):
    fig, axe, fs = _get_baseplot(figsize=figsize)  
    
    palette = _get_palette()
    violin = sns.violinplot(
        df,
        x=x,
        y=y, 
        hue=hue,
        ax=axe,
        palette=palette,
        inner='box'
    )
    if addstrip:
        _, axe = stripplot(df, x, y, hue, palette, fig, axe, fs)
        for patch in violin.collections:
            patch.set_alpha(0.2)

    axe = _set_label_layout(axe, fs, title, xlabel, ylabel, tight_layout)

    return fig, axe


def boxplot(
        df:pd.DataFrame,
        x:str,
        y:str,
        hue:str = None,
        addstrip:bool = True,
        title:str = None,
        xlabel:str = None,
        ylabel:str = None,
        figsize:Tuple[int] = (10, 6),
        tight_layout:bool = False
    ):
    fig, axe, fs = _get_baseplot(figsize=figsize)  
    
    palette = _get_palette()
    box = sns.boxplot(
        df,
        x=x,
        y=y, 
        hue=hue,
        ax=axe,
        palette=palette,
        width=0.5,
    )
    if addstrip:
        _, axe = stripplot(df, x, y, hue, palette, fig, axe, fs)
        for patch in box.patches:
            patch.set_alpha(0.6)

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

    sns.histplot(
        df, 
        x=x,
        hue=hue, 
        ax=axe, 
        palette=_get_palette(),
        bins=bins, 
        kde=kde
    )
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
        colors=_get_palette(),
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

    sns.barplot(
        df, 
        x=x, 
        y=y, 
        hue=hue, 
        ax=axe, 
        palette=_get_palette()
    )
    for i, value in enumerate(df[y]):
        axe.text(i, value, f"{value:.4f}", ha="center", va="bottom", fontsize=fs['label'])

    axe = _set_label_layout(axe, fs, title, xlabel, ylabel, tight_layout)

    return fig, axe

#############
# Utilities #
#############

def _get_palette():
    len_palette = len(_PALETTES)
    idx = np.random.choice(np.arange(len_palette), len_palette, False)
    return np.concatenate([_PALETTES[i] for i in idx], axis=0)

def _get_fontsize(figsize, base_area=40):
    scale = figsize[0] * figsize[1] / base_area
    return {
        "title": round(15 * scale, 1),
        "label": round(11 * scale, 1),
        "tick": round(9 * scale, 1)}

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