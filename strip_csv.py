import csv
import os

import pandas as pd
import re
import numpy as np
from scipy import stats
import sys
from os import listdir
from os.path import isfile, join


# the z score value used to filter outliers
zscore = 2.698

path = "stripped_final/"
if not os.path.exists(path):
    os.makedirs(path)


# Function to extract all the distinct keypoints from a csv
def getKeyPoints(columns):
    columns = "".join(columns)
    array = re.findall(r"/topic_transform/keypoints/[0-9]+/points/point/x", columns)
    return array


# Function to extract all the distinct keypoint names from a csv
def getKeypointNames(df):
    listOfNames = []
    for col in df.columns[1:]:
        if "name" in col:
            listOfNames.append(df[col].loc[0])
    return listOfNames


def keypointExtractor(filename, withOutliers=False):
    df = pd.read_csv(filename)

    listOfNames = getKeypointNames(df)
    numOfKeyPoints = len(getKeyPoints(df.columns))

    listOfKeyPoints_x = ["/topic_transform/keypoints/" + str(i) + "/points/point/x" for i in range(numOfKeyPoints)]
    listOfKeyPoints_y = ["/topic_transform/keypoints/" + str(i) + "/points/point/y" for i in range(numOfKeyPoints)]
    listOfKeyPoints_z = ["/topic_transform/keypoints/" + str(i) + "/points/point/z" for i in range(numOfKeyPoints)]

    new_listOfKeyPoints_x, new_listOfKeyPoints_y, new_listOfKeyPoints_z = [], [], []
    new_listOfNames = []
    # create new dataframe containing only columns with point information
    new_df = pd.DataFrame()
    new_df["TimeStamps"] = df.ix[:, 0]
    for i, point_list_names in enumerate(zip(listOfKeyPoints_x, listOfKeyPoints_y, listOfKeyPoints_z)):
        # check if keypoint contains mostly zero points
        count_valid_array = [(df[col_point] != 0).sum() for col_point in point_list_names]

        if all([point > numOfKeyPoints / 4 for point in count_valid_array]):
            new_listOfKeyPoints_x.append(listOfNames[i] + "_x")
            new_listOfKeyPoints_y.append(listOfNames[i] + "_y")
            new_listOfKeyPoints_z.append(listOfNames[i] + "_z")
            new_listOfNames.append(listOfNames[i])

            new_df[listOfNames[i] + "_x"] = df[point_list_names[0]].astype(float).round(7)
            new_df[listOfNames[i] + "_y"] = df[point_list_names[1]].astype(float).round(7)
            new_df[listOfNames[i] + "_z"] = df[point_list_names[2]].astype(float).round(7)

    # replace zero values with NAN so they do not plot
    # new_df.replace(0, np.nan, inplace=True)

    # remove outliers
    if withOutliers:
        new_df = new_df[(np.abs(stats.zscore(new_df)) < zscore).all(axis=1)]

    return new_df


if __name__ == "__main__":
    list_of_files = [f for f in listdir("data") if isfile(join("data", f))]
    for filename in list_of_files:
        # filename = sys.argv[1]
        print("Stripping file: %s" % filename)
        df = keypointExtractor("data/" + filename)
        # print(path + filename)
        df.to_csv(path + filename, index=False)
        # df.to_csv(path + filename, index=False, na_rep='NA')

