"""Initialize an empty local MySleep prototype database without demo personal data."""
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
DATABASE = ROOT / "MySleep.db"
SCHEMA = Path(__file__).resolve().with_name("schema.sql")

def main():
    with sqlite3.connect(DATABASE) as connection:
        connection.executescript(SCHEMA.read_text(encoding="utf-8"))
    print(f"Initialized empty local database: {DATABASE}")
    print("No users or patient records were imported.")

if __name__ == "__main__":
    main()
