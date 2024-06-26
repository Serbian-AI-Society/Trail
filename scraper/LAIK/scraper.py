import fitz  # PyMuPDF
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import json
from pathlib import Path
from typing import List
# from typing import Path
import argparse
from tqdm import tqdm
from loguru import logger

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from a PDF file.

    Parameters:
    pdf_path (str): The path to the PDF file.

    Returns:
    str: The extracted text from the PDF.
    """
    document = fitz.open(pdf_path)
    full_text = []
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text = page.get_text()
        full_text.append(text)
    return "\n".join(full_text)

def is_valid_sentence(sentence: str) -> bool:
    """
    Checks if a sentence is valid based on given criteria:
    - Must have more than 3 words.
    - No word should be longer than 25 characters.

    Parameters:
    sentence (str): The sentence to check.

    Returns:
    bool: True if the sentence is valid, False otherwise.
    """
    words = sentence.split()
    if len(words) <= 3:
        return False
    if any(len(word) > 25 for word in words):
        return False
    return True

def extract_sentences(pdf_path: str) -> List[str]:
    """
    Extracts sentences from a PDF file, filtering out those
    that do not meet the criteria:
    - Must have more than 3 words.
    - No word should be longer than 25 characters.

    Parameters:
    pdf_path (str): The path to the PDF file.

    Returns:
    list: A list of valid sentences extracted from the PDF.
    """
    text = extract_text_from_pdf(pdf_path)
    sentences = sent_tokenize(text)
    filtered_sentences = [sentence for sentence in sentences if is_valid_sentence(sentence)]
    return filtered_sentences

def main(pdfs: List[str], output_dir: Path) -> None:
    """
    Scrape manuals from a list of pdfs and save them as JSON files.

    Args:
        pdfs (List[str]): A list of pdfs to scrape.
        output_dir (Path): The directory where the JSON files will be saved.
    """
    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    for pdf in tqdm(pdfs, desc="Scraping manuals", total=len(pdfs)):

        save_path = output_dir / f"{Path(pdf).stem}.json"

        try:
            manual_guides = extract_sentences(pdf_path=pdf)
        except Exception as e:
            logger.error(f'Failed to scrape data from pdf, data might be corrupted: "{pdf}" - {e}')
            continue

        try:
            with open(save_path, "w", encoding="utf-8") as file:
                json.dump(manual_guides, file, indent=4, ensure_ascii=False)
            logger.info(f'Successfully saved data to "{save_path}"')
        except Exception as e:
            logger.error(f'Failed to save data to "{save_path}" - {e}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape home appliances manuals.")
    parser.add_argument(
        "--files",
        type=Path,
        help="Path to text file containing paths to manuals.",
    )
    parser.add_argument(
        "--output_dir",
        type=Path,
        help="Directory to save the JSON files.",
    )

    args = parser.parse_args()

    with open(args.files, "r", encoding="utf-8") as file:
        pdfs = [line.strip() for line in file if line.strip()]

    main(pdfs=pdfs, output_dir=args.output_dir)