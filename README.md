# toronto-parking-tickets
# WORK IN PROGRESS

## Overview

The City of Toronto has published all parking tickets issued in the last 9 years, available through their [Open Data Portal](http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=ca20256c54ea4310VgnVCM1000003dd60f89RCRD). This repo houses the cleaning & analysis of this data. An interactive visualization was created to show a map-based view of the highest grossing areas in Toronto. This project was completed as part of the Udacity Data Analyst Nanodegree.

## Data
The parking ticket data comes in spreadsheets, ranging from 1-4 spreadsheets per year.

The [main.py](https://github.com/ian-whitestone/toronto-parking-tickets/blob/master/data/main.py) loads the data from the spreadsheets into a PostgreSQL database hosted on an AWS RDS instance.

### Data ETL Process
To clean and transform the data from the excel to the format required by the Postgres database, I created a `FIELD_MAP` parameter in `config.py` which defines the field name in the excel file and which function should be used to validate/transform the field.

Each field in `FIELD_MAP` maps to a destination column in the Postgres database (see [schema](https://github.com/ian-whitestone/toronto-parking-tickets/blob/master/data/analysis/queries.sql)). Right now the mapping is order based (i.e. the first field `date` maps to the first column in the `tickets` table and so on).

```python

FIELD_MAP = [
    {'name':'date', 'func':'do_none'},
    {'name':'time_of_infraction', 'func':'check_int'},
    {'name':'infraction_code', 'func':'check_int'},
    {'name':'infraction_description', 'func':'check_text'},
    {'name':'set_fine_amount', 'func':'check_int'},
    {'name':'location1', 'func':'check_varchar', 'length': 10},
    {'name':'location2', 'func':'check_varchar', 'length': 50},
    {'name':'province', 'func':'check_varchar', 'length': 5}
]
```

The functions referenced in the `FIELD_MAP` are housed in the `DataCleaning.py` module. Using the `getattr()` Python function, the functions can be called from their string names.

```python
fields = []
for field in config.FIELD_MAP:
    val = record.get(field['name'], None)
    if val:
        cleaned_val = getattr(DataCleaning, field['func'])(val=val,
                        length=field.get('length',0))
    else:
        cleaned_val = None
    fields.append(cleaned_val)
```

### Analysis
Summary of top parking spots coming soon....

## Visualization

### Design Overview

-- A reader’s summary of the graphic would closely match the written summary in the README.md file, or a reader would identify at least 1 main point or relationship that the graphic attempts to convey.
-- Initial design decisions such as chart type, visual encodings, layout, legends, or hierarchy are included at the beginning of the Design section in the README.md file.

### Initial Design

### Feedback
include all feedback you received from others on your visualization from the first sketch to the final visualization

1) Initial map background
2) Legend? adding infraction codes and descriptions in a legend
3) bootstrap to support multiple devices / dynamic sizing of the chart
4) add instructions!
5) filtering infraction types


### Final Design
explain any design choices you made including changes to the visualization after collecting feedback


### Resources

The visualization was created using D3.js. The following resources were used to create the visualization:

1) [Zoomable Map Tiles](http://bl.ocks.org/mbostock/4132797)
2) [D3 Tips](http://bl.ocks.org/Caged/6476579)
3) [Google Maps Streetview](https://developers.google.com/maps/documentation/javascript/examples/streetview-simple)
