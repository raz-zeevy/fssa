             F A C E T E D   S S A   f o r   W i n d o w s[FSSAWIN]

FSSAWIN and POSAC/LSA are experimental programs developed as part of ongoing research in Facet Theory.
They are provided only free of charge for non-commercial academic research and teaching purposes.

This version of Faceted SSA (ver 1.0 for windows, 1997)
has new features enabling the researcher to test a lot
of different ideas easily. The main new features are the
ability to navigate freely within the fssa running form and
the ability to "choose out" variables, i.e., to ignore them
in the calculation.

This document supplies installation instructions. For details about
the software targets, new features and operation please refer to
the on-line help. 

FSSA for Windows runs on Windows 3.1 and up (Win 95 included), which usually 
means minimal hardware requirements of a 80386 CPU and 4MB memory, and
DOS version 5.x or later. Any computer which runs Windows should be
enough to run FSSA for Windows.

Resident programs you may have in your computer may have to be
deactivated before running the program. In particular, certain commands in
the autoexec.bat and config.sys files may have to be deactivated in order to
load FSSA program.

Certain parts of the program require that you have CONFIG.SYS file in your 
root directory containing the following commands (see DOS manual):

BUFFERS=15
FILES=20


INSTALLATION: 

1. In Windows 3.x

To install FSSA in windows 3.x, place the diskette in a disk drive, and run the 
installation program. To do that, in the Program Manager, select
"Run" from the "File" menu, and in the "command line" box, type
"A:\setup.exe" (assuming A is your floppy drive letter).

The installation program will guide you through the installation,
and, after installing the program files, will create a Windows
program group for you. To start the program, double-click the
program icon in the group.

To undo the installation, delete the program directory, the program
group, and the file "fssawin.ini" in your Windows directory.

2. In Windows 95

To install FSSA in Windows 95, place the diskette in a disk drive, and run the 
installation program. To do that, select "Run" from the "Start" menu,
and in the "command line" box, type "A:\setup.exe" (assuming A is your
floppy drive letter).

The installation program will guide you through the installation,
and, after installing the program files, will create a program group 
sub-submenu in the Programs submenu for you. To start the program, select the
program icon in the submenu.

To undo the installation, delete the program directory, the file 
"fssawin.ini" in your Windows directory, and edit the Task menu
to delete the program group.

****

FSSA output files have long lines. Use the DOS command

> MODE LPT1:132,8

