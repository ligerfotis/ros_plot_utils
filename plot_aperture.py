from os import listdir, makedirs
from os.path import isfile, join, exists

from matplotlib.font_manager import FontProperties
from scipy.spatial import distance

from load_df_from_csv import load
import numpy as np
import matplotlib.pyplot as plt

path = "figures/"
if not exists(path):
    makedirs(path)


def plot_aperture(list_of_files):
    df_dict = load(list_of_files)
    # columns = df_dict[list_of_files[0]].columns[1:]
    plt.figure("Aperture", figsize=[12, 8])
    list_of_handles = []
    for filename in list_of_files:
        current_df = df_dict[filename]
        timestamps = current_df["TimeStamps"].tolist()
        timestamps = regularize_time(timestamps)
        aperture, blacklist = extractAperture(current_df)
        [timestamps.pop(idx) for idx in blacklist]
        list_of_handles.append(plt.plot(timestamps, aperture, label=filename)[0])

    plt.legend(loc="upper left")
    # fontP = FontProperties()
    # plt.legend(handles=list_of_handles, bbox_to_anchor=(1.05, 1), loc='upper left', prop=fontP)
    plt.savefig(path + "aperture")
    # plt.show()


def regularize_time(timestamps):
    min_val = min(timestamps)
    timestamps[:] = [val - min_val for val in timestamps]
    return timestamps


def extractAperture(current_df):
    # calculate aperture
    aperture = []

    index = np.asarray([current_df["RIndex4FingerTip_x"], current_df["RIndex4FingerTip_y"], current_df["RIndex4FingerTip_z"]]).T
    thumb = np.asarray([current_df["RThumb4FingerTip_x"], current_df["RThumb4FingerTip_y"], current_df["RThumb4FingerTip_z"]]).T
    blacklist = []

    for index, (index_point, thumb_point) in enumerate(zip(index, thumb)):
        tmp_aperture = distance.euclidean(index_point, thumb_point)
        if tmp_aperture != distance.euclidean(index_point, [0, 0, 0]) or tmp_aperture != distance.euclidean(thumb_point, [0, 0, 0]):
            aperture.append(tmp_aperture)
        else:
            blacklist.append(index)

    return aperture, blacklist


if __name__ == "__main__":
    list_of_files = [f for f in listdir("stripped_final") if isfile(join("stripped_final", f))]
    plot_aperture(list_of_files)
