# NOZAMA DATABASE README

## Using the Scripts
This directory includes a number of python scripts that are meant to easily, predictably, and programmatically generate large amounts of data to fill out a large website.
These scripts are intended to be "safe"; any can be run without breaking the database. For best results, run the scripts in this order: first Account, then Product, then Orders, then CartSaved, then Review. In their opperative functions, these scripts read to and write from multiple CSV files, for instance, the generateReview script makes Review, ReviewVote, ReviewImage, SellerReview, and ProductReview data an once that is meant to complement each other. 

The `generate.py` unifies the others in the order described above. It is a shortcut to and identical to running these scripts sequentially. The amount of data generated can be tweaked in the scripts, and the raw combinatorial materials used to generate the data is easily editable in the respective scripts.
To run a python script in terminal use command `python [scriptname.py]` 

PLEASE DO NOT PUSH NEW DATA TO GIT. The base data is sufficient, we can all generated data on our own.


## Using the SQL
Run `./setup.sh` in your machine to create the SQL database. To get more data, generate with the scripts before doing this.


## Troubleshooting
1. Be sure the uuid pip package is installed on your machine or VM
