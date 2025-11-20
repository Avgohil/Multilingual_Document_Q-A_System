"""Language detection and translation utilities.

This module provides small, focused helpers for detecting the language of
a text string and translating text to English or to a specified target
language. It prefers `langdetect` for detection and falls back to `langid`
if `langdetect` is not available. Translation uses `deep-translator`'s
GoogleTranslator wrapper; if translation fails the original text is
returned.

The functions are lightweight utilities intended for use by other modules
in the project (no business logic, no CLI or main runner here).
"""

from typing import Optional

try:
    from langdetect import detect  # type: ignore
    _DETECTOR = "langdetect"
except Exception:
    try:
        import langid  # type: ignore

        _DETECTOR = "langid"
    except Exception:
        _DETECTOR = None

try:
    from deep_translator import GoogleTranslator  
except Exception:  
    GoogleTranslator = None  # type: ignore


def detect_language(text: str) -> str:
    """Detect the language code of `text`."""
    if not text or not text.strip():
        return "unknown"

    try:
        if _DETECTOR == "langdetect":
            
            return detect(text)
        elif _DETECTOR == "langid":
            
            lang, _ = langid.classify(text)  
            return lang
        else:
            return "unknown"
    except Exception:

        return "unknown"


def translate_to_english(text: str) -> str:
    """Translate any-language `text` into English."""
    if not text:
        return ""

    if GoogleTranslator is None:

        return text

    try:
        translator = GoogleTranslator(source="auto", target="en")
        return translator.translate(text)
    except Exception:

        return text


def translate_to_language(text: str, target_lang: str) -> str:
    """Translate English `text` to `target_lang`.

    """
    if not text:
        return ""

    if GoogleTranslator is None:
        return text

    try:
        translator = GoogleTranslator(source="en", target=target_lang)
        return translator.translate(text)
    except Exception:
        return text
