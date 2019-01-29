____
### Introduction

Atmospheric correction of Sentinel 2 imagery in Google Earth Engine using [Py6S](http://py6s.readthedocs.io/en/latest/).

### Installation
Create a conda environment based on the environment variable here: ""

By running all notebooks in this environment/kernel, all the package prerequisites will be met. 

### Usage

Before beginning, authenticate Earth Engine in the terminal with the following command:

`earthengine authenticate`

Next, activate your environment by using the command:

`conda activate *yourenvironmentname*`

Finally, start jupyter notebook and navigate to the notebooks here. Use the command:

`jupyter-notebook`

### References
For the atmospheric correction, functions were sourced from Sam Murphy's repository (link below)

[Py6S Atmospheric Correction](https://github.com/samsammurphy/gee-atmcorr-S2)

For cloud masking, GEEtools and S2Cloudless the following repositories were used:

- [GEE-Tools](https://github.com/gee-community/gee_tools)
- [S2Cloudless](https://github.com/sentinel-hub/sentinel2-cloud-detector) 
