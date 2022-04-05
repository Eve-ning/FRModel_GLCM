# FRModel_GLCM
 GLCM Parser for FRModel

# Output Format

shape = `(Height, Width, Channel, Features)`

## Channels
```
Wideband Red = 0
Wideband Green = 1
Wideband Blue = 2
RedEdge = 3
Blue = 4
NIR = 5
Red = 6
Green = 7
```          
## Features
```
NONE = 0
HOMOGENEITY = 1
CONTRAST = 2
ASM = 3
MEAN_I = 4
MEAN_J = 5
VAR_I = 6
VAR_J = 7
CORRELATION = 8
```
## Example
```py
import pickle

with open("...pickle", "rb") as f:
    ar = pickle.load(f)
    
ar_rededge_meanj = ar[..., 3, 5]    
ar_wbgreen_correlation = ar[..., 1, 8]
```
# Instructions

## Dependencies

You need to install `glcm-cupy` and `cupy`

```shell
pip install glcm-cupy
```

CuPy will differ depending on your environment and CUDA Version.

[**See this for more details**](https://docs.cupy.dev/en/stable/install.html)

```
pip install cupy-cuda116
conda install -c conda-forge cupy cudatoolkit=11.6
```

## TIF Files

You need to add the `.tif` files manually first, see **Directory Structure**

I have only provided the `bounds.csv`, so just place them accordingly

## Execution

To run,

```shell
python main.py
```

## Params

Do change the last line of the code to change the
- Bin Size
  - The number of bins.
  - Note it's not bits, thus, 6bit == 2 ** 6bins
- Downscale Size
  - If `1`, then the image is original size
  - If `2`, then the image is half size
  - If `3`, it's 1/3,
  - and so on..

The results will be thrown into `outputs`.

## Directory Structure

Place your inputs like so.
The bounds are provided, please use these

```
inputs
  - 10May2021
    - 90deg43m85pct255deg
      - bounds.csv
      - result.tif
      - result_Blue.tif
      - result_Green.tif
      - result_NIR.tif
      - result_Red.tif
      - result_RedEdge.tif
  - 18Dec2020
    - bounds.csv
    - result.tif
    - result_Blue.tif
    - result_Green.tif
    - result_NIR.tif
    - result_Red.tif
    - result_RedEdge.tif
outputs
```
