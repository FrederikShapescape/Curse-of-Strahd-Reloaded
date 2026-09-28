"""
Fix existing PDF citation links in CoC:Reloaded:
1. Revert all [[pdfs/...]] links and *italic* citations back to raw text
2. Re-detect correct book (fixing smart quote issues)
3. Apply correct page offsets per PDF
4. Add DMG and Xanathar's support
"""

import re
from pathlib import Path

VAULT_ROOT = Path(r"C:\Users\adobe\OneDrive\vault\Curse-of-Strahd-Reloaded")

# PDF filenames
PDF_COS = "pdfs/Curse of Strahd.pdf"
PDF_PHB = "pdfs/Player's Handbook.pdf"
PDF_MM = "pdfs/Monster Manual.pdf"
PDF_DMG = "pdfs/Dungeon Master's Guide.pdf"
PDF_VRG = "pdfs/Van Richtens Guide to Ravenloft.pdf"
PDF_XGE = "pdfs/Xanathar's Guide to Everything.pdf"

# Page offsets: how many pages to ADD to the book page number
# to get the correct PDF page
PAGE_OFFSETS = {
    PDF_COS: 1,
    PDF_PHB: 1,
    PDF_VRG: 1,
    PDF_MM: 0,
    PDF_DMG: 0,
    PDF_XGE: 1,
}

# Book keyword -> PDF mapping (normalize apostrophes for matching)
def normalize(s):
    """Normalize smart quotes and apostrophes for matching."""
    return s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"').lower()


def detect_book(citation_text):
    """Detect which book a citation refers to based on keywords."""
    norm = normalize(citation_text)

    # Check specific books first (longest match first)
    book_keywords = [
        ("xanathar's guide to everything", PDF_XGE),
        ("xanathar's guide", PDF_XGE),
        ("van richten's guide to ravenloft", PDF_VRG),
        ("van richten's guide", PDF_VRG),
        ("player's handbook", PDF_PHB),
        ("dungeon master's guide", PDF_DMG),
        ("monster manual", PDF_MM),
        ("mordenkainen presents", None),  # Not available
        ("tasha's cauldron of everything", None),  # Not available
        ("eberron", None),  # Not available
    ]

    for keyword, pdf in book_keywords:
        if keyword in norm:
            return pdf

    # Default: Curse of Strahd
    return PDF_COS


def extract_page(citation_text):
    """Extract page number from citation text."""
    patterns = [
        r'\(pp?\.\s*(\d+)(?:[–\-]\d+)?\)',
        r',\s*pp?\.\s*(\d+)',
        r'\s+pp?\.\s*(\d+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, citation_text)
        if match:
            return int(match.group(1))
    return None


def make_link(citation_text):
    """Convert citation text to an Obsidian PDF link."""
    pdf = detect_book(citation_text)
    page = extract_page(citation_text)

    if pdf is None:
        # Book not available as PDF
        return f"*{citation_text}*"

    if page is None:
        # No page number
        return f"*{citation_text}*"

    # Apply page offset
    actual_page = page + PAGE_OFFSETS.get(pdf, 0)

    return f"[[{pdf}#page={actual_page}|{citation_text}]]"


def process_file(filepath):
    """Process a single markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    count = 0

    # Step 1: Revert existing [[pdfs/...#page=N|display text]] back to raw citation text
    def revert_pdf_link(match):
        nonlocal count
        display_text = match.group(1)
        count += 1
        return make_link(display_text)

    content = re.sub(
        r'\[\[pdfs/[^|]+\|([^\]]+)\]\]',
        revert_pdf_link,
        content
    )

    # Step 2: Find *italic* citations that were previously unconverted
    # These match patterns like: *Chapter 13: The Amber Temple (p. 181)*
    # or *Dungeon Master's Guide, p. 272* etc.
    # But NOT all italic text — only ones that look like citations
    citation_patterns = [
        # Area codes: *K1. Front Courtyard*
        r'(?<!\[)\*([A-Z]\d+[a-z]?\.\s+[^*]+)\*(?!\])',
        # Chapter refs: *Chapter 13: The Amber Temple (p. 181)*
        r'(?<!\[)\*(Chapter\s+\d+[^*]*\(p\.\s*\d+\))\*(?!\])',
        # Crypt refs: *Crypt 34: King Dostron (p. 92)*
        r'(?<!\[)\*(Crypt\s+\d+[^*]*\(p\.\s*\d+\))\*(?!\])',
        # Book refs with page: *Dungeon Master's Guide, p. 272*
        r"(?<!\[)\*((?:Dungeon Master'?s Guide|Xanathar'?s Guide to Everything|Player'?s Handbook|Monster Manual|Van Richten'?s Guide to Ravenloft)[^*]*)\*(?!\])",
        # Appendix refs: *Appendix D (p. 225)*
        r'(?<!\[)\*(Appendix\s+[A-Z][^*]*\(p\.\s*\d+\))\*(?!\])',
        # Named refs with page: *Barovian Lore (p. 26)*
        r'(?<!\[)\*([A-Z][^*]{3,60}\(p\.\s*\d+(?:[–\-]\d+)?\))\*(?!\])',
    ]

    for pattern in citation_patterns:
        def convert_italic(match):
            nonlocal count
            text = match.group(1)
            result = make_link(text)
            if result != f"*{text}*":
                count += 1
                return result
            return match.group(0)  # Keep as italic if no PDF available

        content = re.sub(pattern, convert_italic, content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    return count


def main():
    total = 0
    files_changed = 0

    for md_file in VAULT_ROOT.rglob("*.md"):
        if '.git' in md_file.parts or '.obsidian' in md_file.parts:
            continue
        if md_file.name.endswith('.py'):
            continue

        count = process_file(md_file)
        if count > 0:
            print(f"  {md_file.relative_to(VAULT_ROOT)}: {count} links fixed")
            total += count
            files_changed += 1

    print(f"\nTotal: {total} links fixed across {files_changed} files")


if __name__ == "__main__":
    main()
