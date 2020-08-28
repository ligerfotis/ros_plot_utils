import sys
from os import listdir, makedirs
from os.path import isfile, join, exists
from scipy.spatial import distance
from load_df_from_csv import load
import numpy as np
import matplotlib.pyplot as plt

record_types = ["live", "on_demand"]
path = "figures/"
if not exists(path):
    makedirs(path)


# get timestamps relevant to the human action
def regularize_time(timestamps):
    min_val = min(timestamps)
    timestamps[:] = [val - min_val for val in timestamps]
    return timestamps


def plot_keypoints(current_df):
    # load a dictionary of the dataframes of each file
    df_dict = load(list_of_files, record_type)


if __name__ == "__main__":
    record_type = sys.argv[1]  # live or on_demand
    if record_type not in record_types:
        print("Please select record type [live or on_demand]")
        exit(1)

    list_of_files = [f for f in listdir("stripped_final/" + record_type + "/") if
                     isfile(join("stripped_final/" + record_type + "/", f))]
    plot_keypoints(list_of_files)
