import csv
from pathlib import Path


def add_processed_flag(in_csv: Path, out_csv: Path) -> None:
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    with in_csv.open("r", newline="", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in)
        fieldnames = list(reader.fieldnames or []) + ["processed"]

        with out_csv.open("w", newline="", encoding="utf-8") as f_out:
            writer = csv.DictWriter(f_out, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                row["processed"] = "1"
                writer.writerow(row)
