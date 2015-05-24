# BLS This script will read BLS .csv data and save a polar bar chart (current.png) that 
represent the percentage of total employment (width of the pie slice) as well as the 
average salary of each position (length of the pie slice). This script works well with 
the BLS data file included here (/owenmwilliams/BLS/bls.csv). Note that this data is 
several years out of date and the script has yet to be tested with new data. There are 
two variables that should be selected: the occupations to be compared and the states and
territories to compare. The script will then generate your graph (as current.png) as well
as an "Other" graph that contains all of the occupations with a lower percentage 
(current_other.png). These pictures will be written over if the script is run again.
