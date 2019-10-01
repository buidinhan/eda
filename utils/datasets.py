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
                 url_to_fetch_if_missing=None, **kwargs):
    
    file_path = os.path.join(dataset_folder, filename)

    if not os.path.isfile(file_path):
        if url_to_fetch_if_missing is not None:
            fetch_dataset(url_to_fetch_if_missing, filename)
        else:
            raise FileNotFoundError("File not found: {}".format(file_path))

    if names is not None:
        df = pd.read_csv(file_path, delimiter=delimiter, header=None,
                         skiprows=skiprows, names=names, **kwargs)
    else:
        df = pd.read_csv(file_path, delimiter=delimiter, header=header,
                         skiprows=skiprows, **kwargs)

    return df


def load_filter_transmittance():
    """Source: NIST Engineering Handbook of Statistical Methods"""
    url = "https://www.itl.nist.gov/div898/handbook/datasets/MAVRO.DAT"
    filename = "MAVRO.DAT"

    return load_dataset(filename, names=["transmittance"], skiprows=25,
                        url_to_fetch_if_missing=url)


def load_michelson():
    """Source: NIST Engineering Handbook of Statistical Methods"""
    url = "https://www.itl.nist.gov/div898/handbook/datasets/MICHELSO.DAT"
    filename = "MICHELSO.DAT"
    headers = ["light_speed", "air_temperature", "elapsed_days",
               "am_pm", "data_set"]

    return load_dataset(filename, names=headers, skiprows=25,
                        url_to_fetch_if_missing=url,
                        delim_whitespace=True)


def load_weibull():
    """Source: NIST Engineering Handbook of Statistical Methods"""
    url = "https://www.itl.nist.gov/div898/handbook/datasets/RANDWEIB.DAT"
    filename = "RANDWEIB.DAT"
    
    return load_dataset(filename, names=["y"], skiprows=25,
                        url_to_fetch_if_missing=url)


def load_beam_deflection():
    """Source: NIST Engineering Handbook of Statistical Methods"""
    url = "https://www.itl.nist.gov/div898/handbook/datasets/LEW.DAT"
    filename = "LEW.DAT"

    return load_dataset(filename, names=["Deflection"], skiprows=25,
                        url_to_fetch_if_missing=url)


def load_normal():
    """Source: NIST Engineering Handbook of Statistical Methods"""
    url = "https://www.itl.nist.gov/div898/handbook/datasets/NORMAL.DAT"
    filename = "NORMAL.DAT"

    return load_dataset(filename, names=["y"], skiprows=25,
                        url_to_fetch_if_missing=url)


def load_water_density():
    """Source: NIST Engineering Handbook of Statistical Methods"""
    url = "https://www.itl.nist.gov/div898/handbook/datasets/JONES.DAT"
    filename = url.split("/")[-1]

    return load_dataset(filename, names=["Density", "Temperature"],
                        skiprows=25, url_to_fetch_if_missing=url,
                        delim_whitespace=True)


def load_alaska_pipeline():
    """Source: NIST Engineering Handbook of Statistical Methods"""
    url = "https://www.itl.nist.gov/div898/handbook/datasets/BERGER1.DAT"
    filename = url.split("/")[-1]
    names = ["In-Field Defect Size", "In-Lab Defect Size", "Batch"]
    
    return load_dataset(filename, names=names, skiprows=25,
                        url_to_fetch_if_missing=url,
                        delim_whitespace=True)

def load_heat_flow_meter():
    """Source: NIST Engineering Handbook of Statistical Methods"""
    url = "https://www.itl.nist.gov/div898/handbook/datasets/ZARR13.DAT"
    filename = url.split("/")[-1]

    return load_dataset(filename, names=["calibration_factor"],
                        skiprows=25, url_to_fetch_if_missing=url)


def load_uniform():
    """Source: NIST Engineering Handbook of Statistical Methods"""
    url = "https://www.itl.nist.gov/div898/handbook/datasets/RANDU.DAT"
    filename = url.split("/")[-1]
    names = ["C1", "C2", "C3", "C4", "C5"]

    df = load_dataset(filename, names=names, skiprows=25,
                      url_to_fetch_if_missing=url,
                      delim_whitespace=True)
    all_values = df.to_numpy().ravel()
    
    return pd.DataFrame(all_values, columns=["y"])


