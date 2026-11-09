"""Launch the original desktop application with local synthetic demonstration data."""
from pathlib import Path
import os
import subprocess
import sys
from setup_demo import main as initialize_demo

ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    os.chdir(ROOT)  # Original GUI and database use project-root-relative paths.
    initialize_demo()  # Creates MySleep.db on first run without overwriting local changes.
    subprocess.run([sys.executable, str(ROOT / "app" / "AppFinale.py")], cwd=ROOT, check=True)
