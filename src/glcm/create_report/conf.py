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
