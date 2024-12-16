WHAT_IS_FSSA_p1 = """Faceted Smallest Space Analysis (FSSA) is a Multidimensional Scaling (MDS) procedure which optionally allows for the incorporation of content classifications (=facets) of the mapped objects into the analysis.

FSSA maps objects (most often the "objects" are observed variables) in a space of prespecified dimensionality, so as to represent pairwise similarity or dissimilarity observed between them. The (dis)similarity measures -- or coefficients -- are created in advance by a statistical package or otherwise conceived and written into a file (e.g., using your editor). Coefficients should be in the form of a symmetric matrix written into an ASCII file, having a fixed format. Optionally, FSSA first computes a matrix of pearson correlations or a matrix of monotonicity coefficients from an appropriate data file (i.e. an ASCII file where each variable is numerical, and ordered from HIGH to LOW in some sense). Then FSSA goes on to processing the matrix -- interpreting its entries as similarity coefficients -- and to mapping the variables in 2-dimensional projections of the requested spaces.

Before you start FSSA you must verify that either the matrix file or the data file you wish to process is indeed in your computer. If you are going to process an existing matrix, you should know:
The name of the matrix file, and its full path (e.g. \mydir\simil.mat)
How many objects (e.g. variables) are referred to by that matrix
In what format is the matrix written in the file. I.e.,
The number of fields in each (physical) row. (This may be smaller than the number of objects if rows wrap;)
The number of columns in each field;
The number of decimal places used, if any.
Whether coefficients represent pairwise similarity between objects (correlations, confusion coefficients, judged similarity) or pairwise dissimilarity (distance).

If you are going to run a two-stage procedure, where a matrix is first computed from an existing data set, you should know:
The name of the data file, and its full path (e.g. \mydir\coded.dat) ;
How many records (lines) per subject are there in the data file;
How many variables are to be processed and where they are located in the data file; i.e. the record number and column(s) of each variable;
For each variable, what are its valid values (the range of numerical values over which correlations are computed) and what are its non- valid (including missing) values.

The full power of FSSA for scientific theory construction is attained by identifying a correspondence between a content facet (i.e. a classification of the variables) and a partition of the FSSA solution space into regions. This is facilitated by the program "facet option"."""

WHAT_IS_FSSA_p2 = """         Guttman, L. A general nonmetric technique for finding the smallest coordinate space for a configuration of points. PSYCHOMETRIKA, 1968.
         Lingoes, J.C. The Guttman-Lingoes Nonmetric Program Series. Ann Arbor: Mathesis, 1973.
         Shye, S. (ed.) Theory Construction and Data Analysis in the Behavioral Sciences. San Francisco: Jossey-Bass, 1978.
         Shye, S. Achievement motive: a faceted definition and structural analysis . MULTIVARIATE BEHAVIORAL RESEARCH, 1978.
         Shye, S. Smallest Space Analysis. In T. Husen & T.N. Postlethwaite (eds.) INTERNATIONAL ENCYCLOPEDIA OF EDUCATION. Oxford: Pergamon, 1985.
         Shye, S. Multiple Scaling. Amsterdam: North Holland. 1985.
         Borg, T. and Shye, S. Facet Theory: Form and Content. Thousand Oaks, CA: Sage, 1995.
         Shye, S. and Elizur, D. Introduction to Facet Theory. Thousand 
         Oaks, CA: Sage, 1994."""

USE_KEYBOARD_p1 = """There are a few tricks to using the keyboard, all except one of them standard to the Windows operating system.

The Tab key moves between fields on the screen; the Shift-Tab key combination moves backwards.

The field you are in is said to 'have the focus', and it will usually have a caret to show it. This caret's appearance differs by field (control) type. In an editable text field, it is usually a text cursor; in most other types (buttons, check-boxes, list-boxes) it is a dotted frame around a piece of text.

You can use the space-bar to push buttons or mark check-boxes, when they have the focus.

The Enter key may cause surprises to the unwary: In most screens and dialogs there is a 'default' button, marked by a thick black frame. If no button has the focus, the Enter key will push the default button. But if the dotted-frame caret is on another button, then Enter will press the button that has the focus.

The one exception to Windows standards is in the """

USE_KEYBOARD_p2 = """where selecting a combo-box element also moves you to the next field."""

