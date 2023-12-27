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
