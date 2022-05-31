# Indices
The channels are in this order
```
Wideband Red
Wideband Green
Wideband Blue
RedEdge
Blue
NIR
Red
Green
```

The features are in this order
```
NONE
HOMOGENEITY
CONTRAST
ASM
MEAN
VAR
CORRELATION
```

## Usage
```py
import pickle
tree_path = "path/to/tree.npz"
with open(tree_path, "rb") as f:
    tree = pickle.load(f)

CHANNEL = 3 # RedEdge
FEATURE = 4 # Mean
tree_RE_MEAN = tree[..., CHANNEL, FEATURE]
```