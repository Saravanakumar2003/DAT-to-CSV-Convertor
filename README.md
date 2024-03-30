<h1 align=center>.dat to .csv File Converter</h1>

## Overview

This project is a Python-based .dat to .csv file converter initially developed during my internship tenure at the National Institute of Wind Energy (NIWE). The objective was to address the challenge of converting .dat files to .csv format efficiently.

### Key Features

- Conversion of .dat files from NIWE's wind energy data to .csv format.
- Utilizes Python's CSV, re, and sys libraries to handle data processing and conversion.
- A responsive website to convert files effortlessly.
- Batch conversion of .dat files to .csv is supported.

## Background

During my internship at NIWE, I enthusiastically embarked on the challenge of **converting .dat files to .csv**, an essential requirement for data analysis and visualization. Despite encountering complex data structures and a limited timeframe, I embraced the challenge, leading to a rewarding learning journey.

I was asked to create a Python code for easy conversion of .dat files to .csv format. However, I took an **innovative step** forward by deploying a user-friendly website, enabling anyone, regardless of technical expertise, to perform the conversion effortlessly. This proactive approach allows for **automation and provides accessibility to perform the conversion in a fraction of a second using any device, anytime and anywhere.**

## Experience

- **Problem-solving**: Navigating through the intricacies of .dat file structures and devising a robust conversion process.
- **Time Management**: Accomplishing the task within a restricted timeframe while ensuring quality and accuracy.
- **Learning Curve**: Embracing challenges as opportunities for growth and expanding knowledge in data handling and conversion.
- **Proactive Deployment**: Went beyond the initial task to develop a user-friendly website for effortless automation of the conversion process.

## Project Structure

- **app.py**: Python script for the .dat to .csv conversion.
- **conversion_utils.py**: Utility functions used for data processing.
- **templates**: This directory holds HTML templates used in the application. The upload.html file resides here, facilitating file upload functionality.
- **converted_files**: The converted output files are stored in this directory.
- **uploaded_files**:  A folder dedicated to storing uploaded .dat files for the conversion process.
- **README.md**: The current document provides an overview of the project.

## Scope of the problem

I had a .dat file containing data segments structured in a format similar to the one below:

```
$
GPS LAT GPS LONG   ROLL  PITCH AZIMUT   T IN  PmBARS  T OUT    RH%
8.9636   77.7201   -0.5    1.0    0.0   43.3   998.7   25.1   86.0                    

   BL#  MONTH   DAY  YEAR  HOUR   MIN  VAL1  VAL2  VAL3  VAL4
 19753    12     7  2023     0     0    73    82   121     0

  SPU1  SPU2  SPU3  SPU4 NOIS1 NOIS2 NOIS3 NOIS4 FEMAX SOFTW
     1     0     0     0  4203  4102  4700    18   503  9065

  FE11  FE12  FE21  FE22  SNR1  SNR2  SNR3  SNR4 CHECK   JAM
     8     7     8     8   139   139   139     0    40 11100

   ALT    CT SPEED   DIR     W    SW    SU    SV  ETAM

   200    46   299    46     0     1    19    13     0
   190    52   288    46     0     1    18    15     0
   180    58 -9999    47     0     1    18    17     0
   ...   ...   ...   ...   ...   ...   ...   ...   ...
   30    975    29    73    -8     1    14     2     0 
$

  GPS LAT  GPS LONG   ROLL  PITCH AZIMUT   T IN  PmBARS  T OUT    RH%
    8.9636   77.7201   -1.0    0.9    0.0   48.5   997.7   28.2   73.2                    

   BL# MONTH   DAY  YEAR  HOUR   MIN  VAL1  VAL2  VAL3  VAL4
 19944    12     7  2023    0     10    21    34    51     0

  SPU1  SPU2  SPU3  SPU4 NOIS1 NOIS2 NOIS3 NOIS4 FEMAX SOFTW
     1     0     0     0  5502  5403  5701     8   490  9065

  FE11  FE12  FE21  FE22  SNR1  SNR2  SNR3  SNR4 CHECK   JAM
     8     7     9     7   135   136   139     0    56 11100

   ALT    CT SPEED   DIR     W    SW    SU    SV  ETAM

   200    66   598    39    -9    16    22    36   169
   190    72   599    39    -9    16    22    36   189
   180    77   600    38    -9    17    22    36   194
    ..    ..   ...    ..     .    ..    ..    ..   ...
    20    80   600    37    -9    15    22    35   154
    30    83   591    36    -9    14    22    35   115

$

Again the same above format only the data will change. This dataset contains multiple segments
similar to the provided snippet, each representing a 10-minute interval of records between each $.

$
```

