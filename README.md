# Anki to csv file converter

A simple way to convert Anki `.apgk` files into plain `.csv` files

## Usage

```bash
python3 anki_to_csv.py <path_to_apkg_file>
```

The script will create a temporary directory, extract the contents of the `.apkg` file into it, and then convert the contents into a `.csv` file.
The temporary directory will be deleted after the conversion is done

## Limitations

This script only extracts the front and back sides of each card, all other data is ignored.
It also does some transformations to the text:

  - Replaces `<br>` with `\n`
  - Removes non-breaking spaces
