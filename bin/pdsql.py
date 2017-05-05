import argparse

import numpy as np
from pandasql import sqldf

from research.dataframe import *


def pysqldf(q):
    return sqldf(q, globals())


parser = argparse.ArgumentParser(description='Query a structured file using SQL syntax')
parser.add_argument('input', nargs='+', help='Input files')
parser.add_argument('--sql', '-q', type=str, help='SQL query')
parser.add_argument('--output', '-o', help='Output file')
parser.add_argument('--input-formats', '-f', nargs='*', help='A list of input file formats')
parser.add_argument('--output-format', '-F', help='The output file format', default="parquet")
parser.add_argument('--dtypes', '-d', nargs='*', type=type_mapping, help='Types of column you want to explicitly define')
args = parser.parse_args()

formats = args.input_formats
if formats is None:
    formats = ["parquet" for i in args.input]
if len(formats) == 1 and len(args.input) > 1:
    formats = [formats[0] for i in args.input]
if len(formats) < len(args.input):
    raise ValueError("Not enough input formats")

for idx, file in enumerate(args.input):
    vars()["df{}".format(idx)] = get_file(file, formats[idx])
df = vars()["df0"]

if args.sql is None:
    r = df
else:
    r = pysqldf(args.sql)

if args.dtypes is not None:
    for column, type in args.dtypes:
        r[column] = r[column].astype(getattr(np, type))

if args.output is None:
    print(r)
else:
    save_file(r, args.output, args.output_format)
