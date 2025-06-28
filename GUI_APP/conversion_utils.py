import re

def to_row(line: str) -> list[str]:
    row = [x.strip() for x in re.split(r"\s+", line)]
    return row[1:]

def convert_dat_to_csv(input_file_path):
    LE = "\n"
    try:
        with open(input_file_path) as f:
            txt_chunks = f.read().split("$" + LE)
            txt_chunks = txt_chunks[1:]
            chunks = [x.strip().split(LE) for x in txt_chunks]

        all_rows = []

        for chunk in chunks:
            if len(chunk) < 15:
                continue

            assert chunk[0].strip().startswith("GPS LAT")
            assert chunk[3].startswith("   BL#")

            header = to_row(chunk[4])
            mo, day, yr = header[1:4]
            hr, min = header[4:6]
            ts = f"{yr}-{mo:>02}-{day:>02} {hr:>02}:{min:>02}:00"

            final_row = {"Timestamp": ts}

            assert chunk[12].startswith("   ALT")
            
            
            temp_in = float(chunk[1].split()[5])
            pressure = float(chunk[1].split()[6])
            temp_out = float(chunk[1].split()[7])
            humidity = float(chunk[1].split()[8])                   

            final_row["TEMP_IN"] = temp_in
            final_row["PRESSURE"] = pressure
            final_row["TEMP_OUT"] = temp_out
            final_row["HUMIDITY"] = humidity

            for line in chunk[14:]:
                _row = to_row(line)

                if len(_row) == 0 or _row[0][:2] == "..":
                    continue

                alt = _row[0]

                if int(alt) < 30:
                    continue

                speed = float(_row[2]) / 100
                if speed == -99.99:
                    speed = -9999

                dir = _row[3]

                final_row[f"ALT{alt}_SPEED"] = speed
                final_row[f"ALT{alt}_DIR"] = dir

            all_rows.append(final_row)

        return all_rows
    except Exception as e:
        print(f"Error during conversion: {e}")
        return []