[![Build Status](https://github.com/materialscloud-org/structure-property-visualizer/workflows/ci/badge.svg)](https://github.com/materialscloud-org/structure-property-visualizer/actions)

# Structure-Property-Visualizer

Use this app to generate interactive visualizations like [these](https://www.materialscloud.org/discover/cofs#mcloudHeader)
for atomic structures and their properties.

## Features

 * interactive scatter plots via [bokeh server](https://bokeh.pydata.org/en/1.0.4/)
 * interactive structure visualization via [jsmol](https://chemapps.stolaf.edu/jmol/docs/)
 * simple input: provide CIF/XYZ files with structures and CSV file with their properties
 * simple deployment on [materialscloud.org](https://www.materialscloud.org/discover/menu) through [Docker containers](http://docker.com)
 * driven by database backend:
   1. [sqlite](https://www.sqlite.org/index.html) database (default)
   1. [AiiDA](http://www.aiida.net/) database backend (requires customization)

## Getting started

### Prerequisites

 * [git](https://git-scm.com/)
 * [python](https://www.python.org/)
 * [nodejs](https://nodejs.org/en/) >= 6

### Installation

```
git clone https://github.com/materialscloud-org/structure-property-visualizer.git
cd structure-property-visualizer
pip install -e .     # install python dependencies
./prepare.sh         # download test data (run only once)
```

### Running the app

```
export PYTHONPATH="${PYTHONPATH}:/path/to/structure-property-visualizer"  # export pythonpath
bokeh serve --show figure detail select-figure   # run app
```

## Customizing the app

### Input data
 * a set of structures in `data/structures`
   * Allowed file extensions: `cif`, `xyz`
 * a CSV file `data/properties.csv` with their properties
   * has a column `name` whose value `<name>` links each row to a file in `structures/<name>.<extension>`.
 * adapt `import_db.py` accordingly and run it to create the database

### Plots

The plots can be configured using a few YAML files in `figure/static`:
 * `columns.yml`: defines metadata for columns of CSV file
 * `filters.yml`: defines filters available in plot
 * `presets.yml`: defines presets for axis + filter settings

### AiiDA support

Instead of querying an sqlite database, you can also query an AiiDA database.
In order to keep the docker image size manageable, it is best to keep the AiiDA profile *outside* the image and to

 1. communicate the docker container how to connect to the AiiDA database
 2. mount the AiiDA file repository inside the docker container

For the first step you already find a couple of (commented) variables in the `Dockerfile`, as well a python function `figure.aiida.load_profile` to load an AiiDA profile environment from these variables.

For the second step, modify the `docker-compose.yml` to mount the AiiDA file repository instead of the `data/` directory.

## Docker deployment

```
pip install -e .
./prepare.sh
docker-compose build
docker-compose up
# open http://localhost:3245/select-figure
```
