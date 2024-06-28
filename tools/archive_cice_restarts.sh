#!/bin/bash
# clean up cice_restarts.sh
# this will clear out all the restarts that payu hasn't moved, so if you want extra for some reason, modify this script

r_files=(archive/output*/access-om3.cice.r.*)

if [ -f ${r_files[0]} ]
then
rm archive/output*/access-om3.cice.r.*
fi

if [ -f archive/output*/input/iced.1900-01-01-10800.nc ] 
then
rm archive/output*/input/iced.1900-01-01-10800.nc
fi
