____
### Introduction

Atmospheric correction of Sentinel 2 imagery in Google Earth Engine using [Py6S](http://py6s.readthedocs.io/en/latest/).

### Installation
This repo has the following prerequisites

- [Python 3.x](https://www.python.org/downloads/)
- [Google Earth Engine Python API](https://developers.google.com/earth-engine/python_install_manual)
- [Jupyter](http://jupyter.readthedocs.io/en/latest/install.html)
- [Py6S](http://py6s.readthedocs.io/en/latest/installation.html)

These are all bundled in the environment variable here. Create a conda environment based on these requirements. 

### Usage

Before beginning, authenticate Earth Engine in the terminal with the following command:

`earthengine authenticate`

Next, activate your environment by using the command:

`conda activate *yourenvironmentname*`

Finally, start jupyter notebook and navigate to the notebooks here. Use the command:

`jupyter-notebook`

### References
For the atmospheric correction, functions were sourced from Sam Murphy's repository (link below)
`git clone https://github.com/samsammurphy/gee-atmcorr-S2`
For cloud masking, GEEtools and S2Cloudless were used:
`https://github.com/gee-community/gee_tools` 
`https://github.com/sentinel-hub/sentinel2-cloud-detector` 
