import csv
import re
import os

def to_row(line: str) -> list[str]:
    row = [x.strip() for x in re.split(r"\s+", line)]
    return row[1:]

def convert_dat_to_csv(input_file_path):
    LE = "\n"
    with open(input_file_path) as f:
        txt_chunks = f.read().split("$" + LE)
        txt_chunks = txt_chunks[1:]
        chunks = [x.strip().split(LE) for x in txt_chunks]
    
    table: list[dict[str, str]] = []
    
    for chunk in chunks:
        if len(chunk) < 15:  # Skip chunks with insufficient data
            continue
        
        print(f"Chunk: {chunk[0]} - Length: {len(chunk[0])}")
        assert chunk[0].strip().startswith("GPS LAT") 
        assert chunk[3].startswith("   BL#")
        
        header = to_row(chunk[4])
        mo, day, yr = header[1:4]
        hr, min = header[4:6]
        ts = f"{yr}-{mo:>02}-{day:>02} {hr:>02}:{min:>02}:00"

        final_row: dict[str, str] = {"Timestamp": ts}
        
        assert chunk[12].startswith("   ALT")
        for line in chunk[14:]:
            _row = to_row(line)

            if len(_row) == 0 or _row[0][:2] == "..":
                continue

            alt = _row[0]

            if int(alt) < 30:
                continue

            speed = _row[2]
            dir = _row[3]

            final_row[f"ALT{alt}_SPEED"] = speed
            final_row[f"ALT{alt}_DIR"] = dir
        
        table.append(final_row)
    
    all_keys = {k for row in table for k in row}
    
    def col_name_key(k: str) -> tuple[int, int]:
        if k == "Timestamp":
            return (0, 0)

        k = k[3:]
        parts = k.split("_")
        val, kind = int(parts[0]), parts[1]

        return (1 if kind == "SPEED" else 0, val)

    fieldnames = sorted(all_keys, key=col_name_key, reverse=True)
    fieldnames.remove("Timestamp")
    fieldnames.insert(0, "Timestamp")
    
    output_folder = 'converted_files'
    output_file_path = os.path.join(output_folder, 'output.csv')

    with open(output_file_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, restval="N/A")
        writer.writeheader()
        writer.writerows(table)

    return output_file_path
