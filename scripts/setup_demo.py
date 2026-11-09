"""Initialize a local working copy of the synthetic MySleep demonstration database."""
from pathlib import Path
import argparse
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sample_data" / "MySleep_demo.db"
DESTINATION = ROOT / "MySleep.db"


def main():
    parser = argparse.ArgumentParser(description="Prepare synthetic MySleep demo data")
    parser.add_argument("--reset", action="store_true", help="Replace local demo DB with the packaged copy")
    args = parser.parse_args()
    if DESTINATION.exists() and not args.reset:
        print(f"Keeping existing local database: {DESTINATION}")
        print("Use --reset to replace it with the packaged synthetic demo data.")
        return
    shutil.copy2(SOURCE, DESTINATION)
    print(f"Prepared synthetic demo database: {DESTINATION}")
    print("DEMO ONLY: doctor1@example.com / 1234 or patient4@example.com / 1234")

if __name__ == "__main__":
    main()
