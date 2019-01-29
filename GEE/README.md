____
### Introduction

Atmospheric correction of Sentinel 2 imagery in Google Earth Engine using [Py6S](http://py6s.readthedocs.io/en/latest/).

### Installation
Before running, Anaconda needs to be installed on your system. Go [here](https://www.anaconda.com/download/) to download the latest version, and install by following the instructions on the site.

Verify your installation by running

`conda --version`

Once you've got conda working, create a new environment to suit the requirements of the notebooks here. To do that, run the following command in your terminal

`conda env create -f environment.yml`

This will set up an environment/kernel with all the suitable package versions for the notebooks here.

### Usage

Before beginning, authenticate Earth Engine in the terminal with the following command:

`earthengine authenticate`

Next, activate your environment by using the command:

`conda activate geepy6s-env`

Finally, start jupyter notebook and navigate to the notebooks here. Use the command:

`jupyter-notebook`

### References
For the atmospheric correction, functions were sourced from Sam Murphy's repository (link below)

[Py6S Atmospheric Correction](https://github.com/samsammurphy/gee-atmcorr-S2)

For cloud masking, GEEtools and S2Cloudless the following repositories were used:

- [GEE-Tools](https://github.com/gee-community/gee_tools)
- [S2Cloudless](https://github.com/sentinel-hub/sentinel2-cloud-detector)
