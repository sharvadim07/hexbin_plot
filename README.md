## Overview

Generate Hexbin plots for table(s).

## How to use 
```
usage: hexbin_plot.py [-h] -t TABLES [-x XLIM] [-y YLIM] [-c CIRCLES_TABLES] -p PREFIX
                      -w WORK_DIR

optional arguments:
  -h, --help            show this help message and exit
  -t TABLES, --tables TABLES
                        Table or comma seaprated tables to construct hexbin.
  -x XLIM, --xlim XLIM  Limit for x axis.
  -y YLIM, --ylim YLIM  Limit for y axis.
  -c CIRCLES_TABLES, --circles_tables CIRCLES_TABLES
                        Table or comma seaprated tables for add circle.
  -p PREFIX, --prefix PREFIX
                        prefix
  -w WORK_DIR, --work_dir WORK_DIR
                        Working (output) dir absolute path.
```