RUN_COMMAND_p1 = """Use this command to run FSSA according to the form you have filled. FSSA for Windows will then do the following:

1. Check your form for correctness and consistency. If you have failed to supply some information that is needed for FSSA to run correctly, or filled a form that cannot be run, FSSA for Windows will indicate the error and bring you to the screen where you can correct it.

2. Check for old output files. FSSA for Windows places graphics (*.scr) output files in a fixed place, in the directory where it is installed. These files are created when you run a form. When you run another form, without taking measures against it, new files for the same processing will overwrite the old ones, and old files will remain in place where similar processing has not been requested; this may cause old output to be shown for new runs. To prevent this situation, FSSA for Windows offers to delete the old output files, if they exist. If you wish to keep them, you may at that point choose to cancel the run and move them to another directory (e.g. using the Windows File Manager). You may also choose to keep them where they are and run, which is not recommanded.

3. Ask for a job name and an output file name. The job name is an arbitrary string that will show up as a headline in the ouput file. The output file will contain the details of the run and analysis in DOS text form."""

EXIT_COMMAND_p1 = """Use this command to end your FSSA for Windows session. You can also use the Close command on the application Control menu. FSSA for Windows prompts you to save the current form."""

RECORDED_DATA_SCREEN_p1 = """In this screen you are required to define the general properties of your input file. The details of each variable are defined later in the """
RECORDED_DATA_SCREEN_p2 = """\n\n1. Specify path of data file. You can use the Browse 
button to open a file selection box"""
RECORDED_DATA_SCREEN_p3 = """ to help you find the right path. If the specified data file cannot be read, you will be notified upon finishing the screen (After the FSSA run has been successfully completed, the output file will be directed, by default, to the directory where the data file is).

2. Specify the number of rows (physical records) per case (logical record) in the data file specified above. This number can have a value from 1 to 10 and depends on how your data is set up.

3. If any of the variables have missing values other than zero, or if zero itself is not a missing value, choose 'No' in answer to the question. Otherwise, choose 'Yes'. Pressing the button switches between the two."""

NEW_FORM_DIALOG_BOX_p1 = """Specify the type of input file for the new form you wish to create:

The option of Coefficient Matrix processing enables you to run FSSA directly in a single stage. This selection assumes that a file containing the matrix in ASCII code exists in your computer. The path to that file (drive, directory, file name) must be known to you, as well as the exact (fixed) format of the matrix (the field width of each matrix entry, number of decimals, and whether lines are wrapped or not, i.e. the actual number of entries in each line of the file). If you are not sure about the format, you can use the View Input File command to check.

A matrix file may be created, before running FSSA, either by using your editor or by a statistical package using the saved results of a correlation command (e.g. SPSS.PRC).

The option of DATA processing results in a two stage operation: FSSA first produces a correlation matrix from an existing data file, and then the variables are mapped. The data file must exist in you computer and its path (drive, directory, file-name) and structure (records, columns and field-widths of the variables) known to you. Again, use View Input File to check the format.

A data file may be created, before running FSSA, either by using an editor or by a statistical package using the saved results of a write command (often after recoding and defining the missing values for raw data)"""

MANUAL_VARIABLES_SCREEN_p1 = """In this screen you can define variable labels and select variables for a run. If you are working with Recorded Data, you are also required to define the file structure (i.e. where in the file the variables data reside) in this screen.

The main attraction in this screen is a list box with a line for every variable. This list box is actually a table with the following columns:"""

DIMENSIONS_AND_COEFFS_SCREEN_p1 = """This screen reports the number of variables you have selected to work on, and offers the following fields:

Type of coefficients:

When working with Recorded Data, you can select between Monotonicity and Pearson. The coefficient of Monotonicity between two variables ranges from -1 to +1 and assesses to what extent an increase in one variable is accompanied by an increase (or no decrease) in the other variable, with no reference to an a priori regression line. Its absolute value is no smaller, and usually larger, than that of Pearson correlation. The coefficient of monotonicity is more appropriate for ordinal data, where no linearity is assumed for the regression line. Pearson correlation is the familiar linear correlation coefficient. Select either Monotonicity or Pearson, to suit your data and assumptions.

When working with a Coefficient Matrix, you can select between Similarity and Dissimilarity.Specify whether the matrix-entries represent similarity between the objects (e.g. correlation coefficients, indices of confusion, judged similarity) or dissimilarity between the objects (e.g., distance or indices of alienation).

Lowest dimensionality and Highest dimensionality specify the range of dimensionalities to be tested. Dimensionalities may be between 2 and 10 with the lower being less than or equal to the higher. If only one dimensionality is desired, for example, two-dimensional, enter that dimensionality in both fields (i.e. 2 and 2 in the example)."""

