# gmt5sar_utilities

### makeInputFiles.py

Utility for creating align.in and intf.in files.

##### IN:

	`table` - baselline_table.dat file (found in raw dir)
	
	`master` - name of master or super master that image will align too
	
	`sat` - satellite (ALOS, ENVI, ERS) *Note: Only ALOS is working presently*
	
	`algorithm` - all: every possible combination (least selective)
	
                 baseline: pairs matched by baseline theshold (moderatly selective)
		 
                 leapfrog: GMT5SAR recommended algorithm that splits pairs up into primary, secondary and tertiary pairs (highly selective)
     
	threshold - threshold for small baseline subsets, set to 0 if you do not want a  threshold.
                  It will separate out subgroups based on your threshhold and create all possible
                  combinations for that subset.
	

##### OUT:
	`intf.in`
	
	`align.in`

USAGE:

	Use from command line.It can be put in a .csh or .sh file. For example:

	#linking table.gmt file
		ln -s raw/baseline_table.dat .
	#making align.in
		python makeInputFiles.py baseline_table.dat IMG-HH-ALPSRP052541220-H1.0__A 10000 ALOS baseline prim_base=10000
	#running align script
		align_batch.csh ALOS align.in
	#running intf script
		intf_batch.csh ALOS intf.in intf.config
