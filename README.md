<h1 align=center>.dat to .csv File Converter</h1>

## Overview

This project is a Python-based .dat to .csv file converter initially developed during my internship tenure at the National Institute of Wind Energy (NIWE). The objective was to address the challenge of converting .dat files to .csv format efficiently.

### Key Features

- Conversion of .dat files from NIWE's wind energy data to .csv format.
- Utilizes Python's CSV, re, and sys libraries to handle data processing and conversion.
- A responsive website to convert files effortlessly.

## Background

During my internship at NIWE, I enthusiastically embarked on the challenge of **converting .dat files to .csv**, an essential requirement for data analysis and visualization. Despite encountering complex data structures and a limited timeframe, I embraced the challenge, leading to a rewarding learning journey.

I was asked to create a Python code for easy conversion of .dat files to .csv format. However, I took an **innovative step** forward by deploying a user-friendly website, enabling anyone, regardless of technical expertise, to perform the conversion effortlessly. This proactive approach allows for **automation and provides accessibility to perform the conversion in a fraction of a second using any device, anytime and anywhere.**

## Experience

- **Problem-solving**: Navigating through the intricacies of .dat file structures and devising a robust conversion process.
- **Time Management**: Accomplishing the task within a restricted timeframe while ensuring quality and accuracy.
- **Learning Curve**: Embracing challenges as opportunities for growth and expanding knowledge in data handling and conversion.
- **Proactive Deployment**: Went beyond the initial task to develop a user-friendly website for effortless automation of the conversion process.

## Project Structure

- **code.py**: Python script for the .dat to .csv conversion.
- **conversion_utils.py**: Utility functions used for data processing.
- **templates**: This directory holds HTML templates used in the application. The upload.html file resides here, facilitating file upload functionality.
- **converted_files**:  A folder dedicated to storing converted CSV files. The converted output files are stored in this directory.
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

Again the same above format only the data will change. This dataset contains multiple segments similar to the provided snippet, each representing a 10-minute interval of records between each $.

$
```

Now, I have to convert this data into a CSV file named 'output.csv' with a specific format:

1. The first row contains headers specified as below.
2. Subsequent rows should contain:

- Timestamp in YYYY-MM-DD HH:MM:SS format extracted from the XML.
- Wind speeds at different altitudes (200m to 30m).
- Wind directions at different altitudes (200m to 30m).

For example, for a given input, the desired output CSV would resemble:

```
Timestamp, ALT200_Speed, ALT190_Speed, ..., ALT30_Speed, ALT200_Dir, ALT190_Dir, ..., ALT30_Dir

2023-12-07 00:00:00, 299, 288, ..., 29, 46, 46, ..., 73
2023-12-07 00:00:10, 598, 599, ..., 591, 39, 39, ..., 36


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

### Python Code:

