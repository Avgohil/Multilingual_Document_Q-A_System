"""PDF text extraction helpers.

This module provides utilities to extract and clean text from PDF files
using `pdfplumber`.
"""

from pathlib import Path
import re

import pdfplumber


def clean_text(text: str) -> str:
	"""Clean extracted text.

	- Normalize newlines
	- Replace multiple spaces/tabs with a single space
	- Replace multiple newlines with a single newline
	- Strip leading/trailing whitespace

	Args:
		text: The raw text to clean.

	Returns:
		The cleaned text.
	"""
	if not text:
		return ""

	# Normalize different newline conventions to "\n"
	text = text.replace("\r\n", "\n").replace("\r", "\n")

	# Collapse sequences of spaces and tabs into a single space
	text = re.sub(r"[ \t]+", " ", text)

	# Remove spaces around newlines
	text = re.sub(r" *\n *", "\n", text)

	# Replace multiple newlines with a single newline
	text = re.sub(r"\n{2,}", "\n", text)

	# Final trim
	return text.strip()


def extract_text_from_pdf(pdf_path: str) -> str:
	"""Extract and return cleaned text from a PDF file."""
	path = Path(pdf_path)
	if not path.is_file():
		raise FileNotFoundError(f"PDF file not found: {pdf_path}")

	page_texts = []
	with pdfplumber.open(path) as pdf:
		for page in pdf.pages:
			text = page.extract_text()
			if text is None:
				continue
			page_texts.append(text)

	full_text = "\n".join(page_texts)
	return clean_text(full_text)


def get_preview_300_words(full_text: str) -> str:
	"""Return the first 300 words from the provided text."""
	if not full_text:
		return ""

	words = full_text.split()
	preview = words[:300]
	return " ".join(preview)

