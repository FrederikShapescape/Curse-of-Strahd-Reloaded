"""
Add internal [[]] links throughout CoC:Reloaded markdown files.
Links NPC names, file references, and key terms to their target files.
"""

import re
from pathlib import Path

VAULT_ROOT = Path(r"C:\Users\adobe\OneDrive\vault\Curse-of-Strahd-Reloaded")

# ============================================================
# LINK TARGETS
# ============================================================

# NPC name -> link target (anchor in Non-Player Characters.md or standalone file)
# Format: display name -> (file, anchor or None)
NPCS = {
    # Death House
    "Rosavalda": ("Non-Player Characters", "Rosavalda \"Rose\" Durst"),
    "Rose Durst": ("Non-Player Characters", "Rosavalda \"Rose\" Durst"),
    "Thornboldt": ("Non-Player Characters", "Thornboldt \"Thorn\" Durst"),
    "Thorn Durst": ("Non-Player Characters", "Thornboldt \"Thorn\" Durst"),
    # Village of Barovia
    "Ismark Kolyanovich": ("Non-Player Characters", "Ismark Kolyanovich"),
    "Ireena Kolyana": ("Non-Player Characters", "Ireena Kolyana"),
    "Parriwimple": ("Non-Player Characters", "Parriwimple"),
    "Father Donavich": ("Non-Player Characters", "Father Donavich"),
    # Strahd's court
    "Volenta Popofsky": ("Non-Player Characters", "Volenta Popofsky"),
    "Ludmilla Vilisevic": ("Non-Player Characters", "Ludmilla Vilisevic"),
    "Anastrasya Karelova": ("Non-Player Characters", "Anastrasya Karelova"),
    "Rahadin": ("Non-Player Characters", "Rahadin"),
    "Cyrus Belview": ("Non-Player Characters", "Cyrus Belview"),
    "Gertruda": ("Non-Player Characters", "Gertruda"),
    "Varushka": ("Non-Player Characters", "Varushka"),
    "Escher": ("Non-Player Characters", "Escher"),
    # Vallaki
    "Father Lucian Petrovich": ("Non-Player Characters", "Father Lucian Petrovich"),
    "Father Lucian": ("Non-Player Characters", "Father Lucian Petrovich"),
    "Baron Vargas Vallakovich": ("Non-Player Characters", "Baron Vargas Vallakovich"),
    "Izek Strazni": ("Non-Player Characters", "Izek Strazni"),
    "Victor Vallakovich": ("Non-Player Characters", "Victor Vallakovich"),
    "Gadof Blinsky": ("Non-Player Characters", "Gadof Blinsky"),
    "Lady Fiona Wachter": ("Non-Player Characters", "Lady Fiona Wachter"),
    "Fiona Wachter": ("Non-Player Characters", "Lady Fiona Wachter"),
    # Vistani
    "Luvash": ("Non-Player Characters", "Luvash"),
    "Arrigal": ("Non-Player Characters", "Arrigal"),
    "Kasimir Velikov": ("Non-Player Characters", "Kasimir Velikov"),
    "Madam Eva": ("Non-Player Characters", None),  # Has her own section
    "Ezmerelda d'Avenir": ("Non-Player Characters", "Ezmerelda d'Avenir"),
    # Others
    "Morgantha": ("Non-Player Characters", "Morgantha, Dream Peddler"),
    "Dr. Rudolph van Richten": ("Non-Player Characters", "Dr. Rudolph van Richten"),
    "Muriel Vinshaw": ("Non-Player Characters", "Muriel Vinshaw"),
    "Milivoj": ("Non-Player Characters", "Milivoj"),
    "Sir Godfrey Gwilym": ("Non-Player Characters", "Sir Godfrey Gwilym"),
    "Vladimir Horngaard": ("Non-Player Characters", "Commander Vladimir Horngaard"),
    "Baron Dmitri Krezkov": ("Non-Player Characters", "Baron Dmitri Krezkov"),
    "Baba Lysaga": ("Non-Player Characters", "Baba Lysaga"),
    "Kiril Stoyanovich": ("Non-Player Characters", "Kiril Stoyanovich"),
    "Bianca Stoyanovich": ("Non-Player Characters", "Bianca Stoyanovich"),
    "Vasilka": ("Non-Player Characters", "Vasilka"),
    "Patrina": ("Non-Player Characters", "Patrina"),
    "Vilnius": ("Non-Player Characters", "Vilnius"),
}

