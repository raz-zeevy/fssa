ECHO OFF
ECHO  ÿ
ECHO             *******************************************************
ECHO             *                                                     *
ECHO             *              F A C E T E D    S S A                 *
ECHO             *                                                     *
ECHO             *******************************************************
ECHO  ÿ
IF %1X==MONOX GOTO MONO
IF %1X==monoX GOTO MONO
IF %1X==PEARSONX GOTO PEARSON
IF %1X==pearsonX GOTO PEARSON
GOTO WSSA
:PEARSON
ECHO  ÿ
ECHO      Computing Pearson correlations
ECHO  ÿ
REM ********** BEGIN PROGRAM PEARSON **************
PEACORMS %2 %3 %4 %5
IF ERRORLEVEL 2 GOTO fail
GOTO DOSHIFT
:MONO
ECHO  ÿ
ECHO       Computing  monotonicity  coefficients
ECHO  ÿ
REM ********** BEGIN PROGRAM NEWMON ****************
NEWMONMS %2 %3 %4 %5
IF ERRORLEVEL 2 GOTO fail
:DOSHIFT
SHIFT
SHIFT
SHIFT
SHIFT
SHIFT
:WSSA
IF %3X==PRNX  GOTO SETPRN
IF %3X==prnX  GOTO SETPRN
GOTO DOPROG
:SETPRN
REM ********** BEGIN PRINTER SETTING **************
ECHO PLEASE SCROLL PAPER IN PRINTER TO TOP OF PAGE
PAUSE
TYPE \SETPRNTR.COD>PRN
TIMEMARK>PRN
:DOPROG
ECHO  ÿ
ECHO       Running  Faceted  SSA
ECHO  ÿ
REM ********** BEGIN PROGRAM WSSA1 ****************
FWSSA  %1 %2 %3
IF ERRORLEVEL 2 GOTO fail
ECHO     Enter 2D or 3D to view FSSA screen diagrams in 2 or 3 dimensions.
ECHO     Enter 2DF A (or 2DF B) to view 2-dimensional diagram with facet A (B),
ECHO     etc. 
:fail
