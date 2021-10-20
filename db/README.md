# NOZAMA DATABASE README

## Using the Scripts
This directory includes a number of python scripts that are meant to easily, predictably, and programmatically generate large amounts of data to fill out a large website.
These scripts are intended to be "safe"; any can be run without breaking the database. This is done by reading existing data and
creating new data relative to that. Because of this, for best results, run the scripts in this order: first Account, then Product, then Orders, then CartSaved, then Review. In their opperative functions, these scripts read to and write from multiple CSV files, for instance, the generateReview script makes Review, ReviewVote, ReviewImage, SellerReview, and ProductReview data an once that is meant to complement each other. 

The `generate.py` unifies the others in the order described above. It is a shortcut to and identical to running these scripts sequentially. The amount of data generated can be tweaked in the scripts, and the raw combinatorial materials used to generate the data is easily editable in the respective scripts.
To run a python script in terminal use command `python [scriptname.py]`

PLEASE DO NOT PUSH NEW DATA TO GIT. The base data is sufficient, we can all generated data on our own.


## Using the SQL
Run `./setup.sh` in your machine to create the SQL database. To get more data, generate with the scripts before doing this.


## Troubleshooting
1. Be sure the uuid pip package is installed on your machine or VM
2. The CSV files must NOT end in newlines. This is counter to common dialetcs of CSV but PSQL cannot parse the newlines.


## TO-DOs
1. Refactor for more universal pattern across scripts
2. Refactor to reduce repetative reading of CSVs across scripts
3. Refactor to add easier, more centralized access to raw data material


### author: luke evans