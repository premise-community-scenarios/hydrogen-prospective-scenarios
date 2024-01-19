from datapackage import Package
import pandas as pd
import yaml

FILEPATH_DATAPACKAGE_SCHEMA = "./datapackage.json"

def test_datapackage():
    dp = Package(FILEPATH_DATAPACKAGE_SCHEMA)
    assert dp.descriptor["profile"] == "data-package"
    assert len(dp.resources) >= 2

    mandatory_keys = [
        'profile',
        'name',
        'title',
        'description',
        'version',
        'contributors',
        'dependencies',
        'ecoinvent',
        'scenarios',
        'licenses',
        'resources'
    ]

    assert all(i in dp.descriptor for i in mandatory_keys), f"One of the mandatory" \
                                                            f"descriptor fields in the" \
                                                            f"datapackage file is missing. " \
                                                            f"It must contain the following fields {mandatory_keys}"

    for resource in dp.resources:
        if resource.name == "config":
            resource = dp.get_resource("config")
            config_file = yaml.safe_load(resource.raw_read())
            assert isinstance(config_file, dict)

        if resource.name == "scenario_data":
            assert pd.read_csv(resource.descriptor["path"]).shape != (0, 0)

