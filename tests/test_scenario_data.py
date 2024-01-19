import yaml
import pandas as pd
import numpy as np
from premise.ecoinvent_modification import (
    LIST_IMAGE_REGIONS,
    LIST_REMIND_REGIONS,
    SUPPORTED_EI_VERSIONS,
)
from premise.geomap import Geomap

from datapackage import Package

FILEPATH_DATAPACKAGE_SCHEMA = "./datapackage.json"
dp = Package(FILEPATH_DATAPACKAGE_SCHEMA)

resource = dp.get_resource("config")
config_file = yaml.safe_load(resource.raw_read())


resource = dp.get_resource("scenario_data")
scenario_data = resource.read()
scenario_headers = resource.headers

df = pd.DataFrame(scenario_data, columns=scenario_headers)



def test_scenario_data_file():
    mandatory_fields = ["model", "pathway", "region", "variables", "unit"]
    if not all(v in df.columns for v in mandatory_fields):
        raise ValueError(
            f"One or several mandatory column are missing "
            f"in the scenario data file. Mandatory columns: {mandatory_fields}."
        )

    years_cols = []
    for h, header in enumerate(scenario_headers):
        try:
            years_cols.append(int(header))
        except ValueError:
            continue

    if not all(2005 <= y <= 2100 for y in years_cols):
        raise ValueError(
            f"One or several of the years provided in the scenario data file are "
            "out of boundaries (2005 - 2100)."
        )


    if len(pd.isnull(df).sum()[pd.isnull(df).sum() > 0]) > 0:
        raise ValueError(
            f"The following columns in the scenario data file"
            f"contains empty cells.\n{pd.isnull(df).sum()[pd.isnull(df).sum() > 0]}."
        )


    d_regions = {"remind": LIST_REMIND_REGIONS, "image": LIST_IMAGE_REGIONS}

    list_ei_locs = [
        i if isinstance(i, str) else i[-1]
        for i in list(Geomap(model="remind").geo.keys())
    ]

    for irow, r in df.iterrows():
        if (
                r["region"] not in d_regions[r["model"]]
                and r["region"] not in list_ei_locs
        ):
            raise ValueError(
                f"Region {r['region']} indicated "
                f"in row {irow} is not a valid region for model {r['model'].upper()}"
                f"and is not found within ecoinvent locations."
            )

    if not all(
            v in df["variables"].unique()
            for v in get_recursively(config_file, "variable")
    ):
        list_unfound_variables = [
            p
            for p in get_recursively(config_file, "variable")
            if p not in df["variables"].unique()
        ]

        raise ValueError(
            "The following variables from the configuration file "
            f"cannot be found in the scenario file: {list_unfound_variables}"
        )

    if not all(
            v in df["variables"].unique()
            for v in get_recursively(config_file, "variable")
    ):
        missing_variables = [
            v
            for v in get_recursively(config_file, "variable")
            if v not in df["variables"].unique()
        ]
        raise ValueError(
            f"One or several variable names in the configuration file "
            f"cannot be found in the scenario data file: {missing_variables}."
        )

    try:
        np.array_equal(df.iloc[:, 6:], df.iloc[:, 6:].astype(float))
    except ValueError as e:
        raise TypeError(
            f"All values provided in the time series must be numerical "
            f"in the scenario data file."
        ) from e



def get_recursively(search_dict, field):
    """Takes a dict with nested lists and dicts,
    and searches all dicts for a key of the field
    provided.
    """
    fields_found = []

    for key, value in search_dict.items():

        if key == field:
            fields_found.append(value)

        elif isinstance(value, dict):
            results = get_recursively(value, field)
            for result in results:
                fields_found.append(result)

        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    more_results = get_recursively(item, field)
                    for another_result in more_results:
                        fields_found.append(another_result)

    return fields_found
