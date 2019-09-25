import os

import requests
import pandas as pd


DATASET_FOLDER = "../datasets"


def fetch_dataset(url, filename):
    if not os.path.isdir(DATASET_FOLDER):
        os.makedirs(DATASET_FOLDER)
        
    destination = os.path.join(DATASET_FOLDER, filename)
    
    response = requests.get(url)
    response.raise_for_status()

    with open(destination, "wb") as f:
        for chunk in response.iter_content(10000):
            f.write(chunk)


def load_dataset(filename, dataset_folder=DATASET_FOLDER, delimiter=",",
                 header=None, names=None, skiprows=None,
                 url_to_fetch_if_missing=None):
    
    file_path = os.path.join(dataset_folder, filename)

    if not os.path.isfile(file_path):
        if url_to_fetch_if_missing is not None:
            fetch_dataset(url_to_fetch_if_missing, filename)
        else:
            raise FileNotFoundError("File not found: {}".format(file_path))

    if names is not None:
        df = pd.read_csv(file_path, delimiter=delimiter, header=None,
                         skiprows=skiprows, names=names)
    else:
        df = pd.read_csv(file_path, delimiter=delimiter, header=header,
                         skiprows=skiprows)

    return df


def load_filter_transmittance():
    """Source: NIST Engineering Handbook of Statistical Methods"""
    url = "https://www.itl.nist.gov/div898/handbook/datasets/MAVRO.DAT"
    filename = "MAVRO.DAT"

    return load_dataset(filename, names=["transmittance"], skiprows=25,
                        url_to_fetch_if_missing=url)


# TESTING
if __name__ == "__main__":
    df = load_filter_transmittance()
    print(df.info())