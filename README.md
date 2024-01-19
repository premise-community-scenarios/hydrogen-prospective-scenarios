# hydrogen-prospective-scenarios

Hydrogen Prospective Scenarios

Description
-----------
This datapackage implements technologies and market shares for future hydrogen production, 
on the basis on IEA projections (STEPS, APS and NZE scenarios), combined with
the projections of global models such as REMIND.

Sourced from publication
------------------------

*Future environmental impacts of global hydrogen production (in review).*
Shijie Wei, Romain Sacchi, Arnold Tukker, Sangwon Suh, and Bernhard Steubing.
DOI to come.


Ecoinvent database compatibility
--------------------------------

ecoinvent 3.9 cut-off

IAM scenario compatibility
---------------------------

The following coupling is done between IAM scenarios and the hydrogen market scenarios (APS):

| IAM scenario           | IEA scenario for H2 | Scenario                |
|------------------------|---------------------|-------------------------|
| IMAGE SSP1-Base        | STEPS               | Business As Usual       |
| IMAGE SSP1-RCP19       | NZE                 | Sustainable development |
| IMAGE SSP2-Base        | STEPS               | Business As Usual       |
| IMAGE SSP2-RCP19       | NZE                 | Sustainable development |
| REMIND SSP2-NDC        | APS                 | Sustainable development |
| REMIND SSP2-PkBudg1150 | APS                 | Sustainable development |
| REMIND SSP1-PkBudg500  | NZE                 | Sustainable development |

What does this do?
------------------


Hydrogen
********

The following market is introduced:

* `market for hydrogen, electrolysis (APS)`

It is supplied by two hydrogen production pathways:
* AE (alkaline electrolysis), and 
* PEM electrolysis

This market re-links to ammonia-producing activities 
that consume hydrogen throughout the database.


Flow diagram
------------


How to use it?
--------------

```python

    import brightway2 as bw
    from premise import NewDatabase
    from datapackage import Package
    
    
    fp = r"filepath to datapackage.json"
    hydrogen = Package(fp)
    
    bw.projects.set_current("your_bw_project")
    
    ndb = NewDatabase(
            scenarios = [
                {"model":"image", "pathway":"SSP2-Base", "year":2050,},
                {"model":"image", "pathway":"SSP2-RCP19", "year":2030,},
            ],        
            source_db="ecoinvent 3.8 cutoff",
            source_version="3.8",
            key='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
            external_scenarios=[
                hydrogen, # <-- list datapackages here
            ] 
        )
```

