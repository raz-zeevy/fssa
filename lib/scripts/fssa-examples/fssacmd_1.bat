@echo off

REM Set the paths for the files and executables
set "fss_path="..\fssa-21\FASSA.BAT"
set "dat_path=DJKEDAR2.DAT"
set "drv_path=FSSAINP.DRV"
set "out_fss_path=DJkedar2.FSS"
set "out_mat_path=MONOASC.MA"

REM Call the FASSA.BAT script with the specified parameters
call "%fss_path%" MONO MONOINP.DRV "%dat_path%" NUL MONOASC.MAT "%drv_path%" "%out_mat_path%" "%out_fss_path%"

REM The 'call' command is used to run another batch file from a batch file