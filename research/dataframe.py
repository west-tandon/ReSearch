import fastparquet as fp
import pandas as pd


def type_mapping(s):
    [column, type] = s.split('=')
    return column, type


def get_file(name, file_format):
    if file_format == "parquet":
        return fp.ParquetFile(name).to_pandas()
    elif file_format == "csv":
        return pd.read_csv(name)
    else:
        raise ValueError("unknown file format: {}".format(file_format))


def save_file(df, name, file_format):
    if file_format == "parquet":
        fp.write(name, df)
    elif file_format == "csv":
        df.to_csv(name, index=False)
    else:
        raise ValueError("unknown file format: {}".format(file_format))