FACETS_DEFINITION_SCREEN_p1 = """A facet is a classification of the objects (variables) by some content criterion. One facet of psychological variables may, for example, classify those variables according to whether they refer to subjects' 'knowledge', 'love' or 'action'. A common facet of scholastic aptitude items classifies the items according to whether they assess verbal, spatial, or numerical ability. Each object may be classifiable independently by several facets. This program allows up to 4 facets to be chosen.

Each facet is a content-classification of the variables into classes, and so contains several FACET-ELEMENTS, each facet-element representing a class within that facet. Above the labels for facet-elements is their number, in each facet. The labels you assign to facet-elements of each facet will be used in output FSSA facet diagrams.

By default, there are 4 elements in each facet, labeled by facet letter and element number (i.e. facet A has 4 elements labeled a1,a2,a3,a4).

If you choose 'No facets', no facet analysis will be carried out at all, just Smallest Space Analysis (SSA), an MDS procedure. This is the default.
"""

VARIABLES_FACETS_SCREEN_p1 = """That the variables may be classified by a facet, means that each variable belongs to one of the facet's classes. I.e., each variable may be assigned a facet-element of that particular facet. Similarly, from each of the additional facets you may have defined, a facet-element can be assigned to the same variable. In this screen you are asked to classify each variable by Facet A (then by Facet B, if any, etc). In carrying out this task use the numerical designation of the appropriate facet-element.

You can use the mouse to open a combo-box of facet elements that you have defined, or select by a digit. Select 0 (Undefined) for a variable that has no classification in a particular facet.

Upon selection, the cursor will automatically move to the next variable; You do not need to move it yourself (by mouse or Tab key, as you usually do)."""

REGIONAL_HYPOTHESES_SCREEN_p1 = """In this screen you choose, for each 
facet, which regional hypotheses to test for it.

Mark the Axial check-box if you want to test the hypothesis that tha above mentioned facet is an AXIAL FACET. The program will then look for the set of PARALLEL LINES that best partition the space into strips according to that facet. The Separation Index will indicate agreement with the axial partition pattern.

Mark the Angular check-box if you want to test the hypothesis that the above mentioned facet is an ANGULAR FACET. The program will then look for the set of RADIUSES that best partition the space into sectors according to that facet. The Separation Index will indicate agreement with the angular partition pattern.

Mark the Radial check-box if you want to test the hypothesis that the above mentioned facet is a RADIAL FACET. The program will then look for the set of CONCENTRIC CIRCLES that best partition the space into rings according to that facet. The Separation Index will indicate agreement with the radial partition pattern."""

FACET_DIAGRAM_SCREEN_p1 = """A facet diagram is a reproduction of the SSA solution except that in the place of each variable, its facet-element is printed. Facet diagram facilitates the identification of systematic partitioning of the space by the facet represented. For a 2-dimensional solution, one facet diagram will be produced for every facet. For a 3-dimensional solution, three; and for 4-d solution, six such diagrams will be produced.

To switch a Yes/No, just click on it. Alternatively, you can use the Tab/Shft-Tab keys to move the button on the grid and use the space-bar to push and change it."""

NEXT_command_p1 = """Use this command to move to the next screen in the FSSA form.

This command is also available via a button on the bottom of the screen and a little right arrow in the toolbar."""

PREVIOUS_command_p1 = """Use this command to move to the preceding screen in the FSSA form.

This command is also available via a button on the bottom of the screen and a little left arrow in the toolbar."""

INPUT_FILE_command_p1 = """Use this command to take a peek in your data input file, e.g. if you are not sure about its format and where variables lie or how coefficients are formatted.

The input file will be opened for you in a DOS editor; use the editor's exit command to return to FSSA for Windows."""

OUTPUT_FILE_command_p1 = """Use this command to look at the output file after a successful run.

The output file will be opened for you in a DOS editor; use the editor's exit command to return to FSSA for Windows."""

ELEMENT_LABELS_COMMAND_p1 = """ to define number of facets, number of 
elements in each facet, and facet element labels.

Use these command and screen also to specify that you want no faceted calculations."""

VARIABLE_ELEMENTS_IN_FACETS_SCREEN_p1 = """That the variables may be classified by a facet, means that each variable belongs to one of the facet's classes. I.e., each variable may be assigned a facet-element of that particular facet. Similarly, from each of the additional facets you may have defined, a facet-element can be assigned to the same variable. In this screen you are asked to classify each variable by Facet A (then by Facet B, if any, etc). In carrying out this task use the numerical designation of the appropriate facet-element.

You can use the mouse to open a combo-box of facet elements that you have defined, or select by a digit. Select 0 (Undefined) for a variable that has no classification in a particular facet.

Upon selection, the cursor will automatically move to the next variable; You do not need to move it yourself (by mouse or Tab key, as you usually do)."""

