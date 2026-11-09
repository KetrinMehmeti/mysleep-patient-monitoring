# Scope, limits and release notes

- **Demonstration only:** All accounts shipped in `sample_data/MySleep_demo.db` are fictional. Personal identifiers, contact details and emails have been replaced with placeholders. Static plot and text files are generated synthetic signals, not clinical readings.
- **Security:** The original GUI compares plaintext demo passwords and contains some SQL statements built with string interpolation. Do not deploy this application as-is or store actual patient records.
- **Original code:** `app/AppFinale.py` preserves the student-era application, including some unfinished/experimental UX paths. The app was reviewed statically; complete on-device QA has not been performed.
- **Testing:** Database initialization, demo credentials, paths and Python syntax were validated. No full Windows GUI end-to-end test was run in this environment.
- **Data model:** `db/schema.sql` is included separately; the demo SQLite file maintains a historical test dataset, including relative paths to bundled synthetic signal traces and plots.
- **External packages:** The original `venv/` folder and `CTk_examples/` tutorial assets were deliberately excluded; recreate the environment using `requirements.txt`.
- **Original helper script:** The original `APP/MySleepdb.py` mixed database modification with machine-specific paths and unrelated setup side effects; curated non-destructive functions are available as `app/data_processing.py`.
- **Original report:** `final_report.docx` discusses a different project about hypertension and different authors; it is intentionally not bundled or attributed to MySleep.
- **Group project:** Before publication, coordinate acknowledgements, source ownership and image-asset permissions with the other contributors.
- **Video:** The full-length demonstration is included, compressed to a small GitHub-friendly MP4 file. Its fictional data should not be mistaken for patient information.
