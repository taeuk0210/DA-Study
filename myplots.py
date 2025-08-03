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

_COLORS = [
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
        figsize:Tuple[int] = (10, 6),
        fig = None,
        axe = None,
        fs = None,
        palette = None,
        title:str = None,
        xlabel:str = None,
        ylabel:str = None,
        legend:bool = True,
    ):
    fig, axe, fs, colors = _get_baseplot(figsize, fig, axe, fs, palette)
    
    sns.lineplot(
        data=df,
        x=x,
        y=y, 
        hue=hue,
        ax=axe,
        color=colors,        
    )

    axe = _set_label_layout(axe, fs, title, xlabel, ylabel, legend)

    return fig, axe

def stripplot(
        df:pd.DataFrame,
        x:str,
        y:str,
        hue:str = None,
        figsize:Tuple[int] = (10, 6),
        fig = None,
        axe = None,
        fs = None,
        palette = None,
        title:str = None,
        xlabel:str = None,
        ylabel:str = None,
        legend:bool = True,
    ):
    fig, axe, fs, colors = _get_baseplot(figsize, fig, axe, fs, palette)

    sns.stripplot(
        data=df,
        x=x,
        y=y, 
        hue=hue,
        hue_order=sorted(df[hue].unique()),
        dodge=False,
        ax=axe,
        palette=_get_palette(df, hue, colors),
    )
    axe = _set_label_layout(axe, fs, title, xlabel, ylabel, legend)

    return fig, axe


def violinplot(
        df:pd.DataFrame,
        x:str,
        y:str,
        hue:str = None,
        addstrip:bool = True,
        figsize:Tuple[int] = (10, 6),
        fig = None,
        axe = None,
        fs = None,
        palette = None,
        title:str = None,
        xlabel:str = None,
        ylabel:str = None,
        legend:bool = True,
    ):
    fig, axe, fs, colors = _get_baseplot(figsize, fig, axe, fs, palette)
    
    violin = sns.violinplot(
        data=df,
        x=x,
        y=y, 
        hue=hue,
        hue_order=sorted(df[hue].unique()),
        width=0.5,
        dodge=False,
        ax=axe,
        palette=colors,
        inner='box',
        linewidth=0.5,
    )
    if addstrip:
        from matplotlib.collections import PolyCollection
        _, axe = stripplot(df, x, y, hue, figsize, fig, axe, fs, colors, legend=False)
        for patch in violin.collections:
                if isinstance(patch, PolyCollection):
                    patch.set_alpha(0.6)

    axe = _set_label_layout(axe, fs, title, xlabel, ylabel, legend)
    if not legend:
        axe.get_legend().remove()
    return fig, axe


def boxplot(
        df:pd.DataFrame,
        x:str,
        y:str,
        hue:str = None,
        addstrip:bool = True,
        figsize:Tuple[int] = (10, 6),
        fig = None,
        axe = None,
        fs = None,
        palette = None,
        title:str = None,
        xlabel:str = None,
        ylabel:str = None,
        legend:bool = True,
    ):
    fig, axe, fs, colors = _get_baseplot(figsize, fig, axe, fs, palette)
    
    box = sns.boxplot(
        data=df,
        x=x,
        y=y, 
        hue=hue,
        hue_order=sorted(df[hue].unique()),
        width=0.5,
        dodge=False,
        ax=axe,
        palette=colors,
        linewidth=0.5,
    )
    if addstrip:
        _, axe = stripplot(df, x, y, hue, figsize, fig, axe, fs, colors, legend=False)
        for patch in box.patches:
            patch.set_alpha(0.6)

    axe = _set_label_layout(axe, fs, title, xlabel, ylabel, legend)

    return fig, axe

def histplot(
        df:pd.DataFrame,
        x:str,
        hue:str = None,
        bins:int = 20,
        kde:bool = False,
        figsize:Tuple[int] = (10, 6),
        fig = None,
        axe = None,
        fs = None,
        palette = None,
        title:str = None,
        xlabel:str = None,
        ylabel:str = None,
        legend:bool = True,
    ):
    fig, axe, fs, colors = _get_baseplot(figsize, fig, axe, fs, palette)

    sns.histplot(
        data=df, 
        x=x,
        hue=hue, 
        hue_order=sorted(df[hue].unique()),
        ax=axe, 
        palette=_get_palette(df, hue, colors),
        bins=bins, 
        kde=kde
    )
    axe = _set_label_layout(axe, fs, title, xlabel, ylabel, legend)

    return fig, axe

