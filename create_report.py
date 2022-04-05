from __future__ import annotations

import pickle

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from tqdm import tqdm

from conf import CHANNELS, FEATURES

with open("outputs/18Dec2020/128bins_1xDownScale/Campnosperma Auriculatum_27.npz", "rb") as f:
    out = pickle.load(f)

channels = CHANNELS
features = FEATURES

tree = out
def create_image():

    fig, axs = plt.subplots(8, 9, figsize=(20, 20))
    for ij in tqdm(range(8 * 9), desc='Creating Image Plots'):
        i = ij // 9
        j = ij % 9
        ax: plt.Axes = axs[i][j]
        ax.imshow(tree[..., i, j])

        # ax.axis('off')
        ax.set_yticks([])
        ax.set_xticks([])
        if i == 0:
            ax.set_title(features[j])
        if j == 0:
            ax.set_ylabel(channels[i], rotation='horizontal', ha='right')

    fig.tight_layout()
    fig.show()

create_image()

#%%
def create_hist():

    fig, axs = plt.subplots(8, 9, figsize=(15, 10), sharex='col')
    for ij in tqdm(range(8 * 9), desc='Creating Histogram Plots'):
        i = ij // 9
        j = ij % 9

        ax: plt.Axes = axs[i][j]
        sns.histplot(tree[..., i, j].flatten(), bins=100, kde=True, ax=ax)

        # ax.axis('off')
        ax.set_yticks([])
        ax.set_xticks([])
        ax.set_ylabel("")
        if i == 0:
            ax.set_title(features[j])
        if j == 0:
            ax.set_ylabel(channels[i], rotation='horizontal', ha='right')

    fig.tight_layout()
    fig.show()

create_hist()

# %%
plt.imshow(tree[..., 3, 0])
plt.show()
# %%
np.max(tree[..., 3, 7])