# Standalone file references: display text -> filename (without .md)
FILE_REFS = {
    "Strahd von Zarovich": "Strahd von Zarovich",
    "History of Barovia": "History of Barovia",
    "Lore of Barovia": "Lore of Barovia",
    "Adventure Summary": "Adventure Summary",
    "Amber Shards": "Amber Shards",
}

# ============================================================
# LINKING LOGIC
# ============================================================

def is_inside_link(content, start, end):
    """Check if position is already inside a [[ ]] link or []() link."""
    # Check for [[ before position without ]] between
    before = content[:start]
    after = content[end:]

    # Inside [[...]]
    last_open = before.rfind("[[")
    last_close = before.rfind("]]")
    if last_open > last_close:
        return True

    # Inside [...](...) - the display text part
    # Check if we're between [ and ](
    last_bracket_open = before.rfind("[")
    last_bracket_close = before.rfind("]")
    if last_bracket_open > last_bracket_close:
        return True

    # Inside |display text]] part of [[link|display text]]
    if last_open != -1 and last_open > last_close:
        pipe_pos = content.find("|", last_open)
        if pipe_pos != -1 and pipe_pos < start:
            return True

    return False


def is_inside_heading(content, pos):
    """Check if position is on a heading line (starts with #)."""
    line_start = content.rfind("\n", 0, pos) + 1
    line = content[line_start:pos]
    return line.lstrip().startswith("#")


def is_inside_html_tag(content, start, end):
    """Check if position is inside an HTML tag attribute or bold markers wrapping."""
    # Check for being inside an HTML tag
    before = content[:start]
    last_lt = before.rfind("<")
    last_gt = before.rfind(">")
    if last_lt > last_gt:
        return True
    return False


def add_links_to_content(content, filename):
    """Add [[]] links to file content. Returns modified content."""

    # Track which NPCs/refs we've already linked in this file (link first occurrence only per section)
    # Actually, for navigability, let's link every occurrence

    replacements = []  # (start, end, replacement_text)

    # 1. File references (Strahd von Zarovich, History of Barovia, etc.)
    for display_text, target_file in FILE_REFS.items():
        # Skip self-references
        if filename.replace(".md", "") == target_file:
            continue

        # Find all occurrences not already linked
        pattern = re.compile(re.escape(display_text))
        for match in pattern.finditer(content):
            start, end = match.start(), match.end()

            if is_inside_link(content, start, end):
                continue
            if is_inside_heading(content, start):
                continue
            if is_inside_html_tag(content, start, end):
                continue

            link = f"[[{target_file}|{display_text}]]"
            replacements.append((start, end, link))

    # 2. NPC references
    # Sort by length (longest first) to avoid partial matches
    sorted_npcs = sorted(NPCS.items(), key=lambda x: len(x[0]), reverse=True)

    for display_text, (target_file, anchor) in sorted_npcs:
        # Skip if this NPC name is also a file ref we already handled
        if display_text in FILE_REFS:
            continue

        # Skip self-references (if file is the NPC file)
        if "Non-Player Characters" in filename:
            continue

        pattern = re.compile(re.escape(display_text))
        for match in pattern.finditer(content):
            start, end = match.start(), match.end()

            if is_inside_link(content, start, end):
                continue
            if is_inside_heading(content, start):
                continue
            if is_inside_html_tag(content, start, end):
                continue

            # Check if this overlaps with an existing replacement
            overlaps = False
            for r_start, r_end, _ in replacements:
                if start < r_end and end > r_start:
                    overlaps = True
                    break
            if overlaps:
                continue

            if anchor:
                link = f"[[{target_file}#{anchor}|{display_text}]]"
            else:
                link = f"[[{target_file}|{display_text}]]"
            replacements.append((start, end, link))

    # Apply replacements in reverse order (to preserve positions)
    replacements.sort(key=lambda x: x[0], reverse=True)
    for start, end, replacement in replacements:
        content = content[:start] + replacement + content[end:]

    return content, len(replacements)


def main():
    total = 0
    files_changed = 0

    for md_file in VAULT_ROOT.rglob("*.md"):
        if '.git' in md_file.parts or '.obsidian' in md_file.parts:
            continue
        if md_file.name == "convert_citations.py" or md_file.name == "add_internal_links.py":
            continue

        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content, count = add_links_to_content(content, md_file.name)

        if count > 0:
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  {md_file.relative_to(VAULT_ROOT)}: {count} links added")
            total += count
            files_changed += 1

    print(f"\nTotal: {total} links added across {files_changed} files")


if __name__ == "__main__":
    main()
