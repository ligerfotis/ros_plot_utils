import pandas as pd
import sys

df_dict = {}


def load(list_of_files):
    for filename in list_of_files:
        df = pd.read_csv("stripped_final/"+filename)
        df_dict[filename] = df
    return df_dict