VARIABLE_DEFINITION_SCREEN_p1 = """In this screen you can define variable labels and select variables for a run. If you are working with Recorded Data, you are also required to define the file structure (i.e. where in the file the variables data reside) in this screen.

The main attraction in this screen is a list box with a line for every variable. This list box is actually a table with the following columns:"""

VARIABLE_DEFINITION_SCREEN_p2 = "You can edit all the values of the variable by double clicking on the table entry.  If you press the Add Variable button (enabled only for Recorded Data), a new variable (i.e with serial number one after the last defined so far) will be created and opened for you to edit. When working with Recorded Data, you can also delete the last variable in the list by using the Delete Variable button. or you can delete any variable by selecting it and pressing the Delete selected rows."

DIMENSIONS_AND_COEFFICIENTS_SCREEN_p1 = """
This screen reports the number of variables you have selected to work on, and offers the following fields:

Type of coefficients:

When working with Recorded Data, you can select between Monotonicity and Pearson. The coefficient of Monotonicity between two variables ranges from -1 to +1 and assesses to what extent an increase in one variable is accompanied by an increase (or no decrease) in the other variable, with no reference to an a priori regression line. Its absolute value is no smaller, and usually larger, than that of Pearson correlation. The coefficient of monotonicity is more appropriate for ordinal data, where no linearity is assumed for the regression line. Pearson correlation is the familiar linear correlation coefficient. Select either Monotonicity or Pearson, to suit your data and assumptions.

When working with a Coefficient Matrix, you can select between Similarity and Dissimilarity.Specify whether the matrix-entries represent similarity between the objects (e.g. correlation coefficients, indices of confusion, judged similarity) or dissimilarity between the objects (e.g., distance or indices of alienation).

Lowest dimensionality and Highest dimensionality specify the range of dimensionalities to be tested. Dimensionalities may be between 2 and 10 with the lower being less than or equal to the higher. If only one dimensionality is desired, for example, two-dimensional, enter that dimensionality in both fields (i.e. 2 and 2 in the example)."""

RECODING_DESCRIPTION = """The Recode function allows you to modify the numerical values of a variable or a set of variables according to your specifications.\nBelow are examples illustrating how this function can be used:"""

RECODING_EXAMPLE_1 = """If a variable is defined with values 1, 2, 3, 4, and 5, you may want to group these values into new categories. For instance:
• Change 1 and 2 to the new value 1
• Change 3 to 2
• Change 4 and 5 to 3

This type of recoding can be useful, for example, to reduce the number of distinct values, which is often advisable when running analyses like POSAC."""

RECODING_EXAMPLE_2 = """If a variable is defined with values 1, 2, 3, 4, and 5, you might want to reverse the order of these values. Thus:
• Change 1 to 5
• Change 2 to 4
• Keep 3 as 3
• Change 4 to 2
• Change 5 to 1

Reversing values may be needed ensure that all processed variables have a Common Meaning Range (See Shye & Elizur, 1994), which\naligns with the principles of Facet Theory."""

RECODING_EXAMPLE_3 = """If a variable is defined with values 1, 2, 3, 4, 5, and 6, you might want to both group and reverse these values. For example:
• Group 1 and 2 into 3
• Change 3 to 2
• Group 4, 5, and 6 into 1"""

RECODING_STEPS = """To recode a variable or a set of variables, follow these steps:
1. Specify the variable(s): Identify the variable(s) you wish to recode.
2. List recoding operations: Define the current ("old") values and the new values to which they should be changed."""

RECODING_EXAMPLE_TABLE = [
    ("Old Value(s)", "New Value"),
    ("1, 2", "3"),
    ("3", "2"),
    ("4–6", "1")
]

RECODING_EXAMPLE_NOTE = """By following this process, you can efficiently recode variables to meet the specific requirements of your analysis.
If you only need to reverse the valid values of a variable (or a set of variables), you can use the Reverse Values shortcut function.

However, keep in mind that this function only reverses the values that actually appear in the input data file. For example, if a variable is define\nto include the values 1, 2, 3, 4, 5, and 6, but only the values 3, 4, 5, and 6 are present in the data file,\nthe Reverse Values function will perform the following changes:
• 3 becomes 6
• 4 becomes 5
• 5 becomes 4
• 6 becomes 3

Unused values (e.g., 1 and 2 in this example) will not be considered or reversed."""

RECODING_REFERENCE = """Shye, S. & Elizur. D. (1994). Introduction to Facet Theory: Content design and intrinsic data analysis in behavioral research. Thousand Oaks, CA: Sage."""