Now, I have to convert this data into a CSV file named 'output.csv' with a specific format:

1. The first row contains headers specified as below.
2. Subsequent rows should contain:

- Timestamp in YYYY-MM-DD HH:MM:SS format extracted from the XML.
- Wind speeds at different altitudes (200m to 30m) and divide by 100 (Cm/s to M/s Conversion).
- Wind directions at different altitudes (200m to 30m).
- Temperatur internal, Pressure, Temperature external and Humidity

For example, for a given input, the desired output CSV would resemble:

```
Timestamp, ALT200_Speed, ALT190_Speed, ..., ALT200_Dir, ALT190_Dir, ..., Temp_in, Pressure, Temp_out, Humidity

2023-12-07 00:00:00, 2.99, 2.88, ..., 46, 46, ..., 43.3, 998.7, 25.1, 86.0 
2023-12-07 00:00:10, 5.98, 5.99, ..., 39, 39, ..., 48.5, 997.7, 28.2, 73.2 


```

## Getting Started

### Algorithm for the Code -

1. Read .dat file and extract relevant data segments

2. Loop through the file, identify and extract segments containing wind data between $ symbol

3. Process each segment to extract timestamps, wind speeds, and directions

4. Generate 'output.csv' with appropriate headers and write data

5. Write each timestamp, wind speed, and directions to the CSV file in the specified format

### Tech Stack

- **Python**: Main programming language.
- **Flask**: Web framework used for the converter website.
- **re, sys and csv libraries**: Utilized for data manipulation and conversion.

<div align="center">
    <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54" alt="Python Badge">
    <img src="https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white" alt="Flask Badge">
</div>

### Screenshots

<a href="https://postimg.cc/t7tf1DZG" target="_blank"><img src="https://i.postimg.cc/FF2QBBhz/Intro.jpg" alt="Intro"/></a><br/><br/>

## Getting Started
- Click "Choose File" to select your .dat file.
- Click "Convert" to initiate the conversion process.
- Download the converted .csv file.

### Video Walkthrough

[![Video Walkthrough](https://img.youtube.com/vi/ggpB_Erkl4k/0.jpg)](https://www.youtube.com/watch?v=ggpB_Erkl4k)


### Deployment

<div align="center">
   <img src="https://img.shields.io/badge/pythonanywhere-%232F9FD7.svg?style=for-the-badge&logo=pythonanywhere&logoColor=151515" alt="PythonAnywhere">
   <p>The site can be accessed at <a href="https://saravanakumar.pythonanywhere.com">here</a></p>
</div>



### Acknowledgement

<ul>
<li>I express my deepest gratitude to the NIWE team for their invaluable support and guidance throughout this project.</li>
<li> <b>Boopathy Sir</b> provided exceptional mentorship, offering insightful guidance during the internship.</li>
<li> <b> Zach Sir's  </b>technical support was instrumental in overcoming challenges. </li>
<li>Special thanks to <b> Senthil Sir  </b> for providing crucial data and  <b>Vinoth Sir </b> for meticulously validating project outputs.</li> 
<li>Their contributions were pivotal to the project's success and the invaluable learning experiences gained.</li>
</ul>