def load_airplane_glass_failure():
    """Source: NIST Engineering Handbook of Statistical Methods"""
    url = "https://www.itl.nist.gov/div898/handbook/datasets/FULLER2.DAT"
    filename = url.split("/")[-1]

    return load_dataset(filename, names=["y"], skiprows=25,
                        url_to_fetch_if_missing=url)


def load_normal_random_numbers():
    """Source: NIST Engineering Handbook of Statistical Methods"""
    url = "https://www.itl.nist.gov/div898/handbook/datasets/RANDN.DAT"
    filename = url.split("/")[-1]
    names = ["C{}".format(i) for i in range(1, 11)]
    df = load_dataset(filename, names=names, skiprows=25,
                      url_to_fetch_if_missing=url,
                      delim_whitespace=True)
    all_values = df.to_numpy().ravel()
    
    return pd.DataFrame(all_values, columns=["y"])


def load_flicker_noise():
    """Source: NIST Engineering Handbook of Statistical Methods"""
    url = "https://www.itl.nist.gov/div898/handbook/datasets/FLICKER.DAT"
    filename = url.split("/")[-1]

    return load_dataset(filename, names=["y"], skiprows=25,
                        url_to_fetch_if_missing=url)


def load_random_walk():
    """Source: NIST Engineering Handbook of Statistical Methods"""
    url = "https://www.itl.nist.gov/div898/handbook/datasets/RANDWALK.DAT"
    filename = url.split("/")[-1]

    return load_dataset(filename, names=["y"], skiprows=25,
                        url_to_fetch_if_missing=url)


def load_josephson_junction_cryothermometry():
    """Source: NIST Engineering Handbook of Statistical Methods"""
    url = "https://www.itl.nist.gov/div898/handbook/datasets/SOULEN.DAT"
    filename = url.split("/")[-1]
    names = ["C{}".format(i) for i in range(1, 6)]
    df = load_dataset(filename, names=names, skiprows=25,
                      url_to_fetch_if_missing=url,
                      delim_whitespace=True)
    all_values = df.to_numpy().ravel()
    
    return pd.DataFrame(all_values, columns=["y"])


def load_ceramic_strength():
    """Source: NIST Engineering Handbook of Statistical Methods"""
    url = "https://www.itl.nist.gov/div898/handbook/datasets/JAHANMI2.DAT"
    filename = url.split("/")[-1]
    names = ["Run", "Lab", "Bar ID", "Test", "Y", "X1", "X2", "X3", "X4",
             "Treatment", "Set", "Llab", "Rep", "Batch", "Sblab", "Set2"]
    
    return load_dataset(filename, names=names, skiprows=50,
                        url_to_fetch_if_missing=url,
                        delim_whitespace=True)


def load_notch_testing():
    """Source: NIST Engineering Handbook of Statistical Methods"""
    url = "https://www.itl.nist.gov/div898/handbook/datasets/SPLETT2.DAT"
    filename = url.split("/")[-1]
    
    return load_dataset(filename, names=["Energy", "Machine"],
                        skiprows=25, url_to_fetch_if_missing=url,
                        delim_whitespace=True)


def load_fatigue_life():
    """Source: NIST Engineering Handbook of Statistical Methods"""
    url = "https://www.itl.nist.gov/div898/handbook/datasets/BIRNSAUN.DAT"
    filename = url.split("/")[-1]

    return load_dataset(filename, names=["y"], skiprows=25,
                        url_to_fetch_if_missing=url)


def load_lead_wire_weld():
    """Source: NIST Engineering Handbook of Statistical Methods"""
    url = "https://www.itl.nist.gov/div898/handbook/datasets/SHEESLE2.DAT"
    filename = url.split("/")[-1]
    names = ["Defects", "Weld", "Plant", "Speed", "Shift", "Tag"]
    
    return load_dataset(filename, names=names, skiprows=25,
                        url_to_fetch_if_missing=url,
                        delim_whitespace=True)


# TESTING
if __name__ == "__main__":
    df = load_lead_wire_weld()
    print(df.info())
    print(df.head())
    print(df.tail())
