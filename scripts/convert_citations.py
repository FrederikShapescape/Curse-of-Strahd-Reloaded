"""
Convert <span class="citation">...</span> references in CoC:Reloaded markdown files
to clickable Obsidian PDF links.

Maps citations to the correct PDF based on book references.
"""

import re
import os
from pathlib import Path

VAULT_ROOT = Path(r"C:\Users\adobe\OneDrive\vault\Curse-of-Strahd-Reloaded")

# PDF filenames (relative to vault, inside the pdfs/ junction)
PDF_COS = "pdfs/Curse of Strahd.pdf"
PDF_PHB = "pdfs/Player's Handbook.pdf"
PDF_MM = "pdfs/Monster Manual.pdf"
PDF_DMG = "pdfs/Dungeon Master's Guide.pdf"
PDF_VRG = "pdfs/Van Richtens Guide to Ravenloft.pdf"

# Book keyword -> PDF mapping
BOOK_MAP = {
    "player's handbook": PDF_PHB,
    "monster manual": PDF_MM,
    "dungeon master's guide": PDF_DMG,
    "van richten's guide to ravenloft": PDF_VRG,
    "van richten's guide": PDF_VRG,
    "xanathar's guide to everything": None,  # Not available as PDF
    "tasha's cauldron of everything": None,   # Not available
    "mordenkainen presents": None,            # Not available
    "eberron": None,                          # Not available
}


def detect_book(citation_text):
    """Detect which book a citation refers to based on keywords."""
    lower = citation_text.lower()
    for keyword, pdf in BOOK_MAP.items():
        if keyword in lower:
            return pdf
    # Default: Curse of Strahd
    return PDF_COS


def extract_page(citation_text):
    """Extract page number(s) from citation text."""
    # Match patterns like (p. 181), (p. 243-44), p. 181, (pp. 181-182)
    patterns = [
        r'\(pp?\.\s*(\d+)(?:[–\-]\d+)?\)',   # (p. 181) or (p. 181-182)
        r',\s*pp?\.\s*(\d+)',                  # , p. 181
        r'\s+pp?\.\s*(\d+)',                   # p. 181
    ]
    for pattern in patterns:
        match = re.search(pattern, citation_text)
        if match:
            return int(match.group(1))
    return None


def convert_citation(match):
    """Convert a single <span class="citation">...</span> to an Obsidian link."""
    full_match = match.group(0)
    citation_text = match.group(1).strip()

    pdf = detect_book(citation_text)
    page = extract_page(citation_text)

    if pdf is None:
        # Book not available as PDF — keep as styled text but remove HTML
        return f"*{citation_text}*"

    if pdf == PDF_DMG:
        # DMG is not searchable — keep as styled text
        return f"*{citation_text}*"

    if page is None:
        # No page number — can't link to specific page, keep as styled text
        return f"*{citation_text}*"

    # Create Obsidian PDF link: [[pdf#page=X|display text]]
    return f"[[{pdf}#page={page}|{citation_text}]]"


def process_file(filepath):
    """Process a single markdown file, converting citations."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match <span class="citation">...</span>
    pattern = r'<span class="citation">(.*?)</span>'

    new_content, count = re.subn(pattern, convert_citation, content)

    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return count


def main():
    total = 0
    files_changed = 0

    for md_file in VAULT_ROOT.rglob("*.md"):
        # Skip _other, .obsidian, .git directories
        if '.git' in md_file.parts or '.obsidian' in md_file.parts:
            continue

        count = process_file(md_file)
        if count > 0:
            print(f"  {md_file.relative_to(VAULT_ROOT)}: {count} citations converted")
            total += count
            files_changed += 1

    print(f"\nTotal: {total} citations converted across {files_changed} files")


if __name__ == "__main__":
    main()
