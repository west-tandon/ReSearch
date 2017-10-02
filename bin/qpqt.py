import argparse

from fastparquet import ParquetFile


def parse_condition(df, condition):
    """
    Parse a condition string to a pandas condition.
    NOTE: currently, only equality conditions are supported.
    NOTE: they should not contain any spaces
    :param df:          data frame
    :param condition:   a condition string, e.g., query=1
    :return:            a pandas condition
    """
    s = condition.split('=')
    return df[s[0]] == df.dtypes[s[0]].type(s[1])


def filter_rows(df, conditions):
    condition_array = [parse_condition(df, condition) for condition in conditions]
    for condition in condition_array:
        df = df[condition]
    return df

parser = argparse.ArgumentParser(description='Retrieve data from parquet file')
parser.add_argument('input', type=str, help='Parquet input file')
parser.add_argument('--columns', '-c', nargs='+', help='Columns to select')
parser.add_argument('--where', '-w', nargs='+', help='Filtering conditions in format: column=value (no spaces)')
args = parser.parse_args()

pf = ParquetFile(args.input)

# Filter columns
if args.columns is None:
    df = pf.to_pandas()
else:
    df = pf.to_pandas(args.columns)

# Filter rows
if args.where is not None:
    df = filter_rows(df, args.where)

print(df.to_string())
