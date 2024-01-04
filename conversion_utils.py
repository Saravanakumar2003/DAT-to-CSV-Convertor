import re

def to_row(line: str) -> list[str]: 
    row = [x.strip() for x in re.split(r"\s+", line)] # split on whitespace
    return row[1:] # remove first element

def convert_dat_to_csv(input_file_path): # input_file_path is a string
    LE = "\n" # line ending
    try: 
        with open(input_file_path) as f: 
            txt_chunks = f.read().split("$" + LE) # split on $ and line ending
            txt_chunks = txt_chunks[1:] # remove first element
            chunks = [x.strip().split(LE) for x in txt_chunks] # split on line ending

        all_rows = [] # list of dictionaries

        for chunk in chunks: # iterate through chunks
            if len(chunk) < 15: # if chunk is less than 15 lines, skip
                continue 

            assert chunk[0].strip().startswith("GPS LAT") # assert that first line starts with GPS LAT
            assert chunk[3].startswith("   BL#") # assert that fourth line starts with BL#

            header = to_row(chunk[4]) # get header row
            mo, day, yr = header[1:4] # get month, day, year
            hr, min = header[4:6] # get hour, minute
            ts = f"{yr}-{mo:>02}-{day:>02} {hr:>02}:{min:>02}:00" # create timestamp

            final_row = {"Timestamp": ts} # create dictionary with timestamp

            assert chunk[12].startswith("   ALT") # assert that 13th line starts with ALT
            for line in chunk[14:]: # iterate through lines
                _row = to_row(line) # get row

                if len(_row) == 0 or _row[0][:2] == "..": # if row is empty or starts with ..
                    continue 

                alt = _row[0] # get altitude

                if int(alt) < 30: # if altitude is less than 30, skip
                    continue 

                speed = _row[2] # get speed
                dir = _row[3] # get direction

                final_row[f"ALT{alt}_SPEED"] = speed # add speed to dictionary
                final_row[f"ALT{alt}_DIR"] = dir # add direction to dictionary

            all_rows.append(final_row) # append dictionary to list

        return all_rows # return list of dictionaries
    except Exception as e:
        print(f"Error during conversion: {e}") # print error
        return [] # return empty list
