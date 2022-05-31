from itertools import combinations

CHANNELS = ["Wideband Red",
            "Wideband Green",
            "Wideband Blue",
            "RedEdge",
            "Blue",
            "NIR",
            "Red",
            "Green", ]

CHANNELS_CROSS = list(map(str, combinations(CHANNELS, 2)))


FEATURES = ["HOMOGENEITY",
            "CONTRAST",
            "ASM",
            "MEAN",
            "VAR",
            "CORRELATION"]
NO_OF_FEATURES = len(FEATURES)
NO_OF_CHANNELS = 8

HIST_BINS = 100
STACKED_HIST_ALPHA = 0.3
GLCM_STACK_HIST_FIGSIZE = 25, 20
GLCM_HIST_FIGSIZE = 20, 20
GLCM_IM_FIGSIZE = 15, 10

GLCM_CROSS_STACK_HIST_FIGSIZE = 25, 25
GLCM_CROSS_HIST_FIGSIZE = 20, 20
GLCM_CROSS_IM_FIGSIZE = 12, 23


CHANNELS = ["Wideband Red",
            "Wideband Green",
            "Wideband Blue",
            "RedEdge",
            "Blue",
            "NIR",
            "Red",
            "Green", ]

CHANNELS_CROSS = list(map(str, combinations(CHANNELS[3:], 2)))
