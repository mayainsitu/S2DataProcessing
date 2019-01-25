# S2DataProcessing

## Goal of this repository:
- Atmospheric correction and cloud removal of Sentinel L1C images to create L2A products. (*Complete!*)
- Monthly composites of cloud-free L2A products (*In Progress*)
- Time series analysis of pixels from the monthly composites (study site VS similar pixels nearby -- *In Progress*) 

Separate notebooks for each goal? And separate environments?

## Prerequisites
### Sentinel Hub Account
A Sentinel Hub account is required - you can apply for a free non-commercial account, or register for a 1 month trial.
Submit proposal for free account here: https://earth.esa.int/web/guest/pi-community/apply-for-data/ao-s?IFRAME_SRC=%2Fpi%2Fesa%3Fcmd%3Daodetail%26aoname%3DOSEO%26displayMode%3Dcenter%26targetIFramePage%3D%252Fweb%252Fguest%252Fpi-community%252Fapply-for-data%252Fao-s

Once you have an account, go to the "Configuration Utility" app and log in.

Add new configuration in the Configuration Utility. Set whatever name for it you like, but from the dropdown menu "Create configuration based on:" select "Python scripts template".

From your new configuration, make a note of the "ID" - this will be required in the Jupyter Notebook  for the data requests from Sentinel Hub.

## Initial setup
1. Install Anaconda if not already on your system
2. Create a new conda environment
3. Install correct package versions into the conda environment (listed in file "requirements.txt")

I want to create a bash script that when run will do this setup automatically on your local machine, perform the above steps and make sure the setup is done correctly for this notebook - but I still need to create this.

To add the environment as a kernel in jupyter, first install ipykernel in the environment, then run the following command: 
*python -m ipykernel install --user --name=<insert_name_assigned>* 

## Running the notebook
To run the Jupyter Notebook, first go to your terminal/commandline and enter:

*jupyter notebook*

This will launch jupyter in your browser, and you can play with the script from there