```python
import csv
import re
import os

def to_row(line: str) -> list[str]:  # Split by whitespace and strip whitespace from each element 
    row = [x.strip() for x in re.split(r"\s+", line)] 
    return row[1:] # Skip first element (empty string) 

def convert_dat_to_csv(input_file_path): # Convert .dat file to .csv file
    LE = "\n" # Line ending
    with open(input_file_path) as f: # Read .dat file
        txt_chunks = f.read().split("$" + LE) # Split by "$" and line ending
        txt_chunks = txt_chunks[1:] # Skip first element (empty string)
        chunks = [x.strip().split(LE) for x in txt_chunks] 
    
    table: list[dict[str, str]] = [] # List of dictionaries (rows)
    
    for chunk in chunks: # Iterate through chunks
        if len(chunk) < 15:  # Skip chunks with insufficient data
            continue 
        assert chunk[0].strip().startswith("GPS LAT") # Check if chunk is valid (starts with "GPS LAT") 
        assert chunk[3].startswith("   BL#") # Check if chunk is valid (starts with "   BL#")
        
        header = to_row(chunk[4]) # Get header row
        mo, day, yr = header[1:4] # Get month, day, year
        hr, min = header[4:6] # Get hour, minute
        ts = f"{yr}-{mo:>02}-{day:>02} {hr:>02}:{min:>02}:00"  # Format timestamp (YYYY-MM-DD HH:MM:SS) 

        final_row: dict[str, str] = {"Timestamp": ts} # Create dictionary (row) with timestamp as first element
        
        assert chunk[12].startswith("   ALT") # Check if chunk is valid (starts with "   ALT")
        for line in chunk[14:]: # Iterate through lines
            _row = to_row(line) # Split by whitespace and strip whitespace from each element

            if len(_row) == 0 or _row[0][:2] == "..": # Skip empty lines and lines starting with ".."
                continue

            alt = _row[0] # Get altitude

            if int(alt) < 30: # Skip altitudes below 30
                continue 

            speed = _row[2] # Get speed
            dir = _row[3] # Get direction

            final_row[f"ALT{alt}_SPEED"] = speed  # Add altitude and speed to row
            final_row[f"ALT{alt}_DIR"] = dir  # Add altitude and direction to row
        
        table.append(final_row) # Add row to table
    
    all_keys = {k for row in table for k in row} # Get all keys from table
    
    def col_name_key(k: str) -> tuple[int, int]: # Sort keys by altitude and speed
        if k == "Timestamp": # Timestamp should always be first
            return (0, 0) 

        k = k[3:] # Remove "ALT" from key
        parts = k.split("_") # Split by "_"
        val, kind = int(parts[0]), parts[1] # Get altitude and speed/direction

        return (1 if kind == "SPEED" else 0, val) # Sort by speed first, then altitude

    fieldnames = sorted(all_keys, key=col_name_key, reverse=True) # Sort keys by altitude and speed
    
    #This is a special case for the timestamp
    fieldnames.remove("Timestamp")  # Remove timestamp from fieldnames
    fieldnames.insert(0, "Timestamp")   # Add timestamp to beginning of fieldnames
    
    output_folder = 'converted_files'   # Create folder for converted files
    output_file_path = os.path.join(output_folder, 'output.csv')    # Create output file path

    with open(output_file_path, "w", newline="") as f: # Write to output file
        writer = csv.DictWriter(f, fieldnames=fieldnames, restval="N/A") # Create writer       
        #Restval is the value to be written if the dictionary is missing a key
        writer.writeheader() # Write header row
        writer.writerows(table) # Write rows

    return output_file_path # Return output file path

# Path: conversion_utils.py
```
### Short Explanation:

1. **Libraries Imported**: The code starts by importing required libraries (csv, re, sys).

2. **Parsing .dat File**:  It reads a file specified by the input_file_path, splits its content based on the "$" delimiter, processes each chunk of data, and organizes them into a list of dictionaries (table).

3. **Data Processing**:

- The function to_row splits lines into fields.
- Assertions validate specific lines in each chunk to ensure data structure.
- Date-time information is extracted from the header and organized into a Timestamp dictionary.
- Altitude data is processed and stored in the final_row dictionary.

4. **CSV File Writing**: Ultimately, the processed data contained in the table is written into an "output.csv" file using csv.DictWriter. Before writing, the field names are sorted based on predefined rules to ensure a structured CSV layout.


### Deployment

![PythonAnywhere](https://img.shields.io/badge/pythonanywhere-%232F9FD7.svg?style=for-the-badge&logo=pythonanywhere&logoColor=151515)
The site can be accessed at [saravanakumar.pythonanywhere.com](https://saravanakumar.pythonanywhere.com).

### Acknowledgement

I express my deepest gratitude to the NIWE team for their invaluable support and guidance throughout this project. **Boopathy Sir** provided exceptional mentorship, offering insightful guidance during the internship. **Zach Sir's** technical support was instrumental in overcoming challenges. Special thanks to **Senthil Sir** for providing crucial data and **Vinoth Sir** for meticulously validating project outputs. Their contributions were pivotal to the project's success and the invaluable learning experiences gained.