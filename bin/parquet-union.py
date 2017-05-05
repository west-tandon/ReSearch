import argparse

import numpy as np
from fastparquet import ParquetFile

from research.dataframe import *


parser = argparse.ArgumentParser(description='Union parquet files into one file')
parser.add_argument('input', nargs='+', type=str, help='Parquet input files')
parser.add_argument('--output', '-o', help='Output file')
parser.add_argument('--dtypes', '-d', nargs='*', type=type_mapping, help='Types of column you want to explicitly define')
args = parser.parse_args()

r = pd.concat([ParquetFile(f).to_pandas() for f in args.input])

if args.dtypes is not None:
    for column, type in args.dtypes:
        r[column] = r[column].astype(getattr(np, type))

if args.output is None:
    print(r)
else:
    save_file(r, args.output, 'parquet')