def pieplot(
        df:pd.DataFrame,
        x:str,
        y:str,
        center_text:str = None,
        figsize:Tuple[int] = (10, 6),
        fig = None,
        axe = None,
        fs = None,
        palette = None,
        title:str = None,
        xlabel:str = None,
        ylabel:str = None,
        legend:bool = True,
    ):
    fig, axe, fs, colors = _get_baseplot(figsize, fig, axe, fs, palette)
    
    linewidth = figsize[0] * figsize[1] // 20

    _, texts, autotexts = axe.pie(
        df[y],
        radius=1,
        labels=df[x],
        labeldistance=1,
        colors=colors,
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

    axe = _set_label_layout(axe, fs, title, xlabel, ylabel, legend)
 
    return fig, axe

def barplot(
        df:pd.DataFrame,
        x:str,
        y:str,
        hue:str,
        figsize:Tuple[int] = (10, 6),
        fig = None,
        axe = None,
        fs = None,
        palette = None,
        title:str = None,
        xlabel:str = None,
        ylabel:str = None,
        legend:bool = True,
    ):
    fig, axe, fs, colors = _get_baseplot(figsize, fig, axe, fs, palette)

    sns.barplot(
        data=df, 
        x=x, 
        y=y, 
        hue=hue, 
        hue_order=sorted(df[hue].unique()),
        width=0.5,
        dodge=False,
        ax=axe, 
        palette=colors
    )
    for i, value in enumerate(df[y]):
        axe.text(i, value, f"{value:.4f}", ha="center", va="bottom", fontsize=fs['label'])

    axe = _set_label_layout(axe, fs, title, xlabel, ylabel, legend)

    return fig, axe

def baseplot(
        figsize:Tuple[int] = (10, 6),
        fig = None,
        axe = None,
        fs = None,
        palette = None,
        nrow:int = 1,
        ncol:int = 1, 
    ):
    return _get_baseplot(figsize, fig, axe, fs, palette, nrow, ncol)

#############
# Utilities #
#############

def _get_colors():
    len_palette = len(_COLORS)
    idx = np.random.choice(np.arange(len_palette), len_palette, False)
    return np.concatenate([_COLORS[i] for i in idx], axis=0)

def _get_palette(df, hue, color):
    hue_order = sorted(df[hue].unique())
    return {h:c for h, c in zip(hue_order, color)}

def _get_fontsize(figsize, nrow, ncol):
    minsize = min(int(figsize[0] / ncol), int(figsize[1] / nrow))
    scale = minsize * minsize / 40
    return {
        "title": round(30 * scale, 1),
        "label": round(20 * scale, 1),
        "tick": round(15 * scale, 1)}

def _get_baseplot(
        figsize:Tuple[int] = (10, 6),
        fig = None,
        axe = None,
        fs = None,
        palette = None,
        nrow:int = 1,
        ncol:int = 1, 
    ):

    if palette is None:
        palette = _get_colors()

    if fig is not None and axe is not None and fs is not None:
        return fig, axe, fs, palette
    
    fig, axe = plt.subplots(nrow, ncol, figsize=figsize)
    fs = _get_fontsize(figsize, nrow, ncol)

    if nrow * ncol == 1:
        axe.set_facecolor("#F0F0F0")
    else:
        for ax in axe.flatten():
            ax.set_facecolor("#F0F0F0")
    return fig, axe, fs, palette

def _set_label_layout(
        axe,
        fs:Dict[str, int],
        title:str = None,
        xlabel:str = None,
        ylabel:str = None,
        legend:bool = True,
    ):
    axe.set_title(title, fontsize=fs['title'], fontweight="bold")
    axe.set_xlabel(xlabel, fontsize=fs['label'], color='#000000')
    axe.set_ylabel(ylabel, fontsize=fs['label'], color='#000000')

    axe.tick_params(axis='x', labelsize=fs['tick'], color='#000000')
    axe.tick_params(axis='y', labelsize=fs['tick'], color='#000000') 
    
    if legend and axe.get_legend() is not None:
        leg = axe.get_legend()
        for text in leg.get_texts():
            text.set_fontsize(fs.get('legend', fs['tick']))
            text.set_fontweight("normal")
        leg.set_title(None)
    return axe