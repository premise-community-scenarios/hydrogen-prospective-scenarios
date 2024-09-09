# hydrogen-prospective-scenarios

Hydrogen Prospective Scenarios

Description
-----------
This datapackage implements technologies and market shares for future hydrogen production, 
on the basis on IEA projections (STEPS, APS and NZE scenarios), combined with
the projections of global models such as REMIND.

.. note::
    If combined with a global IAM scenario, select REMIND as the IAM model.

Sourced from publication
------------------------

*Future environmental impacts of global hydrogen production.*
Shijie Wei, Romain Sacchi, Arnold Tukker, Sangwon Suh, and Bernhard Steubing.
Energy Environ. Sci. (2024) doi:[10.1039/D3EE03875K](https://pubs.rsc.org/en/content/articlelanding/2024/ee/d3ee03875k)


Ecoinvent database compatibility
--------------------------------

ecoinvent 3.9 cut-off

IAM scenario compatibility
---------------------------

The following coupling is done between IAM scenarios and the hydrogen market scenarios from the IEA:

| IAM scenario           | IEA scenario | Scenario          |
|------------------------|--------------|-------------------|
| REMIND SSP2-NDC        | SPS          | Business As Usual |
| REMIND SSP2-PkBudg1150 | APS          | Ambitious         |
| REMIND SSP1-PkBudg500  | NZE          | Very ambitious    |

More details on the mapping between the IAM variables and the IEA hydrogen scenarios are available
in the mapping `IAM-IEA.xlsx` file, under `others/hydrogen market`.

What does this do?
------------------


Hydrogen
********

The following market is introduced for each region in the IAM scenarios:

* `market for hydrogen, gaseous (IEA)`

And the following technologies feed into it:

* Hydrogen, from coal gasification
* Hydrogen, from coal gasification, with CCS
* Hydrogen, from natural gas (SMR)
* Hydrogen, from natural gas (SMR), with CCS
* Hydrogen, from biomethane (SMR)
* Hydrogen, from biomethane (SMR), with CCS
* Hydrogen, from electrolysis (Alkaline)
* Hydrogen, from electrolysis (Proton Exchange Membrane)
* Hydrogen, from electrolysis (Solid Oxide)


Flow diagram
------------


How to use it?
--------------

```python

    import brightway2 as bw
    from premise import NewDatabase
    from datapackage import Package
    
    
    fp = r"https://raw.githubusercontent.com/premise-community-scenarios/hydrogen-prospective-scenarios/main/datapackage.json"
    hydrogen = Package(fp)
    
    bw.projects.set_current("your_bw_project")
    
    ndb = NewDatabase(
            scenarios = [
                {"model":"remind", "pathway":"SSP2-Base", "year":2050, "external scenarios": [{"scenario": "Business as usual", "data": hydrogen}]},
                {"model":"remind", "pathway":"SSP2-NPi", "year":2030, "external scenarios": [{"scenario": "Ambitious", "data": hydrogen}]},
                {"model":"remind", "pathway":"SSP1-PkBudg500", "year":2020, "external scenarios": [{"scenario": "Very ambitious", "data": hydrogen}]},
            ],        
            source_db="ecoinvent 3.9.1 cutoff",
            source_version="3.9",
            key='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        )

    ndb.update("external") # or ndb.update() if you want to update the database with the IAM data plus the external scenario
```

