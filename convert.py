import sys
import os
import zipfile
import sqlite3
import shutil
import csv

def extract_and_dump(apkg_file):

    # Check if the file has the .apkg extension
    if not apkg_file.endswith('.apkg'):
        print("Error: The file must have a .apkg extension")
        return

    # Check if the file exists
    if not os.path.isfile(apkg_file):
        print(f"Error: File '{apkg_file}' does not exist")
        return

    # Create a temporary directory for extraction
    extraction_dir = '.anki-to-csv-temp'
    os.makedirs(extraction_dir, exist_ok=True)

    # Extract the .apkg file (really just a ZIP archive)
    try:
        with zipfile.ZipFile(apkg_file, 'r') as zip_ref:
            zip_ref.extractall(extraction_dir)
            print(f"Extracted contents to temporary directory {extraction_dir}")
    except zipfile.BadZipFile:
        print("Error: The file is not a valid ZIP archive")
        return

    # Open the SQLite database
    try:
        conn = sqlite3.connect(f'{extraction_dir}/collection.anki2')

        # Dump all notes from the database
        cursor = conn.cursor()
        cursor.execute("SELECT sfld as front_side, flds as back_side FROM notes;")
        notes = cursor.fetchall()
      
        # Write the notes to a CSV file
        csv_file = apkg_file.replace('.apkg', '.csv')
        with open(csv_file, 'w') as f:
            writer = csv.writer(f, delimiter=",")
            writer.writerow(["Front", "Back"])

            for note in notes:
                front_side = note[0]
                back_side = note[1]

                # The backside also contains the front side, so we'll remove it (they are separated by 0x1f)
                back_side = back_side.split('\x1f')[1]

                # Replace the HTML line breaks with newlines
                front_side = front_side.replace("<br>", "\n")
                back_side = back_side.replace("<br>", "\n")

                # Remove non-breaking spaces
                front_side = front_side.replace("&nbsp;", " ")
                back_side = back_side.replace("&nbsp;", " ")

                # Fix single quotes
                front_side = front_side.replace("’", "'")
                back_side = back_side.replace("’;", "'")

                writer.writerow([front_side, back_side])

        print(f"Dumped {len(notes)} notes to {csv_file}")

        conn.close()
    except sqlite3.Error as e:
        print(f"Error: Unable to connect to the SQLite database {e}")

    # Remove the temporary directory
    print("Removing temporary directory")
    shutil.rmtree('.anki-to-csv-temp')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file.apkg>")
    else:
        apkg_file = sys.argv[1]
        
        extract_and_dump(apkg_file)