if you intend to print out FSSA output on a narrow (9") paper.

****


Faceted SSA program maps objects in a space of
prespecified dimensionality so as to represent pairwise similarity or
dissimilarity observed between them. The (dis)similarity coefficients
may be an existing symmetric matrix written as an ASCII file,
having a fixed format; or, in case the objects are variables, a matrix of
statistical coefficients may be created by the program itself from a data file.

CASE I: Matrix Material. Before you start FSSA you must verify that the
(dis)similarity matrix you wish to analyze is indeed in your computer and 
that you know--

-The name of the matrix file, and its full path (e.g. \mydir\simil.mat);

- How many objects (e.g. variables) are referred to by that matrix;

- In what format is the matrix written in the file. I.e.,
        - the number of fields in each (physical) row. (This may be 
          smaller than the number of objects if rows wrap);
        - the number of columns in each field;
        - the number of decimal places used.

- Whether coefficients represent pairwise similarity between objects
  (correlations, confusion coefficients, judged similarity) or pairwise
  dissimilarity (distance);

- What values are to be considered as missing values in the matrix.

CASE II: Data. Before you start FSSA you must verify that the data set
you wish to analyze is indeed in your computer in an ASCII file of fixed
format, that it has been recoded (using a statistical package or your editor)
in accordance with FSSA purposes and requirements (see 'About Faceted SSA'
below or info screens within the program), and that you know--

- The name of the data file, and its full path (e.g. A:\mydir\recod.dat);

- How many records per case are there in the data file;

- In which record and column(s) is each of the variables you wish to 
  include in the analysis, located;

- What are the valid values (and the missing values) for each variable.

IN BOTH CASES, you may skip the facet option and run a simple SSA: Just 
specify "no facets" for the number of facets.

In order to use the facet option, you should have a substantive (content)
criterion--one or more--for classifying the variables.
FSSA allows you to examine the empirical validity of such criteria in terms
of patterns of partitions of the resulting space.


Default responses are offered to most questions. 

By default, FSSA results are written on file FSSA.RES, thereby erasing
the previously saved file with this name. You may change the names of
these results files, and direct to other directories, or direct it to 
printer by entering PRN.

 
      On running FSSAWIN featuring REGIONAL HYPOTHESIS testing 
      ==============================================================

      Optionally, you can explore or test hypotheses of the fit of the SSA
      solution to specific patterns of space partitioning (axial, angular,
      radial). Given a content facet (i.e. a classification of the items),
      the program searches for the best axial partition, the best angular
      partition and the best radial partition, of the 2-dimensional SSA 
      solution, that correspons to that facet. The results are partitioned 
      facet diagrams each with a SEPARATION INDEX that indicates how well the
      obtained partition corresponds to the pre-conceived facet. The 
      partitioned facet diagrams are created in the form of graphic screen
      diagrams.

                                  MSHERC.COM

      Users of Hercules or "Hercules-compatible" graphics cards must 
      run the program MSHERC.COM (or put the MSHERC instruction in their 
      AUTOEXEC.BAT file) before running either of the graphics programs 
      FSSA or DISSCRN.
  

      
                   Use of the font files COURB.FON, TMSRB.FON


      The font files COURB.FON, TMSRB.FON have to be accessible to the two
      programs FWSSA and DISSCRN.  To ensure this, several options are available:

1.    The font files can be stored in the default directory when the 
      program is run.


2.    If the font files are not in the default directory, the DOS environment 
      can be used to tell the program where to find it, using the 
      environment variable FONTDIR.  For example, if they are stored in 
      directory \fonts of drive c:, put the instruction 

      SET FONTDIR=C:\FONTS

      in the AUTOEXEC.BAT file in the root directory.


3.    As another possibility, if the environment variable FONTDIR is not 
      set, the font files can be stored in the same directory as the EXE 
      program file itself (FWSSA.EXE and DISSCRN.EXE).  However, this 
      solution is available only to users of DOS 3.0 or later versions, 
      and not to users of versions 2.x of DOS. 

       ********** INSPECTING, PRINTING AND TRANSPORTING ************
       ************** THE PARTITIONED FACET-DIAGRAMS ***************

      Besides a file with full FSSA results, the program produces also
      screen diagrams of the solution and of the facet diagrams.
      If requested, graphic facet diagrams with results of the  
      regional hypotheses testing (parallel lines, radii, circles) are
      shown as well. All these appear briefly while the program is 
      running. But they can be re-displayed for inspection.

      INSPECTING screen diagrams: After successful completion of the program,
      screen diagrams can be displayed for inspection by using the view
      menu.

      2D  

      in order to see the FSSA solution, with items identified by their 
      serial number. Enter

      2DF A  

      in order to see diagrams of Facet A. In this case the screen
      facet diagram is shown first, then, repeatedly pressing 'ENTER' key,
      the graphic diagrams of Facet A, testing the regional hypotheses,
      are displayed. Q MUST BE ENTERED TO QUIT THIS DISPLAY. Then Facets
      B C D --if they exist--may be similarly examined by entering 2DF B, etc.
     
      PRINTING the screen diagrams: It is recommended to print the screen
      diagrams immediately after each FSSA run, since they will be replaced
      in the next run. The non graphic (ASCII) diagrams may be printed by
      pressing  'Print Screen' while the diagram is shown on the screen.
      THE GRAPHIC DIAGRAMS ARE PRINTED BY ENTERING P, for dot matrix printers;
      or entering L, for HP laser printers, while the diagram is on the screen.
      The printing of the graphic diagrams can be slow.

      The names of the files containing the screen diagrams of a 2-dim
      solution are:

      SSA212.SCR (the solution itself with variables denoted by their
            serial ID number)
      FCA212.SCR (unpartitioned diagram of Facet A;  FCB212.SCR for Facet B; 
            FCC212.SCR for Facet C; FCD212.SCR for Facet D.)
      FCA212AX.SCR (The best AXial partition for facet A; FCB212AX.SCR 
            for Facet B etc.)
      FCA212AN.SCR (The best ANgular partition for facet A; FCB212AN.SCR 
            for Facet B etc.)
      FCA212RD.SCR (The best RaDial partition for facet A; FCB212RD.SCR 
            for Facet B etc.)
      
      A transportable file of a screen diagram (for use in WINDOWS. e.g.) 
      can be created by entering F while the diagram is shown on the screen. 
      The new transportable file will have the extension .PCX.

      If the resulting picture e.g. FCA212AN.PCX appears in inverse video,
      type (in DOS, in the appropriate directory:

      DISSCRN2 FCA212AN.SCR

      then, when the picture is on the screen, enter f. The PCX file 
      created now will have the opposite video colors of the default,
      (which uses DISSCRN command).
      If you want to save a screen diagram you must change its file name.
      For example the original name of the screen diagram displaying the
      test of the AXial role of Facet B is fcb212ax.scr. 
      
      (E.g. When in DOS enter 

      RENAME FCB212AX.SCR  <newname>.SCR

      Then the diagram may be displayed later on the screen by entering

      DISSCRN <newname>.SCR    or     DISSCRN2  <newname>.SCR
     
      The other screen diagram files of facet B,

      FCB212AN.SCR, FCB212RD.SCR

      can be similarly treated.)


                       About Faceted SSA
                      ====================  

  Faceted Smallest Space Analysis (FSSA) is a Multidimensional Scaling        
  (MDS) procedure which optionally allows for the incorporation of            
  content classifications (=facets) of the mapped objects into the            
  analysis, and testing their validity.                                                                   
                                                                              
  FSSA maps objects (most often the "objects" are observed variables)         
  in a space of prespecified dimensionality, so as to represent pairwise      
  similarity or dissimilarity observed between them. The (dis)similarity      
  measures -- or coefficients -- are created in advance by a statistical      
  package or are otherwise conceived and written into a file (e.g., using your    
  editor). Coefficients should be in the form of a symmetric matrix           
  written into an ASCII file, having a fixed format. Optionally, FSSA         
  first computes a matrix of Pearson correlations or a matrix of              
  monotonicity coefficients from an appropriate data file (i.e. an ASCII      
  file where each variable is numerical, and ordered from HIGH to LOW        
  in some sense). Then FSSA goes on to processing the matrix --               
  interpreting its entries as similarity coefficients -- and to mapping       
  the variables in  2-dimensional projections of the requested spaces.        
  The full power of FSSA for scientific theory construction is attained       
  by identifying a correspondence between a content facet (i.e. a             
  classification of the variables) and a partition of the FSSA solution
  space into regions. This is facilitated by the program "facet option".      
                                                                             
                                                                             
  REFERENCES                                                                 
   Borg, I. and Shye, S. Facet Theory: Form and Content. Newbury Park
     California: Sage, 1995.                                                                          
   Guttman, L. A general nonmetric technique for finding the smallest         
     coordinate space for a configuration of points. PSYCHOMETRIKA, 1968.     
   Shye, S. (ed.) Theory Construction and Data Analysis in the Behavioral     
     Sciences. San Francisco: Jossey-Bass, 1978.                              
   Shye, S. Achievement motive: a faceted definition and structural analysis .
     MULTIVARIATE BEHAVIORAL RESEARCH, 1978.                                  
   Shye, S. Smallest Space Analysis. In T. Husen & T.N. Postlethwaite (eds.)  
     INTERNATIONAL ENCYCLOPEDIA OF EDUCATION. Oxford: Pergamon, 1985; 
     2nd edition, 1994.
   Shye, S. Facet Theory. In T. Husen & T.N. Postlethwaite (eds.)  
     INTERNATIONAL ENCYCLOPEDIA OF EDUCATION, 2nd EDITION. Oxford: Pergamon,
     1994. 
   Shye, S. Partial Order Scalogram Analysis. In T. Husen & T.N. Postlethwaite
     (eds.)  INTERNATIONAL ENCYCLOPEDIA OF EDUCATION. Oxford: Pergamon, 1985; 
     2nd edition, 1994.
   Shye, S. (In Press) Facet Theory. Encyclopedia of Statistical Sciences 
     (Update). New York: Wiley
   Shye, S. and Elizur, D. Introduction to Facet Theory. Newbury Park, 
     California: Sage, 1994.
                                                                              
 