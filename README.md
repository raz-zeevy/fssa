# FSSA (Faceted SSA)

[![Website](https://img.shields.io/website?url=https://raz-zeevy.github.io/fssa/)](https://raz-zeevy.github.io/fssa/)



## Introduction

Welcome to the `fssa` application! This desktop application is dedicated to providing a robust and user-friendly framework for facilitating the analysis and visualization of statistical data. Our goal is to make data analysis more accessible and efficient for researchers, data scientists, and statisticians.

for more details [🌐 Visit the FSSA Website](https://raz-zeevy.github.io/fssa/)

## About the Project

The `fssa` project, inspired by the original Faceted SSA for Windows (FSSAWIN), is designed to streamline the process of statistical data analysis. It includes a variety of tools and functionalities, such as data parsing, statistical modeling, and graphical representation of data, with a focus on ease of use without compromising the depth of analysis.

### Faceted Smallest Space Analysis (FSSA)

Faceted Smallest Space Analysis (FSSA) is a Multidimensional Scaling (MDS) procedure that optionally allows for the incorporation of content classifications (=facets) of the mapped objects into the analysis and testing their validity. FSSA maps objects (typically variables) in a space of prespecified dimensionality to represent pairwise similarity or dissimilarity observed between them. The (dis)similarity measures are either precomputed or computed by the program from data files.

## Installation

Installing `fssa` only requires a few simple steps:

1. Download the installation package:

   | Version  | Date       | Download |
   |----------|------------|----------|
   | alpha 0.97 | 2024-01-25 | [![Setup](https://img.shields.io/badge/setup-exe-blue.svg)](http://u.pc.cd/mHXctalK) |

2. Run the downloaded `FssaSetup.exe` file to start the installation wizard.

3. Follow the on-screen instructions provided by the installation wizard to complete the setup.

Once installed, `fssa` is ready to use on your system.
## Usage

Here's how to get started with `fssa`:

1. Run the application: double click on `fss`

 2. Follow the on-screen instructions to input your data and configure the analysis parameters.

*Note: Detailed usage instructions will be added soon.*
## Data Analysis and Visualization

### Understanding Your Data

Before starting with FSSA, it's crucial to understand the data you are working with:

#### CASE I: Matrix Material
- Ensure the (dis)similarity matrix is accessible on your computer.
- Know the matrix file's name and full path (e.g., `\mydir\simil.mat`).
- Understand the matrix format in the file, including the number of fields per row, columns per field, and decimal places used.
- Determine if coefficients represent similarity (e.g., correlations) or dissimilarity (e.g., distance).
- Identify any missing values in the matrix.

#### CASE II: Data
- Verify the data set is in an ASCII file of fixed format and recoded appropriately.
- Know the data file's name and full path (e.g., `A:\mydir\recod.dat`).
- Understand the structure of the data file, including records per case and the location of each variable.
- Identify valid and missing values for each variable.

#### Facet Option
- You may choose to run a simple SSA without facets or use the facet option for more complex analysis.
- For the facet option, have a substantive criterion for classifying the variables.

### Results and Output
- By default, FSSA results are saved in `FSSA.RES`.
- You can change the file names, save to different directories, or direct output to a printer.

### Inspecting and Printing Diagrams
- The program produces screen diagrams of the solution and facet diagrams.
- After completion, these diagrams can be re-displayed for inspection.
- To print the diagrams, use the view menu and follow the instructions for your specific printer.

## Screenshots

*Placeholder for screenshots*

*More screenshots will be added soon.*

## References

- Borg, I. and Shye, S. Facet Theory: Form and Content. Newbury Park, California: Sage, 1995.
- Guttman, L. A general nonmetric technique for finding the smallest coordinate space for a configuration of points. PSYCHOMETRIKA, 1968.
- Shye, S. (ed.) Theory Construction and Data Analysis in the Behavioral Sciences. San Francisco: Jossey-Bass, 1978.
- Shye, S. Achievement motive: a faceted definition and structural analysis. MULTIVARIATE BEHAVIORAL RESEARCH, 1978.
- Shye, S. Smallest Space Analysis. In T. Husen & T.N. Postlethwaite (eds.) INTERNATIONAL ENCYCLOPEDIA OF EDUCATION. Oxford: Pergamon, 1985; 2nd edition, 1994.
- Shye, S. Facet Theory. In T. Husen & T.N. Postlethwaite (eds.) INTERNATIONAL ENCYCLOPEDIA OF EDUCATION, 2nd EDITION. Oxford: Pergamon, 1994.
- Shye, S. Partial Order Scalogram Analysis. In T. Husen & T.N. Postlethwaite (eds.) INTERNATIONAL ENCYCLOPEDIA OF EDUCATION. Oxford: Pergamon, 1985; 2nd edition, 1994.
- Shye, S. (In Press) Facet Theory. Encyclopedia of Statistical Sciences (Update). New York: Wiley
- Shye, S. and Elizur, D. Introduction to Facet Theory. Newbury Park, California: Sage, 1994.

## Contact

For any queries or suggestions, feel free to contact us at [raz3zeevy@gmail.com](mailto:raz3zeevy@gmail.com).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
