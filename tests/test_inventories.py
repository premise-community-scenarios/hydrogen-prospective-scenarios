import yaml
import bw2io
from datapackage import Package

FILEPATH_DATAPACKAGE_SCHEMA = "./datapackage.json"
dp = Package(FILEPATH_DATAPACKAGE_SCHEMA)

if dp.get_resource("inventories"):
    i = bw2io.CSVImporter(dp.get_resource("inventories").source)

    resource = dp.get_resource("config")
    config_file = yaml.safe_load(resource.raw_read())

def test_length():
    if dp.get_resource("inventories"):
        assert len(i.data) > 0


def test_inventories():
    if dp.get_resource("inventories"):
        for k, v in config_file["production pathways"].items():

            name = v["ecoinvent alias"]["name"]
            ref = v["ecoinvent alias"]["reference product"]

            if (
                len(
                    [
                        a
                        for a in i.data
                        if (name, ref) == (a["name"], a["reference product"])
                    ]
                )
                == 0
            ) and not v["ecoinvent alias"].get("exists in original database")\
                    and not v["ecoinvent alias"].get("new dataset"):
                raise ValueError(
                    f"The inventories provided do not contain the activity: {name, ref}"
                )

