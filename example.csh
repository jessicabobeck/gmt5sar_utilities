#Example command to run files from .csh/.sh script in terminal

#linking base line tbale
ln -s raw/baseline_table.dat .
#makeInputFiles.py table master algorithm threshold
python makeInputFiles.py baseline_table.dat IMG-HH-ALPSRP052541220-H1.0__A ALOS baseline 10000
