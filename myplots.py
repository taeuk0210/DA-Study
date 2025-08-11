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
    ["#B2B0E8", "#1A2A80", "#7A85C1", "#3B38A0"],
    ["#EEEEEE", "#B9375D", "#E7D3D3", "#D25D5D"],
    ["#FCF8DD", "#00809D", "#FFD700", "#D3AF37"],
    ["#FEFFC4", "#799EFF", "#FFDE63", "#FFBC4C"],
    ["#77BEF0", "#FFCB61", "#FF894F", "#EA5B6F"],
]

#############
# Draw plot #
#############

def featureplot(
        feature_name,
        feature_value,
        figsize:Tuple[int] = (10, 6),
        fig = None,
        axe = None,
        fs = None,
        title:str = None,
        xlabel:str = None,
        ylabel:str = None,
        legend:bool = True
    ):
    fig, axe, fs = _get_baseplot(figsize, fig, axe, fs)
    
    sns.barplot(
        x=feature_name,
        y=feature_value,
        orient="h",
        palette="rainbow"
    )

    axe = _set_label_layout(axe, fs, title, xlabel, ylabel, legend)

    return fig, axe

def heatmap(
        df:pd.DataFrame,
        figsize:Tuple[int] = (10, 6),
        fig = None,
        axe = None,
        fs = None,
        title:str = None,
        xlabel:str = None,
        ylabel:str = None,
        legend:bool = True,
    ):
    fig, axe, fs = _get_baseplot(figsize, fig, axe, fs)
    
    sns.heatmap(
        data=df,
        ax=axe,    
    )

    axe = _set_label_layout(axe, fs, title, xlabel, ylabel, legend)

    return fig, axe


def scatterplot(
        df:pd.DataFrame,
        x:str,
        y:str,
        hue:str = None,
        addline:bool = False,
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
    fig, axe, fs = _get_baseplot(figsize, fig, axe, fs)
    hue_order, palette = _get_palette(df, hue, palette)
    
    sns.scatterplot(
        data=df,
        x=x,
        y=y, 
        hue=hue,
        hue_order=hue_order,
        ax=axe,
        palette=palette,        
    )

    if addline:
        from sklearn.linear_model import LinearRegression
        lm = LinearRegression()
        lm.fit(df["X"].values.reshape(-1, 1), df["Y"].values.reshape(-1, 1))
        axe.axline((0, lm.intercept_[0]), slope=lm.coef_[0][0])

    axe = _set_label_layout(axe, fs, title, xlabel, ylabel, legend)

    return fig, axe

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
    fig, axe, fs = _get_baseplot(figsize, fig, axe, fs)
    hue_order, palette = _get_palette(df, hue, palette)
    
    sns.lineplot(
        data=df,
        x=x,
        y=y, 
        hue=hue,
        hue_order=hue_order,
        ax=axe,
        color=palette,        
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
    fig, axe, fs = _get_baseplot(figsize, fig, axe, fs)
    hue_order, palette = _get_palette(df, hue, palette)

    sns.stripplot(
        data=df,
        x=x,
        y=y, 
        hue=hue,
        hue_order=hue_order,
        dodge=False,
        ax=axe,
        palette=palette,
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
    fig, axe, fs = _get_baseplot(figsize, fig, axe, fs)
    hue_order, palette = _get_palette(df, hue, palette)
    
    violin = sns.violinplot(
        data=df,
        x=x,
        y=y, 
        hue=hue,
        width=0.5,
        dodge=False,
        ax=axe,
        palette=palette,
        inner='box',
        linewidth=0.5,
    )
    if addstrip:
        from matplotlib.collections import PolyCollection
        _, axe = stripplot(df, x, y, hue, figsize, fig, axe, fs, palette, legend=False)
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
    fig, axe, fs = _get_baseplot(figsize, fig, axe, fs)
    hue_order, palette = _get_palette(df, hue, palette)
    
    box = sns.boxplot(
        data=df,
        x=x,
        y=y, 
        hue=hue,
        hue_order=hue_order,
        width=0.5,
        dodge=False,
        ax=axe,
        palette=palette,
        linewidth=0.5,
    )
    if addstrip:
        _, axe = stripplot(df, x, y, hue, figsize, fig, axe, fs, palette, legend=False)
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
    fig, axe, fs = _get_baseplot(figsize, fig, axe, fs)
    hue_order, palette = _get_palette(df, hue, palette)

    sns.histplot(
        data=df, 
        x=x,
        hue=hue, 
        hue_order=hue_order,
        ax=axe, 
        palette=palette,
        bins=bins, 
        kde=kde
    )
    axe = _set_label_layout(axe, fs, title, xlabel, ylabel, legend)

    return fig, axe

def pieplot(
        df:pd.DataFrame,
        x:str,
        y:str,
        hue:str,
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
    fig, axe, fs = _get_baseplot(figsize, fig, axe, fs)
    _, palette = _get_palette(df, hue, palette)
    linewidth = figsize[0] * figsize[1] // 20

    df = df.sort_values(hue)

    _, texts, autotexts = axe.pie(
        df[y],
        radius=1,
        labels=df[x],
        labeldistance=1,
        colors=[palette[k] for k in palette.keys()],
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
        addtext:bool = False,
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
    fig, axe, fs = _get_baseplot(figsize, fig, axe, fs)
    hue_order, palette = _get_palette(df, hue, palette)

    max_label_len = max([len(lab) for lab in hue_order])

    sns.barplot(
        data=df, 
        x=x, 
        y=y, 
        hue=hue, 
        hue_order=hue_order,
        width=0.5,
        dodge=False,
        ax=axe, 
        palette=palette,
    )
    if addtext:
        for i, value in enumerate(df[y]):
            axe.text(i, value, f"{value:.4f}", ha="center", va="bottom", fontsize=fs['label'])
    if max_label_len > 6:
        axe.tick_params(axis='x', rotation=90)

    axe = _set_label_layout(axe, fs, title, xlabel, ylabel, legend)

    return fig, axe

def baseplot(
        figsize:Tuple[int] = (10, 6),
        fig = None,
        axe = None,
        fs = None,
        nrow:int = 1,
        ncol:int = 1, 
    ):
    return _get_baseplot(figsize, fig, axe, fs, nrow, ncol)

#############
# Utilities #
#############

def _get_colors(num_colors:int = 4):
    len_color_sets = len(_COLORS)
    if (num_colors <= len(_COLORS[0])):
        return _COLORS[np.random.randint(0, len_color_sets)]
    np.random.shuffle(_COLORS)
    return np.concatenate([c for c in _COLORS], axis=0)

def _get_palette(df, hue, palette=None):
    hue_order = sorted(df[hue].unique())
    
    if palette is not None:
        palette = [(k,v) for k,v in palette.items() if k in hue_order]
        palette = sorted(palette, key=lambda x: x[0])
        palette = {k:v for k,v in palette}
        return hue_order, palette

    colors = _get_colors(len(hue_order))
    palette = {h:c for h, c in zip(hue_order, colors)} if palette is None else palette 
    return hue_order, palette

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
        nrow:int = 1,
        ncol:int = 1, 
    ):
    if fig is not None and axe is not None and fs is not None:
        return fig, axe, fs
    
    fig, axe = plt.subplots(nrow, ncol, figsize=figsize)
    fs = _get_fontsize(figsize, nrow, ncol)

    if nrow * ncol == 1:
        axe.set_facecolor("#FFFFFF")
    else:
        for ax in axe.flatten():
            ax.set_facecolor("#F0F0F0")
    return fig, axe, fs

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