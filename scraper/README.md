# Scraper

This script scrapes appliances manuals from a list of PDFs and saves them as JSON files.

## Usage

To run the script, use the following command:

```bash
python scraper/scraper.py --file scraper/pdfs.txt --output-dir appliances_test
```

## Arguments
- `--files`: Path to a text file containing PDFs separated by newlines.
- `--output-dir`: Directory to save the JSON files.

## Example

To scrape home appliances manuals from a list of PDFs in pdfs.txt and save the output in the `scraper/appliances` directory:
```bash
python scraper/scraper.py --file scraper/pdfs.txt --output-dir scraper/appliances
```
> ⚠️ _**Note**: Ensure you are in the root directory of the project before running the script._

## Output
The output JSON files will be saved in the specified output directory, with each file named after the corresponding URL's stem.
