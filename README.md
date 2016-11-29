# gmt5sar_utilities
----------------------------------------------------------------------------------------------------------------------------------------
### makeInputFiles.py

Utility for creating align.in and intf.in files. You can also type -h or --help in the command line

##### IN:
###### REQUIRED:
`table` - baselline_table.dat file (found in raw dir)
	
`master` - name of master or super master that image will align too
	
`sat` - satellite (ALOS, ENVI, ERS) *Note: Only ALOS is working presently*
	
`algorithm` - 
+ all: every possible combination (least selective)
+ baseline: pairs matched by baseline theshold (moderatly selective) 
+ leapfrog: GMT5SAR recommended algorithm that splits pairs up into primary, secondary and tertiary pairs (highly selective)
     
`prim_base` - Baseline Threshold. Default=800 [m]. (Primary Baseline threshold for leap frog algorithm)

###### FLAGS:	
`--py` - Primary Year Threshold. Default=2 [y]. Required for leapfrog algorithm only.

`--sb`- Secondary Year Threshold. Default=1500 [m]. Required for leapfrog algorithm only.

`--sy` - Secondary Year Threshold. Default=2 [y]. Required for leapfrog algorithm only.

`--tb` - Tertiary Baseline Threshold. Default=5000 [m] Required for leapfrog algorithm only.

`--ty` - Tertiary Year Threshold. Default=1 [y]. Required for leapfrog algorithm only.

##### OUT:
`intf.in` - formatted intf.in file for intf_batch.csh
	
`align.in` - formated align.in file for align_batch.csh

`[algorithm]Pairs.png` - Plot of all the pairs and ids.
##### USAGE:

Use from command line.It can be put in a .csh or .sh file (also see `example.csh`). For example:
```bash
#linking table.gmt file

	ln -s raw/baseline_table.dat .

#making align.in

	#baseline algorithm
	python makeInputFiles.py baseline_table.dat IMG-HH-ALPSRP052541220-H1.0__A ALOS baseline prim_base=10000
	
	#leapfrog algorithm
	python makeInputFiles.py baseline_table.dat IMG-HH-ALPSRP052541220-H1.0__A ALOS leapfrog prim_base=10000 --py 2 --sb 15000 --sy 2 --tb 50000 --ty 3
	
	#all algorithm
	python makeInputFiles.py baseline_table.dat IMG-HH-ALPSRP052541220-H1.0__A ALOS all prim_base=10000

#running align script

	align_batch.csh ALOS align.in

#running intf script

	intf_batch.csh ALOS intf.in intf.config
```
----------------------------------------------------------------------------------------------------------------------------------------
