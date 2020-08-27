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


def plot_aperture(list_of_files):
    # load a dictionary of the dataframes of each file
    df_dict = load(list_of_files, record_type)

    # plot on separate figure for each file
    for filename in list_of_files:
        plt.figure("Aperture_" + filename[:-4], figsize=[12, 8])
        current_df = df_dict[filename]
        timestamps = current_df["TimeStamps"].tolist()
        timestamps = regularize_time(timestamps)
        aperture, blacklist = extractAperture(current_df)
        # remove the timestamps for which there was a point missing either from the index or thumb fingertips
        [timestamps.pop(idx) for idx in blacklist]
        # plot
        plt.plot(timestamps, aperture, label=filename[:-4], marker='o')

        plt.legend(loc="upper left")
        plt.savefig(path + record_type + "/" + "aperture_" + filename[:-4])  # remove the .csv extension

    # plot a line for each file
    plt.figure("Aperture", figsize=[12, 8])
    for filename in list_of_files:
        current_df = df_dict[filename]
        timestamps = current_df["TimeStamps"].tolist()
        timestamps = regularize_time(timestamps)
        aperture, blacklist = extractAperture(current_df)
        # remove the timestamps for which there was a point missing either from the index or thumb fingertips
        [timestamps.pop(idx) for idx in blacklist]
        # plot
        plt.plot(timestamps, aperture, label=filename)

    plt.legend(loc="upper left")
    plt.savefig(path + record_type + "/" + "total_aperture")
    # plt.show()


# get timestamps relevant to the human action
def regularize_time(timestamps):
    min_val = min(timestamps)
    timestamps[:] = [val - min_val for val in timestamps]
    return timestamps


def extractAperture(current_df):
    aperture = []

    index = np.asarray(
        [current_df["RIndex4FingerTip_x"], current_df["RIndex4FingerTip_y"], current_df["RIndex4FingerTip_z"]]).T
    thumb = np.asarray(
        [current_df["RThumb4FingerTip_x"], current_df["RThumb4FingerTip_y"], current_df["RThumb4FingerTip_z"]]).T
    blacklist = []

    for idx, (index_point, thumb_point) in enumerate(zip(index, thumb)):
        tmp_aperture = distance.euclidean(index_point, thumb_point)
        if tmp_aperture != distance.euclidean(index_point, [0, 0, 0]) \
                or tmp_aperture != distance.euclidean(thumb_point, [0, 0, 0]):
            aperture.append(tmp_aperture)
        else:
            blacklist.append(idx)

    return aperture, blacklist


if __name__ == "__main__":
    record_type = sys.argv[1]  # live or on_demand
    if record_type not in record_types:
        print("Please select record type [live or on_demand]")
        exit(1)

    list_of_files = [f for f in listdir("stripped_final/" + record_type + "/") if isfile(join("stripped_final/" + record_type + "/", f))]
    plot_aperture(list_of_files)
