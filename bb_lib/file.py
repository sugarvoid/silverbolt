from csv import reader, writer
from pathlib import Path

def trim_csv(file_path: str) -> None:
    rows = []
    file_extension = Path(file_path).suffix
    print("File Extension: ", file_extension)

    with open(file=file_path, mode='r') as f_input:    
        for row in reader(f_input):
            rows.append([col.strip() for col in row])
    
    # Write the trimmed rows back to the same file
    with open(file=file_path, mode='w', newline='') as f_output:
        csv_writer = writer(f_output)
        csv_writer.writerows(rows)



trim_csv("data/test_csv.csv")